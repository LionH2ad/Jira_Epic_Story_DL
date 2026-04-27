# constants.py

class JiraFields:
    # 커스텀 필드 ID 매핑
    SUPPLIER = "customfield_13114"
    DOMAIN = "customfield_12788"
    DESIGN = "customfield_13106"
    IMPLEMENT = "customfield_13108"
    VERIFICATION = "customfield_13110"
    VALIDATION = "customfield_13112"
    SOURCE_OF_DOC = "customfield_12539"
    ASSIGNEE_EMAIL = "customfield_13237"
    CRQ_NO = "customfield_10481"
    SPEC_UPDATE_REASON = "customfield_16689"
    LABELS = "customfield_12787"
    EXECUTIVE_SUMMARY = "customfield_12554"

    # 탭 2: CRQ 필터 조건
    CRQ_TARGETS = ["CRQ", "CRQ_Related"]

    # 탭 3: LGE PI 필터 대상 라벨
    PI_TARGET_LABELS = [
        "PI29_BASE", "PI30_BASE", "PI30_CarryOver", 
        "PI31_BASE", "PI31_CarryOver", "PI32_BASE", "PI32_CarryOver"
    ]

    # 탭 4: 제외할 상태(Status) 목록
    EXCLUDE_STATUS_LIST = [
        "CLOSE", "CLOSED", "Verified", "Rejected", "Close", "Closed",
        "Validation Ok", "Validation NG", "PREPARING VALIDATION ENVIRONMENT"
    ]

    # 타겟 공급사 명칭 (대소문자 실수 방지)
    TARGET_SUPPLIER = "LGE"

    # --- [엑셀 설정 상수] ---
    SHEET_TOTAL = "Total_Issues"
    SHEET_CRQ = "CRQ"
    SHEET_SECOND_SOP = "2nd_SOP"
    SHEET_EXEC = "Exec_Summary_Report"

    MAX_COL_WIDTH = 70  # 최대 열 너비 제한
    DATE_FORMAT = "%Y-%m-%d" # 날짜 출력 형식

    # API 요청을 위한 필드 리스트 생성 (문자열로 합침)
    FETCH_FIELDS = [
        "summary", "status", "issuetype", "assignee", "created", "priority",
        "issuelinks", "attachment", "comment",
        SUPPLIER, DOMAIN, DESIGN, IMPLEMENT, VERIFICATION, 
        VALIDATION, SOURCE_OF_DOC, ASSIGNEE_EMAIL, CRQ_NO, 
        SPEC_UPDATE_REASON, LABELS, EXECUTIVE_SUMMARY
    ]

    # 컬럼 이름별 지정 너비 (Key: 헤더이름, Value: 너비값)
    COLUMN_WIDTHS = {
        "Key": 12.5,
        "Issue id": 9.38,
        "Supplier": 8.5,
        "Type": 6.75,
        "Status": 9.13,
        "Domain":15.13,
        "Summary": 35.63,
        "Design": 11.0,
        "Implement": 11.0,
        "Verification": 11.0,
        "Validation": 11.0,
        "Source of Doc": 18.13,
        "Assignee": 14.25,
        "Assignee Email": 17.75,
        "CRQ No.": 12.13,
        "Parent Jira": 8.38,
        "Child Jira": 8.38,
        "Count Parent Jira": 8.38,
        "Count Child Jira": 8.38,
        "Labels": 120.0,
        "Executive Summary": 80.5,
        # 여기에 필요한 컬럼명을 계속 추가하세요.
    }
    
    DEFAULT_WIDTH = 8.38 # 목록에 없는 컬럼의 기본 너비
    
    @classmethod
    def get_fields_string(cls):
        return ",".join(cls.FETCH_FIELDS)
