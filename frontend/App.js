import React, { useState } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ScrollView, ActivityIndicator } from 'react-native';

export default function App() {
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);

  // 1. 프로젝트 리스트 정의 (이름과 서버 주소를 매칭)
  const projects = [
    { id: 1, name: "DB/DL (ESR)", endpoint: "Nissan_DB_DL_ESR" },
    { id: 2, name: "DB/DL (REU)", endpoint: "Nissan_DB_DL_REU" },
    { id: 3, name: "프로젝트 3", endpoint: "Project_3_Name" },
    { id: 4, name: "프로젝트 4", endpoint: "Project_4_Name" },
  ];

  const addLog = (msg) => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [`[${time}] ${msg}`, ...prev]);
  };

  const runProject = async (endpoint, name) => {
    setLoading(true);
    addLog(`${name} 실행 요청 중...`);
    try {
      // 엔드포인트 이름을 주소에 그대로 사용
      const response = await fetch(`http://localhost:8000/run/${endpoint}`);
      
      if (response.status === 404) {
        throw new Error("서버에서 해당 경로를 찾을 수 없습니다 (404).");
      }

      const result = await response.json();
      addLog(`결과: ${result.message}`);
    } catch (error) {
      addLog(`오류: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Nissan CDC Automation</Text>
      
      <View style={styles.buttonGrid}>
        {/* 3. 정의한 리스트로 버튼 생성 */}
        {projects.map((proj) => (
          <TouchableOpacity 
            key={proj.id} 
            style={[styles.button, loading && styles.disabled]} 
            onPress={() => runProject(proj.endpoint, proj.name)}
            disabled={loading}
          >
            <Text style={styles.buttonText}>{proj.name} 실행</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.logTitle}>실시간 로그</Text>
      <ScrollView style={styles.logBox}>
        {logs.map((log, i) => <Text key={i} style={styles.logText}>{log}</Text>)}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 40, backgroundColor: '#f0f2f5' },
  title: { fontSize: 28, fontWeight: 'bold', marginBottom: 30, textAlign: 'center' },
  buttonGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', marginBottom: 30 },
  button: { backgroundColor: '#0052cc', width: '48%', padding: 20, borderRadius: 10, marginBottom: 15, alignItems: 'center' },
  disabled: { backgroundColor: '#a0a0a0' },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  logTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
  logBox: { flex: 1, backgroundColor: '#1e1e1e', borderRadius: 10, padding: 15 },
  logText: { color: '#00ff00', fontFamily: 'monospace', marginBottom: 5 }
});
