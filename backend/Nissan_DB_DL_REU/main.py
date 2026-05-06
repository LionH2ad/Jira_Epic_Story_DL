import os

from shared.theme.theme_manager import ThemeManager
from backend.common.config import JiraConfig
from backend.common.jira_client import fetch_issues
from backend.common.excel_style import apply_excel_style
from backend.Nissan_DB_DL_REU.services.data_processor import process_and_save
def main():
    print("--- REU Process Start ---")

    SERVICE_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    # 1. 디자인(테마) 로드
    theme = ThemeManager.get_theme()

    # 2. 터미널 UTF-8 및 시스템 초기화
    JiraConfig.setup_terminal()
    
    print("Downloading Jira data...")

    target_jql = JiraConfig.get_jql("REU") # 1. ESR 전용 JQL 가져오기
    raw_data = fetch_issues(target_jql) # 2. 데이터 가져오기
    
    # 3. 가공 및 저장
    if not raw_data:
        print("Data download failed...")
        return

    # 4. 데이터 가공 및 저장 (파일 경로와 시트명 리스트 반환)
    file_path, sheet_names = process_and_save(raw_data, SERVICE_NAME)
    
    # [스타일] 저장된 엑셀에 테마 주입
    if file_path:
        print(f"Saving...")
        apply_excel_style(file_path, sheet_names, theme)
        print(f"File saved successfully")
        print(f"file: {file_path}")
        print("--- REU Process Done ---")
    else:
        print(f"Save Failed")

if __name__ == "__main__":
    main()

