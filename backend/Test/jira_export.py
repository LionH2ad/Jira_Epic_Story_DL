import requests
import json  # 로그 출력을 위해 반드시 필요함!
import pandas as pd
from requests.auth import HTTPBasicAuth
from datetime import datetime
import urllib3
import sys
import io
import os

# 터미널 출력 인코딩을 UTF-8로 설정 (이모지 출력 가능하게 함)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# --- [설정 구간] ---
JIRA_URL = "https://spaws.jp.nissan.biz/jira" # "https://nissan.biz" 
USER_EMAIL = "LGEJ-LGEJ1028"
API_TOKEN = "XfqfORtVR0asqJ7iWpB65EW8JuNknPl6TpYOkl"

JQL_QUERY = "key = 'CDCFM-22853'" # "project = CDCFM AND type in (Epic, Story) AND created > 2026-03-06 ORDER BY id ASC" 
MAX_RESULTS = 1000

os.environ['NO_PROXY'] = 'nissan.biz'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# ------------------

def get_jira_issues():
    url = f"{JIRA_URL}/rest/api/2/search"
    
    auth = HTTPBasicAuth(USER_EMAIL, API_TOKEN)
    
    # [핵심 수정] User-Agent를 추가하여 브라우저인 것처럼 속입니다.
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    params = {
        'jql': JQL_QUERY,
        'maxResults': 10, # MAX_RESULTS
        'fields': '*all'
    }

    try:
        print(f"연결 시도 중: {url}")
        # auth 방식을 헤더에 직접 넣는 방식으로도 시도해볼 수 있습니다.
        response = requests.get(
            url, 
            headers=headers, 
            auth=auth, 
            params=params, 
            verify=False, 
            timeout=30
        )

        if response.status_code == 200:
            # 성공 로직 (이전과 동일)
            data = response.json()

            # --- [로그 출력 구간 시작] ---
            print("\n--- [Jira API Response JSON Log] ---")
            # indent=4 옵션을 주면 들여쓰기가 되어 보기 편하게 출력됩니다.
            print(json.dumps(data, indent=4, ensure_ascii=False))
            print("--- [End of Log] ---\n")
            # --- [로그 출력 구간 끝] ---

            # --- [로그 파일 저장 구간] ---
            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file_name = f"jira_debug_log_{now_str}.json"
    
            with open(log_file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
    
            print(f"로그가 파일로 저장되었습니다: {log_file_name}")
            # ---------------------------

            issues = data.get('issues', [])
            if not issues:
                print("조회된 티켓이 없습니다.")
                return None
            
            issue_list = []
            for issue in issues:
                fields = issue.get('fields', {})
                issue_list.append({
                    'Key': issue.get('key'),
                    'Issue id': issue.get('id'),
                    'Supplier': fields.get('customfield_13114', {}).get('value'),
                    'Type': fields.get('issuetype', {}).get('name'),
                    'Status': fields.get('status', {}).get('name'),
                    'Domain': fields.get('customfield_12788', {}).get('value'),                    
                    'Summary': fields.get('summary'),
                    'Design': fields.get('customfield_13106', {}).get('value'),
                    'Implement': fields.get('customfield_13108', {}).get('value'),
                    'Verification': fields.get('customfield_13110', {}).get('value'),
                    'Validation': fields.get('customfield_13112', {}).get('value'),
                    'Source of Doc': fields.get('customfield_12539'),
                    'Assignee': fields.get('assignee', {}).get('name'),
                    'Assignee': fields.get('assignee', {}).get('emailAddress'),
                    # 'Assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else "Unassigned",
                    'Created': fields.get('created')
                })
            return issue_list
        
        elif response.status_code == 403:
            print(f"에러 403: 접근이 거부되었습니다. (ID/PW 또는 권한 문제)")
            print("팁: 주소 뒤에 /jira를 붙여보거나(https://nissan.biz), ID/PW가 정확한지 확인하세요.")
            return None
        else:
            print(f"실패 코드: {response.status_code}")
            return None

    except Exception as e:
        print(f"오류 발생: {e}")
        return None

if __name__ == "__main__":
    results = get_jira_issues()

    if results:
        df = pd.DataFrame(results)

        # 현재 날짜와 시간 가져오기 (예: 20260402_153025)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"nissan_jira_export_{now}.xlsx"

        df.to_excel(file_name, index=False)
        print(f"성공! 파일이 생성되었습니다: {file_name}")
