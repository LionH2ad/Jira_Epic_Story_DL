from jira_client import fetch_issues
from data_processor import process_and_save
try:
    from config import JiraConfig
except ImportError:
    from .config import JiraConfig # 점(.)을 찍어 현재 패키지 내에서 찾음

def main():
    print("Start Main()")
    # 터미널 환경 설정
    JiraConfig.setup_terminal()
    
    print("작업 시작: Jira 데이터를 가져오는 중...")
    
    # 1. 데이터 가져오기
    raw_data = fetch_issues()
    
    # 2. 가공 및 저장
    if raw_data:
        process_and_save(raw_data)
        print("모든 작업이 완료되었습니다.")
    else:
        print("데이터를 가져오지 못해 작업을 중단합니다.")

if __name__ == "__main__":
    main()
