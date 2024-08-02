import { StyleSheet } from 'react-native';

import { Text, View } from '@/src/components/Themed';

export default function TabTwoScreen() {
  return (
    <View style={styles.container}>
      <Text>Server select</Text>
      <Text>Light/dark mode</Text>
      <Text>Automatic refreshing</Text>
      <Text>Celsius/Fahrenheit</Text>
    </View>
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
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
