import os
import urllib3
import sys
import io


class JiraConfig:
    URL = "https://spaws.jp.nissan.biz/jira"
    USER = "LGEJ-LGEJ1028"
    TOKEN = "XfqfORtVR0asqJ7iWpB65EW8JuNknPl6TpYOkl"

    # JQL = "key = 'CDCFM-17422'"
    JQL = "project = CDCFM AND type in (Epic, Story) ORDER BY id ASC"

    # 한 번에 가져올 단위 (보통 500~1000이 안정적입니다)
    PAGE_SIZE = 1000

    # 시스템 설정
    os.environ["NO_PROXY"] = "nissan.biz"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @staticmethod
    def setup_terminal():
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
