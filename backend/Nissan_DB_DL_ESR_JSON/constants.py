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

    # API 요청을 위한 필드 리스트 생성 (문자열로 합침)
    FETCH_FIELDS = [
        "summary", "status", "issuetype", "assignee", "created", "priority",
        "issuelinks", "attachment", "comment",
        SUPPLIER, DOMAIN, DESIGN, IMPLEMENT, VERIFICATION, 
        VALIDATION, SOURCE_OF_DOC, ASSIGNEE_EMAIL, CRQ_NO, 
        SPEC_UPDATE_REASON, LABELS, EXECUTIVE_SUMMARY
    ]
    
    @classmethod
    def get_fields_string(cls):
        return ",".join(cls.FETCH_FIELDS)
