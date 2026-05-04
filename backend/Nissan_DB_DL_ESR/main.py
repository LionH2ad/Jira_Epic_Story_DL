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

from shared.theme.theme_manager import ThemeManager
from backend.common.excel_style import apply_excel_style

def main():
    # [디자인] REU 전용 테마 설정 (기본 남색 대신 주황색 사용)
    # reu_override = {"header_bg": "reu_orange"}
    # theme = ThemeManager.get_theme(override_semantic=reu_override)
    theme = ThemeManager.get_theme()

    print("--- ESR Process Start ---")
    JiraConfig.setup_terminal() # 터미널 환경 설정
    
    print("Downloading Jira data...")

    target_jql = JiraConfig.get_jql("ESR") # 1. ESR 전용 JQL 가져오기
    raw_data = fetch_issues(target_jql) # 2. 데이터 가져오기
    
    # 3. 가공 및 저장
    if not raw_data:
        print("Data download failed...")

    # [가공] 데이터 가공 및 엑셀 저장 (D 드라이브)
    # 이 안에서 저장된 파일 경로를 반환한다고 가정합니다.
    file_path, sheet_names = process_and_save(raw_data)
    
    # [스타일] 저장된 엑셀에 테마 주입
    if file_path:
        print(f"Saving...")
        apply_excel_style(file_path, sheet_names, theme)
        print(f"file: {file_path}")
        print("--- ESR Process Done ---")
    else:
        print(f"Save Failed")

if __name__ == "__main__":
    main()
