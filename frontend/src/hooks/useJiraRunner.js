import { useState, useRef } from 'react';

export const useJiraRunner = () => {
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);
  const scrollViewRef = useRef(null);

  const addLog = (msg) => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, `[${time}] ${msg}`]);
  };

  const runProject = async (endpoint, name) => {
    if (loading) return;
    setLoading(true);
    setLogs([]);
    addLog(`${name} 실행 요청 중...`);

    try {
      const response = await fetch(`http://localhost:8000/run/${endpoint}`);
      if (!response.ok) throw new Error(`서버 에러 (${response.status})`);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        chunk.split('\n').forEach(line => {
          if (line.startsWith('data: ')) {
            const message = line.replace('data: ', '').trim();
            if (message) addLog(message);
          }
        });
      }
    } catch (error) {
      addLog(`❌ 오류: ${error.message}`);
    } finally {
      setLoading(false);
      addLog(`🏁 프로세스 종료`);
    }
  };

  return { loading, logs, runProject, scrollViewRef };
};
