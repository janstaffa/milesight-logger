import { FlatList, Pressable, StyleSheet } from 'react-native';

import SensorCard from '@components/SensorCard';
import { View } from '@components/Themed';
import { FontAwesome } from '@expo/vector-icons';
import { useSensorData } from '@providers/SensorDataProvider';
import { Stack } from 'expo-router';
import { Colors } from 'react-native/Libraries/NewAppScreen';

export default function SensorsScreen() {
  const { sensorData, fetchData } = useSensorData();
  return (
    <>
      <View style={styles.container}>
        <FlatList
          data={sensorData}
          renderItem={({ item }) => <SensorCard sensorData={item} />}
        />
      </View>
      <Stack.Screen
        options={{
          title: 'Sensors',
          headerRight: () => (
            <Pressable
              onPress={() => {
                fetchData();
              }}
            >
              {({ pressed }) => (
                <FontAwesome
                  name="refresh"
                  size={25}
                  color={Colors.light.text}
                  style={{ marginRight: 15, opacity: pressed ? 0.5 : 1 }}
                />
              )}
            </Pressable>
          ),
        }}
      ></Stack.Screen>
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
