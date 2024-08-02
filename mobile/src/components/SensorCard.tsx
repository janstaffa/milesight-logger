import { Href, Link } from 'expo-router';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { getColorGradient } from '../app/utils';

export interface SensorCardProps {
  sensorData: SensorData;
}

const SensorCard: React.FC<SensorCardProps> = ({ sensorData }) => {
  const tempmNorm = Math.min(Math.max(sensorData.temperature, 0), 30) / 30; // Color range: 0-30°C
  const humNorm = sensorData.humidity / 100;
  const batNorm = sensorData.battery / 255;
  const tempColor = getColorGradient('#0000ff', '#ff0000', tempmNorm);
  const humColor = getColorGradient('#0000ff', '#ff0000', humNorm);
  const batColor = getColorGradient('#ff0000', '#00ff00', batNorm);

  return (
    <Link href={`/sensors/${sensorData.sensor.eui}` as Href} asChild>
      <TouchableOpacity style={styles.container}>
        <Text style={styles.title}>Sensor - {sensorData.sensor.eui}</Text>
        <View style={styles.dataRow}>
          <View style={styles.dataDisplayWrap}>
            <Text style={[styles.dataDisplay, { color: tempColor }]}>
              {sensorData.temperature}°C
            </Text>
            <Text style={styles.dataTitle}>Temperature</Text>
          </View>
          <View style={styles.dataDisplayWrap}>
            <Text style={[styles.dataDisplay, { color: humColor }]}>
              {sensorData.humidity}%
            </Text>
            <Text style={styles.dataTitle}>Humidity</Text>
          </View>
          <View style={styles.dataDisplayWrap}>
            <Text style={[styles.dataDisplay, { color: batColor }]}>
              {Math.round(batNorm * 100)}%
            </Text>
            <Text style={styles.dataTitle}>Battery</Text>
          </View>
        </View>
      </TouchableOpacity>
    </Link>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'white',
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
