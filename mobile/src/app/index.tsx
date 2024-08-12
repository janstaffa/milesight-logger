import { Pressable, StyleSheet, TextInput } from 'react-native';

import { Text, View } from '@/src/components/Themed';
import { useRouter } from 'expo-router';
import { useEffect, useState } from 'react';
import Colors from '../constants/Colors';
import { useSettings } from '../providers/SettingsProvider';
import { showErrorAlert } from './utils';

export default function SetupScreen() {
  const router = useRouter();

  const { serverUrl, saveSettings } = useSettings();

  const [newServerURL, setNewServerURL] = useState('');

  useEffect(() => {
    if (serverUrl.length > 0) router.replace('/sensors');
  }, [serverUrl]);

  return (
    <View style={styles.container}>
      <Text style={styles.welcomeMessage}>Welcome to Milesight logger!</Text>
      <Text style={styles.title}>Please enter your data server:</Text>
      <View style={styles.row}>
        <TextInput
          style={styles.input}
          onChangeText={(t) => setNewServerURL(t)}
          value={newServerURL}
          placeholder="localhost:1111"
          autoCapitalize="none"
        />
        <Pressable
          style={({ pressed }) => [
            styles.button,
            pressed ? { backgroundColor: Colors.light.tabIconSelected } : {},
          ]}
          onPress={() => {
            if (newServerURL.length === 0)
              return showErrorAlert(
                'Server address cannot be empty',
                'User error'
              );
            saveSettings(
              {
                serverUrl: newServerURL,
              },
              false
            );
            router.replace('/sensors');
          }}
        >
          {({ pressed }) => (
            <Text
              style={[styles.buttonText, pressed ? { color: 'white' } : {}]}
            >
              Next
            </Text>
          )}
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    flexDirection: 'column',
    justifyContent: 'center',
  },
  welcomeMessage: {
    fontSize: 23,
    marginBottom: 30,
    textAlign: 'center',
  },
  title: {
    fontSize: 18,
    marginVertical: 10,
    textAlign: 'center',
  },
  input: {
    height: '100%',
    marginVertical: 10,
    borderWidth: 1,
    borderColor: 'gray',
    borderRightWidth: 0,
    borderTopLeftRadius: 8,
    borderBottomLeftRadius: 8,
    padding: 10,
    flex: 1,
  },
  button: {
    borderColor: Colors.light.tabIconSelected,
    borderWidth: 2,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 16,
    borderTopRightRadius: 8,
    borderBottomRightRadius: 8,
    height: '100%',
  },
  buttonText: {
    color: Colors.light.tabIconSelected,
    textAlign: 'center',
  },
  row: {
    height: 60,
    width: '100%',
    flexDirection: 'row',
    alignItems: 'center',
  },
});
