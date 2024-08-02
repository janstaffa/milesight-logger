interface ServerResponse {
  status: 'ok' | 'err';
  timestamp: number;
  data?: any;
  message?: string;
}

interface Sensor {
  eui: string;
  name?: string;
}

interface SensorData {
  sensor: Sensor;
  temperature: number;
  humidity: number;
  battery: number;
  timestamp: number;
}
