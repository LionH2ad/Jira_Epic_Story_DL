import React from 'react';
import { View, Text, SafeAreaView, StatusBar } from 'react-native';

// 분리된 모듈 임포트
import { PROJECTS } from './src/config/projects';
import { useJiraRunner } from './src/hooks/useJiraRunner';
import { ProjectButton } from './src/components/ProjectButton';
import { LogViewer } from './src/components/LogViewer';
import { styles } from './src/styles/mainStyles';
import { Theme } from '../shared/theme/themeManager';

export default function App() {
  const { loading, logs, runProject, scrollViewRef } = useJiraRunner();

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      
      {/* Header Section */}
      <View style={styles.header}>
        <Text style={styles.title}>NISSAN CDC</Text>
        <Text style={styles.subtitle}>Automation System Console</Text>
      </View>
      
      {/* Project Selection */}
      <View style={styles.buttonGrid}>
        {PROJECTS.map((proj) => (
          <ProjectButton 
            key={proj.id}
            name={proj.name}
            loading={loading && logs.length > 0} // 현재 실행중인 경우만 로딩 표시
            onPress={() => runProject(proj.endpoint, proj.name)}
            styles={styles}
          />
        ))}
      </View>

      {/* Log Section */}
      <View style={styles.logSection}>
        <Text style={styles.logTitle}>Live Console Logs</Text>
        <LogViewer 
          logs={logs} 
          scrollViewRef={scrollViewRef} 
          styles={styles} 
        />
      </View>
    </SafeAreaView>
  );
}
