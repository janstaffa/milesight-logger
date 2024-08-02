import { createContext, useContext, useEffect, useState } from 'react';
import { showErrorAlert } from '../app/utils';

interface SensorDataContextType {
  sensorData: SensorData[];
  fetchData: () => void;
}
const SensorDataContext = createContext<SensorDataContextType>({
  sensorData: [],
  fetchData: () => {},
});

const DEFAULT_API_URL = 'http://78.80.32.122:1111/api';

const SensorDataProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const [sensors, setSensors] = useState<Sensor[]>([]);

  const fetchSensors = () => {
    fetch(DEFAULT_API_URL + '/devices')
      .then((d) => d.json())
      .then((response: ServerResponse) => {
        if (response.status === 'err') return showErrorAlert(response.message!);
        if (!response.data) return showErrorAlert('Invalid server response');
        const fetchedSensors: Sensor[] = response.data.map((s: string) => ({
          eui: s,
        }));
        setSensors(fetchedSensors);
      });
  };
  useEffect(() => {
    fetchSensors();
  }, []);

  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  useEffect(() => {
    const fetchedSensorData: SensorData[] = [];
    const requests = sensors.map((s) =>
      fetch(DEFAULT_API_URL + '/latest' + `?device=${s.eui}`)
        .then((d) => d.json())
        .then((response: ServerResponse) => {
          if (response.status === 'err')
            return showErrorAlert(response.message!);
          if (!response.data) return showErrorAlert('Invalid server response');
          const sensorDataEntry: SensorData = {
            sensor: s,
            temperature: response.data.temp,
            humidity: response.data.hum,
            battery: response.data.bat,
            timestamp: response.data.timestamp,
          };

          fetchedSensorData.push(sensorDataEntry);
        })
    );

    Promise.all(requests).then(() => {
      setSensorData(fetchedSensorData);
    });
  }, [sensors]);

  return (
    <SensorDataContext.Provider value={{ sensorData, fetchData: fetchSensors }}>
      {children}
    </SensorDataContext.Provider>
  );
};

export default SensorDataProvider;


export const useSensorData = () => useContext(SensorDataContext);