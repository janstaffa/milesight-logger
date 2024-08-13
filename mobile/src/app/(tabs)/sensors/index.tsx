import { FlatList, Pressable, StyleSheet } from 'react-native';

import SensorCard from '@components/SensorCard';
import { useThemeColors, View } from '@components/Themed';
import { FontAwesome } from '@expo/vector-icons';
import { useSensorData } from '@providers/SensorDataProvider';
import { Stack } from 'expo-router';
import { useSettings } from '../../../providers/SettingsProvider';

export default function SensorsScreen() {
  const { sensorData, fetchData } = useSensorData();
  const { tempUnit } = useSettings();

  const colors = useThemeColors();


  return (
    <>
      <View style={styles.container}>
        <FlatList
          data={sensorData}
          renderItem={({ item }) => (
            <SensorCard sensorData={item} tempUnit={tempUnit} />
          )}
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
                  color={colors.text}
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
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
});
