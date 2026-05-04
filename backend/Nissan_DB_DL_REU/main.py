import sys
import os

CURRENT_SERVICE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if CURRENT_SERVICE_DIR not in sys.path:
    sys.path.insert(0, CURRENT_SERVICE_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.common.config import JiraConfig
from backend.common.jira_client import fetch_issues
from services.data_processor import process_and_save

def main():
    print("--- REU Process Start ---")
    JiraConfig.setup_terminal() # 터미널 환경 설정
    
    print("작업 시작: Jira 데이터를 가져오는 중...")

    target_jql = JiraConfig.get_jql("ESR") # 1. ESR 전용 JQL 가져오기
    raw_data = fetch_issues(target_jql) # 2. 데이터 가져오기
    
    # 3. 가공 및 저장
    if raw_data:
        process_and_save(raw_data)
        print("ESR 작업 완료")
    else:
        print("데이터를 가져오지 못했습니다.")

if __name__ == "__main__":
    main()

