import requests
from requests.auth import HTTPBasicAuth
from common.config import JiraConfig
from common.constants import JiraFields


def fetch_issues(jql):
    search_url = f"{JiraConfig.URL}/rest/api/2/search"
    auth = HTTPBasicAuth(JiraConfig.USER, JiraConfig.TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    all_issues = []
    start_at = 0
    # page_size = 1000  # 한 번에 가져올 단위

    while True:
        params = {
            "jql": jql,
            "startAt": start_at,  # 시작 위치 지절
            "maxResults": JiraConfig.PAGE_SIZE,
            "fields": JiraFields.get_fields_string(),
            # "fields": "*all",
        }

        print(f"데이터 가져오는 중... ({start_at}번부터 시작)")

        try:
            response = requests.get(
                search_url,
                headers=headers,
                auth=auth,
                params=params,
                verify=False,
                timeout=60,
            )

            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                break

            response.raise_for_status()

            data = response.json()
            issues = data.get("issues", [])
            all_issues.extend(issues)

            total = data.get("total", 0)
            print(f"현재 누적: {len(all_issues)} / 전체: {total}")

            # 더 이상 가져올 데이터가 없으면 종료
            if len(all_issues) >= total or len(issues) == 0:
                break

            start_at += len(issues)

        except Exception as e:
            print(f"데이터 취득 중 오류 발생: {e}")
            break

    return {"issues": all_issues}
