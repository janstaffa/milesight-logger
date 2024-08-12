/**
 * Learn more about Light and Dark modes:
 * https://docs.expo.io/guides/color-schemes/
 */

import {
  Text as DefaultText,
  TouchableOpacity as DefaultTouchableOpacity,
  View as DefaultView,
} from 'react-native';

import Colors from '@/src/constants/Colors';
import { ColorMode, useSettings } from '../providers/SettingsProvider';

type ThemeProps = {
  lightColor?: string;
  darkColor?: string;
};

export type TextProps = ThemeProps & DefaultText['props'];
export type ViewProps = ThemeProps & DefaultView['props'];
export type TouchableOpacityProps = ThemeProps & DefaultTouchableOpacity['props'];

export function useThemeColors() {
  const { colorMode } = useSettings();
  const colorModeName = colorMode === ColorMode.Dark ? 'dark' : 'light';
  return Colors[colorModeName];
}

export function Text(props: TextProps) {
  const { style, ...otherProps } = props;
  const color = useThemeColors()['text'];

  return <DefaultText style={[{ color }, style]} {...otherProps} />;
}

export function View(props: ViewProps) {
  const { style, ...otherProps } = props;
  const backgroundColor = useThemeColors()['background'];

  return <DefaultView style={[{ backgroundColor }, style]} {...otherProps} />;
}

export function TouchableOpacity(props: TouchableOpacityProps) {
  const { style, ...otherProps } = props;
  const backgroundColor = useThemeColors()['background'];

  return (
    <DefaultTouchableOpacity
      style={[{ backgroundColor }, style]}
      {...otherProps}
    />
  );
}
