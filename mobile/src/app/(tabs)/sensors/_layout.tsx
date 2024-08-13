import { Stack } from 'expo-router';
import React from 'react';

import SensorDataProvider from '@providers/SensorDataProvider';
import { useThemeColors } from '../../../components/Themed';

export default function SensorStack() {
  const colors = useThemeColors();

  return (
    <SensorDataProvider>
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: colors.background,
          },
          headerTintColor: colors.text,
        }}
      />
    </SensorDataProvider>
  );
}
