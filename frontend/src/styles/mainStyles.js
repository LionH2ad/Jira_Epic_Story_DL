import { StyleSheet } from 'react-native';
import { Theme } from '../../../shared/theme/themeManager';

export const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    padding: Theme?.layout?.padding || 30, 
    backgroundColor: Theme?.colors?.background || '#f0f2f5' 
  },
  header: {
    marginBottom: 40,
    alignItems: 'center'
  },
  title: { 
    fontSize: 32, 
    fontWeight: '800', 
    color: Theme?.colors?.primary || '#44546A',
    letterSpacing: -1
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 5
  },
  buttonGrid: { 
    flexDirection: 'row', 
    flexWrap: 'wrap', 
    justifyContent: 'space-between', 
    marginBottom: 30 
  },
  button: { 
    backgroundColor: Theme?.colors?.primary || '#44546A', 
    width: '48%', 
    paddingVertical: 18, 
    borderRadius: 12, 
    marginBottom: 15, 
    alignItems: 'center',
    elevation: 4, // Android Shadow
    shadowColor: '#000', // iOS Shadow
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8
  },
  buttonText: { 
    color: '#000',
    fontSize: 15, 
    fontWeight: '700' 
  },
  disabled: { opacity: 0.5 },
  logSection: {
    flex: 1,
  },
  logTitle: { 
    fontSize: 18, 
    fontWeight: '700', 
    marginBottom: 12,
    color: '#333'
  },
  logBox: { 
    flex: 1, 
    backgroundColor: Theme?.colors?.terminal || '#1e1e1e', 
    borderRadius: 16, 
    padding: 18,
    borderWidth: 1,
    borderColor: '#333'
  },
  logText: { 
    color: Theme?.colors?.terminalText || '#00ff00', 
    fontFamily: 'Courier', 
    fontSize: 13,
    lineHeight: 20,
    marginBottom: 4 
  }
});
