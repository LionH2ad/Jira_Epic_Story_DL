import os
import urllib3
import sys
import io
from dotenv import load_dotenv

# 현재 파일(config.py) 기준: common(1) -> backend(2) -> NISSAN_CDC(3)
# 따라서 2단계 상위 폴더의 .env를 찾습니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class JiraConfig:
    URL = "https://spaws.jp.nissan.biz/jira"
    USER = "LGEJ-LGEJ1028"
    TOKEN = os.getenv("MY_TOKEN")
    PAGE_SIZE = 1000 # 한 번에 가져올 단위 (보통 500~1000이 안정적입니다)

    # 프록시 및 경고 끄기
    os.environ["NO_PROXY"] = "nissan.biz"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @staticmethod
    def get_jql(service_type):
        """service_type(ESR, REU 등)에 맞는 JQL 반환"""
        return os.getenv(f"JQL_{service_type}")

    @staticmethod
    def setup_terminal():
        # 표준 출력을 UTF-8로 강제 설정하여 한글 깨짐 방지
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(
                sys.stdout.detach(), 
                encoding="utf-8", 
                line_buffering=True  # 줄 단위로 즉시 출력
            )
        if sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(
                sys.stderr.detach(), 
                encoding="utf-8", 
                line_buffering=True
            )

    BASE_SAVE_PATH = "D:/NISSAN_JIRA_DATA"

    @staticmethod
    def get_excel_path(service_name):
        """서비스명을 받아 D 드라이브 내 최종 저장 경로를 반환"""
        excel_dir = os.path.join(JiraConfig.BASE_SAVE_PATH, service_name)
        try:
            os.makedirs(excel_dir, exist_ok=True)
        except Exception:
            # D 드라이브 실패 시 대안 경로 (프로젝트 루트/Excel)
            excel_dir = os.path.join(os.getcwd(), "Excel")
            os.makedirs(excel_dir, exist_ok=True)
        return excel_dir
