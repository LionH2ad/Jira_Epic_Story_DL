import React from 'react';
import { View, Text, ScrollView } from 'react-native';

export const LogViewer = ({ logs, scrollViewRef, styles }) => (
  <View style={styles.logBox}>
    <ScrollView 
      ref={scrollViewRef}
      onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
    >
      {logs.length > 0 ? (
        logs.map((log, i) => (
          <Text key={i} style={styles.logText}>
            {log.includes('❌') ? <Text style={{color: '#ff4d4d'}}>{log}</Text> : log}
          </Text>
        ))
      ) : (
        <Text style={[styles.logText, { opacity: 0.3 }]}>대기 중...</Text>
      )}
    </ScrollView>
  </View>
);
