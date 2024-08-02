import { Alert } from 'react-native';

export const showErrorAlert = (msg: string, title = 'Error') => {
  Alert.alert(
    title,
    msg,
    [
      {
        text: 'OK',
        style: 'default',
      },
    ],
    {
      cancelable: true,
    }
  );
};

/**
 * @param i Floating point value from 0 to 1
 */

export function getColorGradient(color1: string, color2: string, i: number) {
  if (i < 0 || i > 1) throw new Error('Invalid argument i');

  const parsed1 = color1.trim().replace('#', '');
  const parsed2 = color2.trim().replace('#', '');

  const [r1, g1, b1] = [
    parseInt(parsed1.slice(0, 2), 16),
    parseInt(parsed1.slice(2, 4), 16),
    parseInt(parsed1.slice(4), 16),
  ];
  const [r2, g2, b2] = [
    parseInt(parsed2.slice(0, 2), 16),
    parseInt(parsed2.slice(2, 4), 16),
    parseInt(parsed2.slice(4), 16),
  ];

  const newR = Math.round(r1 + i * (r2 - r1));
  const newG = Math.round(g1 + i * (g2 - g1));
  const newB = Math.round(b1 + i * (b2 - b1));

  return (
    '#' +
    ('00' + newR.toString(16)).slice(-2) +
    ('00' + newG.toString(16)).slice(-2) +
    ('00' + newB.toString(16)).slice(-2)
  );
}
