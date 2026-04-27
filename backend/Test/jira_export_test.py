import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import urllib3
import os

# --- [설정 구간: 본인의 정보로 수정하세요] ---
# 1. 주소 확인: 브라우저 주소창에서 /browse/ 앞부분까지만 입력 (예: https://nissan.biz)
JIRA_URL = "https://spaws.jp.nissan.biz" # "https://nissan.biz" 

# 2. 인증 정보: 이메일 대신 '사내 ID'를 넣어야 할 수도 있습니다.
USER_EMAIL = "LGEJ-LGEJ1028" 

# 3. 토큰 또는 비번: Personal Access Token이 없다면 실제 로그인 비밀번호를 입력하세요.
API_TOKEN = "XfqfORtVR0asqJ7iWpB65EW8JuNknPl6TpYOkl"

# 4. 추출 조건: JQL (Jira Query Language)
JQL_QUERY = "project = CDCFM AND type in (Epic, Story) AND created > 2026-03-06 ORDER BY id ASC" 

# 5. 한 번에 가져올 개수 (최대 100~1000)
MAX_RESULTS = 50

# 사내 프록시 우회 설정 (필요 시 주소 도메인 추가)
os.environ['NO_PROXY'] = 'nissan.biz'
# SSL 인증서 경고 메시지 출력 안 함
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# ------------------------------------------

def get_jira_issues():
    # 서버 버전(Data Center)은 rest/api/2 를 사용합니다.
    url = f"{JIRA_URL}/rest/api/2/search"
    
    auth = HTTPBasicAuth(USER_EMAIL, API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    params = {
        'jql': JQL_QUERY,
        'maxResults': MAX_RESULTS,
        # 필요한 필드들을 추가하세요 (예: description, duedate 등)
        'fields': 'summary,status,assignee,created,priority,issuetype'
    }

    try:
        print(f"연결 시도 중: {url}")
        response = requests.get(
            url, 
            headers=headers, 
            auth=auth, 
            params=params, 
            verify=False,  # 사내 보안 인증서 검증 생략 (10054 에러 해결책)
            timeout=30     # 30초 동안 응답 없으면 종료
        )

        if response.status_code == 200:
            data = response.json()
            issues = data.get('issues', [])
            
            if not issues:
                print("조회된 티켓이 없습니다. JQL 조건을 확인하세요.")
                return None

            issue_list = []
            for issue in issues:
                fields = issue.get('fields', {})
                item = {
                    'Key': issue.get('key'),
                    'Summary': fields.get('summary'),
                    'Status': fields.get('status', {}).get('name'),
                    'Type': fields.get('issuetype', {}).get('name'),
                    'Priority': fields.get('priority', {}).get('name') if fields.get('priority') else "None",
                    'Assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else "Unassigned",
                    'Created': fields.get('created')
                }
                issue_list.append(item)
            
            return issue_list
        else:
            print(f"실패 코드: {response.status_code}")
            print(f"상세 내용: {response.text}")
            return None

    except Exception as e:
        print(f"연결 중 오류 발생: {e}")
        return None

# 실행 및 엑셀 저장
if __name__ == "__main__":
    print("Jira 데이터를 가져오는 중입니다...")
    results = get_jira_issues()
    
    if results:
        df = pd.DataFrame(results)
        file_name = "nissan_jira_tickets.xlsx"
        # 엑셀 파일로 저장
        df.to_excel(file_name, index=False)
        print(f"\n성공! 파일이 생성되었습니다: {os.path.abspath(file_name)}")
    else:
        print("\n데이터를 가져오지 못했습니다. 설정을 다시 확인해주세요.")
