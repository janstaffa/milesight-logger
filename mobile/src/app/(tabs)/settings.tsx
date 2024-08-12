import { StyleSheet, Switch, TextInput, TouchableOpacity } from 'react-native';

import { Text, View } from '@/src/components/Themed';
import { Picker } from '@react-native-picker/picker';
import { useState } from 'react';
import Colors from '../../constants/Colors';
import {
  ColorMode,
  TemperatureUnit,
  useSettings,
} from '../../providers/SettingsProvider';

export default function SettingsScreen() {
  const { serverUrl, autoRefresh, colorMode, tempUnit, saveSettings } =
    useSettings();

  const [newServerURL, setNewServerURL] = useState(serverUrl);
  const [newDarkMode, setNewDarkMode] = useState(colorMode === ColorMode.Dark);
  const [newAutoRefresh, setNewAutoRefresh] = useState(autoRefresh);
  const [newTempUnit, setNewTempUnit] = useState<TemperatureUnit>(tempUnit);

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <Text style={styles.title}>Data server</Text>
        <TextInput
          style={styles.input}
          onChangeText={(t) => setNewServerURL(t)}
          value={newServerURL}
          placeholder="localhost:1111"
          autoCapitalize="none"
        />
      </View>
      <View style={styles.row}>
        <Text style={styles.title}>Dark mode</Text>
        <Switch
          value={newDarkMode}
          onValueChange={(v) => setNewDarkMode(v)}
          style={{ alignSelf: 'flex-start' }}
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.title}>Automatic refreshing</Text>
        <Switch
          value={newAutoRefresh}
          onValueChange={(v) => setNewAutoRefresh(v)}
          style={{ alignSelf: 'flex-start' }}
        />
      </View>
      <View style={styles.row}>
        <Text style={styles.title}>Temperature units</Text>
        <View style={styles.pickerContainer}>
          <Picker
            selectedValue={newTempUnit}
            onValueChange={(itemValue, _) => {
              setNewTempUnit(itemValue);
            }}
            mode="dialog"
          >
            <Picker.Item label="Celsius (°C)" value={TemperatureUnit.Celsius} />
            <Picker.Item
              label="Fahrenheit (°F)"
              value={TemperatureUnit.Fahrenheit}
            />
            <Picker.Item label="Kelvin (K)" value={TemperatureUnit.Kelvin} />
          </Picker>
        </View>
      </View>
      <TouchableOpacity
        style={styles.button}
        activeOpacity={0.7}
        onPress={() =>
          saveSettings({
            serverUrl: newServerURL,
            darkMode: newDarkMode,
            autoRefresh: newAutoRefresh,
            tempUnit: newTempUnit,
          })
        }
      >
        <Text style={styles.buttonText}>Save</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  input: {
    height: 50,
    marginVertical: 10,
    borderWidth: 1,
    borderColor: 'gray',
    borderRadius: 5,
    padding: 10,
  },
  pickerContainer: {
    borderColor: 'gray',
    borderWidth: 1,
    marginVertical: 10,
    borderRadius: 5,
    overflow: 'hidden',
  },
  row: {
    width: '100%',
    height: 'auto',
  },
  button: {
    marginTop: 'auto',
    padding: 10,
    backgroundColor: Colors.light.tabIconSelected,
    borderRadius: 8,
  },
  buttonText: {
    color: 'white',
    textAlign: 'center',
    fontWeight: 'bold',
  },
});
