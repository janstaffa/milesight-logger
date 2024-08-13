import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { createContext, useContext, useEffect, useState } from 'react';
import { showErrorAlert, showStyledFlashMessage } from '../app/utils';

export enum ColorMode {
  Light,
  Dark,
}
export enum TemperatureUnit {
  Celsius = 1,
  Fahrenheit = 2,
  Kelvin = 3,
}
interface SettingsContextType {
  serverUrl: string;
  colorMode: ColorMode;
  autoRefresh: boolean;
  tempUnit: TemperatureUnit;
  saveSettings: (
    settings: {
      serverUrl?: string;
      darkMode?: boolean;
      autoRefresh?: boolean;
      tempUnit?: TemperatureUnit;
    },
    showMsg?: boolean
  ) => void;
}
const SettingsContext = createContext<SettingsContextType>({
  serverUrl: '',
  colorMode: ColorMode.Light,
  autoRefresh: false,
  tempUnit: TemperatureUnit.Celsius,
  saveSettings: () => {},
});

const SettingsProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const router = useRouter();

  const [serverUrl, setServerURL] = useState('');
  const [colorMode, setColorMode] = useState(ColorMode.Light);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [tempUnit, setTempUnit] = useState<TemperatureUnit>(
    TemperatureUnit.Celsius
  );

  const loadSettings = async () => {
    const loadedColorMode = await AsyncStorage.getItem('color_mode');
    loadedColorMode && setColorMode(parseInt(loadedColorMode) as ColorMode);
    const loadedAutoRefresh = await AsyncStorage.getItem('auto_refresh');
    loadedAutoRefresh && setAutoRefresh(!!parseInt(loadedAutoRefresh));
    const loadedTempUnit = await AsyncStorage.getItem('temp_unit');
    loadedTempUnit && setTempUnit(parseInt(loadedTempUnit) as TemperatureUnit);

    const loadedServerUrl = await AsyncStorage.getItem('server_url');
    if (loadedServerUrl) setServerURL(loadedServerUrl);
    else {
      // router.replace('/');
      return false;
    }
    return true;
  };

  const saveSettings = (
    settings: {
      serverUrl?: string;
      darkMode?: boolean;
      autoRefresh?: boolean;
      tempUnit?: TemperatureUnit;
    },
    showMsg: boolean = true
  ) => {
    const { serverUrl, darkMode, autoRefresh, tempUnit } = settings;
    if (serverUrl !== undefined) {
      if (serverUrl.length === 0)
        return showErrorAlert('Server URL cannot be empty', 'User error');

      AsyncStorage.setItem('server_url', serverUrl);
      setServerURL(serverUrl);
    }

    if (darkMode !== undefined) {
      const colorMode = darkMode ? ColorMode.Dark : ColorMode.Light;
      AsyncStorage.setItem('color_mode', colorMode.toString());
      setColorMode(colorMode);
    }

    if (autoRefresh !== undefined) {
      AsyncStorage.setItem('auto_refresh', autoRefresh ? '1' : '0');
      setAutoRefresh(autoRefresh);
    }
    if (tempUnit !== undefined) {
      AsyncStorage.setItem('temp_unit', tempUnit.toString());
      setTempUnit(tempUnit);
    }

    showMsg &&
      showStyledFlashMessage({ message: 'Setting saved', type: 'success' });
  };
  useEffect(() => {
    loadSettings().then((success) => {
      success &&
        showStyledFlashMessage({ message: 'Settings loaded', type: 'info' });
    });
  }, []);

  return (
    <>
      <SettingsContext.Provider
        value={{
          serverUrl,
          colorMode,
          autoRefresh,
          tempUnit,
          saveSettings,
        }}
      >
        {children}
      </SettingsContext.Provider>
      <StatusBar style={colorMode == ColorMode.Dark ? 'light' : 'dark'} />
    </>
  );
};

export default SettingsProvider;

export const useSettings = () => useContext(SettingsContext);
