import { StyleSheet, Text } from 'react-native';

import { View } from '@components/Themed';
import { DEFAULT_API_URL, useSensorData } from '@providers/SensorDataProvider';
import { Stack, useLocalSearchParams } from 'expo-router';

import {
  Circle,
  LinearGradient,
  useFont,
  vec,
} from '@shopify/react-native-skia';

import spacemono from '@assets/fonts/SpaceMono-Regular.ttf';

import { SharedValue, useDerivedValue } from 'react-native-reanimated';
import { Area, CartesianChart, Line, useChartPressState } from 'victory-native';

import { Picker } from '@react-native-picker/picker';
import { Text as SKText } from '@shopify/react-native-skia';
import { format as format_date } from 'date-fns';
import { useEffect, useState } from 'react';
import {
  TemperatureUnit,
  useSettings,
} from '../../../providers/SettingsProvider';
import { showErrorAlert, toFahrenheit, toKelvin } from '../../utils';
type PointData = Record<string, number>;
type LineData = PointData[];

type DataParameter = 'temperature' | 'humidity' | 'battery';
interface WeekData {
  [key: string]: LineData;
}

const CHART_COLORS = {
  temperature: '#FF0000',
  humidity: '#0000FF',
  battery: '#FCC600',
};

export default function SensorDetailsScreen() {
  const { eui } = useLocalSearchParams();
  const { sensorData } = useSensorData();

  const [weekData, setWeekData] = useState<WeekData | null>(null);
  const [selectedParameter, setSelectedParameter] =
    useState<DataParameter>('temperature');

  const { tempUnit: selectedTempUnit } = useSettings();

  const tempUnit =
    selectedTempUnit === TemperatureUnit.Celsius
      ? '°C'
      : selectedTempUnit === TemperatureUnit.Fahrenheit
      ? '°F'
      : 'K';

  const fetchWeekData = () => {
    fetch(DEFAULT_API_URL + '/week' + `?device=${eui}`)
      .then((d) => d.json())
      .then((response: ServerResponse) => {
        if (response.status === 'err') return showErrorAlert(response.message!);
        if (!response.data) return showErrorAlert('Invalid server response');

        const fetchedWeekData: WeekData = {
          temperature: [],
          humidity: [],
          battery: [],
        };

        for (const key in fetchedWeekData) {
          const tempData = response.data.data[key];

          const lineData: LineData = [];
          for (let i = 0; i < tempData.timestamps.length; i++) {
            const x = tempData.timestamps[i];
            let y = tempData.vals[i];

            // Normalize battery values
            if (key === 'battery') {
              y /= 255;
              y *= 100;
            } else if (key === 'temperature') {
              if (selectedTempUnit === TemperatureUnit.Fahrenheit)
                y = toFahrenheit(y);
              else if (selectedTempUnit === TemperatureUnit.Kelvin)
                y = toKelvin(y);
            }
            const point = {
              timestamp: x,
              value: y,
            };
            lineData.push(point);
          }
          fetchedWeekData[key] = lineData;
        }
        setWeekData(fetchedWeekData);
      });
  };
  useEffect(() => {
    fetchWeekData();
  }, []);

  const font = useFont(spacemono, 12);
  const tooltipFont = useFont(spacemono, 16);

  const { state, isActive } = useChartPressState({ x: 0, y: { value: 0 } });

  const time = useDerivedValue(() => {
    const d = new Date(state.x.value.value);
    const dateStr = `${d.getDate()}/${d.getMonth()} ${(
      '00' + d.getHours()
    ).slice(-2)}:${('00' + d.getMinutes()).slice(-2)}`;

    return dateStr;
  }, [state]);

  const value = useDerivedValue(() => {
    const unit = selectedParameter === 'temperature' ? tempUnit : '%';
    return state.y.value.value.value.toFixed(2).toString() + unit;
  }, [state, selectedParameter]);

  if (typeof eui !== 'string') return <Text>Invalid params</Text>;

  const data = sensorData.find((s) => s.sensor.eui === eui);
  if (!data) return <Text>Sensor data not found</Text>;

  let tempVal = data.temperature;

  if (selectedTempUnit === TemperatureUnit.Fahrenheit)
    tempVal = toFahrenheit(tempVal);
  else if (selectedTempUnit === TemperatureUnit.Kelvin)
    tempVal = toKelvin(tempVal);
  
  return (
    <>
      <View style={styles.container}>
        <View style={styles.dataWrap}>
          <Text>Name: -</Text>
          <Text>EUI: {eui}</Text>
          <Text>Last message: {new Date(data.timestamp).toLocaleString()}</Text>
          <Text>
            Temperature: {tempVal.toFixed(2)}
            {tempUnit}
          </Text>
          <Text>Humidity: {data.humidity.toFixed(2)}%</Text>
          <Text>Battery: {((data.battery / 255) * 100).toFixed(2)}%</Text>
        </View>
        <View style={styles.chartWrap}>
          <View style={styles.pickerContainer}>
            <Picker
              selectedValue={selectedParameter}
              onValueChange={(itemValue, _) => setSelectedParameter(itemValue)}
              mode="dropdown"
            >
              <Picker.Item label="Temperature" value="temperature" />
              <Picker.Item label="Humidity" value="humidity" />
              <Picker.Item label="Battery" value="battery" />
            </Picker>
          </View>
          {weekData && (
            <CartesianChart
              data={weekData[selectedParameter]}
              xKey={'timestamp'}
              yKeys={['value']}
              domainPadding={30}
              axisOptions={{
                labelColor: 'black',
                lineColor: 'black',
                font,
                tickCount: {
                  x: 6,
                  y: 10,
                },
                formatYLabel(label) {
                  const unit =
                    selectedParameter === 'temperature' ? tempUnit : '%';
                  return label.toString() + unit;
                },
                formatXLabel(label) {
                  const d = new Date(label);
                  const now = new Date();
                  let fmtStr = 'dd/MM';
                  if (d.getFullYear() != now.getFullYear()) fmtStr += ' yyyy'; // Show year if not this year
                  if (
                    new Date(d.toDateString()).getTime() ==
                    new Date(now.toDateString()).getTime()
                  )
                    fmtStr += ' HH:mm'; // Show time if it is today
                  return format_date(d, fmtStr);
                },
              }}
              chartPressState={state}
            >
              {({ points, chartBounds }) => {
                return (
                  <>
                    <Line
                      points={points.value}
                      color={CHART_COLORS[selectedParameter]}
                      strokeWidth={2}
                      animate={{ type: 'timing', duration: 500 }}
                    />
                    <Area
                      points={points.value}
                      y0={chartBounds.bottom}
                      animate={{ type: 'timing', duration: 500 }}
                    >
                      <LinearGradient
                        start={vec(chartBounds.bottom, 200)}
                        end={vec(chartBounds.bottom, chartBounds.bottom)}
                        colors={[
                          CHART_COLORS[selectedParameter] + 'a0',
                          CHART_COLORS[selectedParameter] + '05',
                        ]}
                      />
                    </Area>
                    {isActive && (
                      <>
                        <Tooltip
                          x={state.x.position}
                          y={state.y.value.position}
                        />
                        <SKText
                          x={state.x.position}
                          y={state.y.value.position}
                          transform={[{ translateY: -30 }]}
                          font={tooltipFont}
                          text={time}
                          color={'black'}
                          style={'fill'}
                        />
                        <SKText
                          x={state.x.position}
                          y={state.y.value.position}
                          transform={[{ translateY: -10 }]}
                          font={tooltipFont}
                          text={value}
                          color={'black'}
                          style={'fill'}
                        />
                      </>
                    )}
                  </>
                );
              }}
            </CartesianChart>
          )}
        </View>
      </View>
      <Stack.Screen options={{ title: eui }} />
    </>
  );
}

const Tooltip = ({
  x,
  y,
}: {
  x: SharedValue<number>;
  y: SharedValue<number>;
}) => {
  return <Circle cx={x} cy={y} color={'grey'} opacity={0.8} r={4} />;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    // backgroundColor: '#fafafa',
    // backgroundColor: 'black'
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  dataWrap: {
    backgroundColor: '#fafafa',
    padding: 10,
    borderRadius: 5,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.2,
    shadowRadius: 2,

    elevation: 4,
  },
  chartWrap: {
    flex: 1,
    marginTop: 20,
  },
  pickerContainer: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 4,
    borderRadius: 5,
    overflow: 'hidden',
    marginBottom: 15,
  },
});
