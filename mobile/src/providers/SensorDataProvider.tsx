import { createContext, useContext, useEffect, useRef, useState } from 'react';
import { showErrorAlert, showStyledFlashMessage } from '../app/utils';
import { useSettings } from './SettingsProvider';

interface SensorDataContextType {
  sensorData: SensorData[];
  fetchData: () => void;
}
const SensorDataContext = createContext<SensorDataContextType>({
  sensorData: [],
  fetchData: () => {},
});

export const DEFAULT_API_URL = 'http://10.0.0.2:1111/api';
export const POLLING_INTERVAL = 10 * 1000; // 10 seconds

const SensorDataProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const { serverUrl, autoRefresh } = useSettings();
  const [sensors, setSensors] = useState<Sensor[]>([]);

  const serverApi = serverUrl + '/api';
  const fetchSensors = () => {
    if (serverUrl.length === 0) return;
    fetch(serverApi + '/devices')
      .then((d) => d.json())
      .then((response: ServerResponse) => {
        if (response.status === 'err') return showErrorAlert(response.message!);
        if (!response.data) return showErrorAlert('Invalid server response');
        const fetchedSensors: Sensor[] = response.data.map((s: string) => ({
          eui: s,
        }));
        setSensors(fetchedSensors);
      })
      .catch((e) => {
        showStyledFlashMessage({
          message: 'Network error, check server URL',
          type: 'danger',
        });
      });
  };
  useEffect(() => {
    fetchSensors();
  }, []);

  const fetchSensorData = async (sens: Sensor[]): Promise<SensorData[]> => {
    const requests = sens.map((s) =>
      fetch(serverApi + '/latest' + `?device=${s.eui}`)
        .then((d) => d.json())
        .then((response: ServerResponse) => {
          if (response.status === 'err') {
            showErrorAlert(response.message!);
            throw 'Network error';
          }

          if (!response.data) {
            showErrorAlert('Invalid server response');
            throw 'Network error';
          }

          const sensorDataEntry: SensorData = {
            sensor: s,
            temperature: response.data.temp,
            humidity: response.data.hum,
            battery: response.data.bat,
            timestamp: response.data.timestamp,
          };

          return sensorDataEntry;
        })
    );

    return Promise.all(requests);
  };

  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  let interval = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (sensors.length === 0) return;
    const _fetchSensorData = () =>
      fetchSensorData(sensors)
        .then((d) => {
          setSensorData(d);
        })
        .catch((_) => {
          showStyledFlashMessage({ message: 'Network error, check server URL', type: 'danger' });
        });

    _fetchSensorData();

    if (autoRefresh) {
      interval.current = setInterval(_fetchSensorData, POLLING_INTERVAL);
    } else {
      interval.current !== null && clearInterval(interval.current);
    }

    return () => {
      interval.current !== null && clearInterval(interval.current);
    };
  }, [sensors, autoRefresh]);

  return (
    <SensorDataContext.Provider value={{ sensorData, fetchData: fetchSensors }}>
      {children}
    </SensorDataContext.Provider>
  );
};

export default SensorDataProvider;

export const useSensorData = () => useContext(SensorDataContext);
