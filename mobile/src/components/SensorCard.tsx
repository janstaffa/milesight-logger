import { Text, TouchableOpacity, View } from '@components/Themed';
import { Href, useRouter } from 'expo-router';
import { StyleSheet } from 'react-native';
import { getColorGradient } from '../app/utils';
import { TemperatureUnit } from '../providers/SettingsProvider';

export interface SensorCardProps {
  sensorData: SensorData;
  tempUnit: TemperatureUnit;
}

const SensorCard: React.FC<SensorCardProps> = ({ sensorData, tempUnit }) => {
  const router = useRouter();

  const tempmNorm = Math.min(Math.max(sensorData.temperature, 0), 30) / 30; // Color range: 0-30°C
  const humNorm = sensorData.humidity / 100;
  const batNorm = sensorData.battery / 255;
  const tempColor = getColorGradient('#0000ff', '#ff0000', tempmNorm);
  const humColor = getColorGradient('#0000ff', '#ff0000', humNorm);
  const batColor = getColorGradient('#ff0000', '#00ff00', batNorm);

  let tempVal = sensorData.temperature;

  if (tempUnit === TemperatureUnit.Fahrenheit) {
    tempVal = (9 / 5) * tempVal + 32;
  } else if (tempUnit === TemperatureUnit.Kelvin) {
    tempVal += 273.15;
  }

  const unit =
    tempUnit === TemperatureUnit.Celsius
      ? '°C'
      : tempUnit === TemperatureUnit.Fahrenheit
      ? '°F'
      : 'K';

  return (
    <TouchableOpacity
      style={styles.container}
      onPress={() => router.push(`/sensors/${sensorData.sensor.eui}` as Href)}
    >
      <Text style={styles.title}>Sensor - {sensorData.sensor.eui}</Text>
      <View style={styles.dataRow}>
        <View style={styles.dataDisplayWrap}>
          <Text style={[styles.dataDisplay, { color: tempColor }]}>
            {tempVal.toFixed(1)}
            {unit}
          </Text>
          <Text style={styles.dataTitle}>Temperature</Text>
        </View>
        <View style={styles.dataDisplayWrap}>
          <Text style={[styles.dataDisplay, { color: humColor }]}>
            {sensorData.humidity.toFixed(1)}%
          </Text>
          <Text style={styles.dataTitle}>Humidity</Text>
        </View>
        <View style={styles.dataDisplayWrap}>
          <Text style={[styles.dataDisplay, { color: batColor }]}>
            {(batNorm * 100).toFixed(1)}%
          </Text>
          <Text style={styles.dataTitle}>Battery</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    borderColor: 'lightgray',
    borderWidth: 1,
    borderRadius: 8,
    padding: 10,
    gap: 15,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  dataRow: {
    flexDirection: 'row',
    gap: 10,
    justifyContent: 'space-evenly',
  },
  dataDisplayWrap: {
    flexDirection: 'column',
    alignItems: 'center',
  },
  dataDisplay: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  dataTitle: {
    fontSize: 12,
  },
});

export default SensorCard;
