import React from 'react';
import { TouchableOpacity, Text, ActivityIndicator } from 'react-native';

export const ProjectButton = ({ name, onPress, loading, styles }) => (
  <TouchableOpacity 
    style={[styles.button, loading && styles.disabled]} 
    onPress={onPress}
    disabled={loading}
  >
    {loading ? (
      <ActivityIndicator color="#fff" />
    ) : (
      <Text style={styles.buttonText}>{name}</Text>
    )}
  </TouchableOpacity>
);
