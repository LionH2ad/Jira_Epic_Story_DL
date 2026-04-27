// 버튼 클릭 시 호출할 함수 예시
const runProject = async (projNum) => {
  setLoading(true);
  try {
    const response = await fetch(`http://localhost:8000/run/project${projNum}`);
    const result = await response.json();
    addLog(`[Project ${projNum}] ${result.message}`);
  } catch (e) {
    addLog(`오류 발생: ${e.message}`);
  } finally {
    setLoading(false);
  }
};

// UI 부분 (반복문이나 개별 버튼으로 구성)
[1, 2, 3, 4].map(num => (
  <TouchableOpacity key={num} style={styles.button} onPress={() => runProject(num)}>
    <Text style={styles.buttonText}>프로젝트 {num} 실행</Text>
  </TouchableOpacity>
))
