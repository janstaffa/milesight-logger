import { StyleSheet, Text } from 'react-native';

import { View } from '@components/Themed';
import { useSensorData } from '@providers/SensorDataProvider';
import { Stack, useLocalSearchParams } from 'expo-router';

export default function SensorDetailsScreen() {
  const { eui } = useLocalSearchParams();
  const { sensorData } = useSensorData();
  
  if (typeof eui !== 'string') return <Text>Invalid params</Text>;

  const data = sensorData.find((s) => s.sensor.eui === eui);
  if (!data) return <Text>Sensor data not found</Text>;

  return (
    <>
      <View style={styles.container}>
        <Text>Name: -</Text>
        <Text>EUI:{eui}</Text>
        <Text>Temperature: {data.temperature}°C</Text>
        <Text>Humidity: {data.humidity}%</Text>
        <Text>Battery: {Math.round((data.battery / 255) * 100)}%</Text>
      </View>
      <Stack.Screen options={{ title: eui }} />
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    backgroundColor: '#fafafa',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
});
