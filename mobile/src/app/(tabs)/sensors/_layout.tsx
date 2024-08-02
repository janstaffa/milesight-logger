import { Stack } from 'expo-router';
import React from 'react';

import SensorDataProvider from '@providers/SensorDataProvider';

export default function SensorStack() {
  return (
    <SensorDataProvider>
      <Stack />
    </SensorDataProvider>
  );
}
