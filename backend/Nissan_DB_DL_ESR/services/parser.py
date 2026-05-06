from backend.common.constants import JiraFields
from backend.common.utils.text_utils import get_value, get_list_values, clean_text

def parse_issue_info(issue):
    """Jira issue(JSON)에서 정제된 issue_info(Dict)를 추출합니다."""
    fields = issue.get("fields", {})
    links = fields.get('issuelinks', [])
    assignee = fields.get('assignee') or {}

    # Issue ID 숫자 변환 (값이 없으면 None으로 두어 엑셀 빈칸 처리)
    raw_id = issue.get("id")
    try:
        issue_id_num = int(raw_id) if raw_id else None
    except:
        issue_id_num = None

    # 특정 링크(parent/child) 데이터 추출
    outward_keys, inward_keys = [], []
    for link in links:
        # 링크 타입 이름 확인 (대소문자 구분 없이 체크하려면 .lower() 사용)
        link_type_name = link.get('type', {}).get('name', "")
        if link_type_name == "parent/child":
            # Outward 이슈 키 추출
            if 'outwardIssue' in link:
                out_key = link.get('outwardIssue', {}).get('key')
                if out_key: outward_keys.append(out_key)
            # Inward 이슈 키 추출
            if 'inwardIssue' in link:
                in_key = link.get('inwardIssue', {}).get('key')
                if in_key: inward_keys.append(in_key)

    # 1. 키 목록 문자열: 리스트에 값이 있으면 공백으로 합치고, 없으면 공백 한 칸(" ")
    outward_str = " ".join(outward_keys) if outward_keys else " "
    inward_str = " ".join(inward_keys) if inward_keys else " "

    # [핵심 수정] Labels 데이터가 None(null)인 경우 빈 리스트([])로 강제 치환
    raw_labels = fields.get(JiraFields.LABELS)
    if not isinstance(raw_labels, list):
        raw_labels = []

    # 모든 가공된 결과물을 하나의 주머니(dict)에 담기
    return {
        "Key": issue.get("key"),
        "Issue_id": issue_id_num,
        "Supplier": get_value(fields.get(JiraFields.SUPPLIER)),
        "Type": fields.get("issuetype", {}).get("name"),
        "Status": fields.get("status", {}).get("name"),
        "Domain": get_value(fields.get(JiraFields.DOMAIN)),
        "Summary": fields.get('summary'),
        "Design": get_value(fields.get(JiraFields.DESIGN)),
        "Implement": get_value(fields.get(JiraFields.IMPLEMENT)),
        "Verification": get_value(fields.get(JiraFields.VERIFICATION)),
        "Validation": get_value(fields.get(JiraFields.VALIDATION)),
        "Source_of_Doc": clean_text(get_value(fields.get(JiraFields.SOURCE_OF_DOC))),
        "Assignee": assignee.get("name", ""),
        "Assignee_Email": get_value(fields.get(JiraFields.ASSIGNEE_EMAIL)),
        "CRQ_No": get_value(fields.get(JiraFields.CRQ_NO)),
        "Parent_Jira": inward_str,
        "Child_Jira": outward_str,
        "Count_Parent": len(inward_keys),
        "Count_Child": len(outward_keys),
        "Labels_Raw": raw_labels,  # 필터링용 리스트
        "Labels_Str": get_list_values(raw_labels), # 표시용 문자열
        "Executive_Summary": get_value(fields.get(JiraFields.EXECUTIVE_SUMMARY)),
    }
