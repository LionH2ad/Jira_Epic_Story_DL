import re
from backend.common.constants import JiraFields
from backend.common.utils.text_utils import get_value, clean_text

def parse_issue_info(issue):
    """Jira issue(JSON)에서 정제된 issue_info(Dict)를 추출합니다."""
    fields = issue.get("fields", {})
    assignee = fields.get('assignee') or {}

    # Issue ID 숫자 변환 (값이 없으면 None으로 두어 엑셀 빈칸 처리)
    raw_id = issue.get("id")
    try:
        issue_id_num = int(raw_id) if raw_id else None
    except:
        issue_id_num = None

    # 첨부파일에서 .dbc 파일 찾기
    attachments = fields.get("attachment", [])
    dbc_filenames = []
    for att in attachments:
        filename = att.get("filename", "")
        if filename.lower().endswith(".dbc"):
            # 확장자 .dbc를 제거한 파일명 추출
            clean_name = filename[:-4] if filename.lower().endswith(".dbc") else filename
            dbc_filenames.append(clean_name)
    
    # [신규] AASP 관련 파일명 추출 로직
    attachments = fields.get("attachment", [])
    comments = fields.get("comment", {}).get("comments", [])

    # 추출된 파일명들을 담을 리스트
    extracted_items = []

    for att in attachments:
        filename = att.get("filename", "")
        if "AASP" in filename.upper():
            clean_name = filename.split('|')[0].split('?')[0].strip()

            if '.xlsx' in clean_name.lower():
                clean_name = clean_name.lower().split('.xlsx')[0]

            clean_name = clean_name.replace(']', '').strip()
            
            if clean_name:
                extracted_items.append(clean_name)
            
    # 2. 댓글에서 찾기 (댓글 텍스트 내에 언급된 파일명이 있다면 수집)
    # (SWD-|QA_) : SWD- 또는 QA_ 로 시작함
    # [^\s,]+ : 그 뒤에 공백이나 쉼표가 아닌 문자들이 붙음
    multi_pattern = r"(?:SWD-|QA_)[^\s,]+"
    for cmt in comments:
        body = cmt.get("body", "")
        if "AASP" in body.upper():
            found = re.findall(multi_pattern, body)
            if found:
                for item in found:
                    # 정규표현식으로 1차 필터링을 했지만, 
                    # 혹시 모를 잔여물(|나 ])을 한 번 더 제거합니다.
                    clean_item = item.split('|')[0].split('?')[0].replace(']', '').strip()

                    if '.xlsx' in clean_item.lower():
                        idx = clean_item.lower().find('.xlsx')
                        clean_item = clean_item[:idx]

                    if 'aasp' in clean_item.lower():
                        extracted_items.append(clean_item)

    # 중복 제거 및 정렬
    extracted_items = sorted(list(set(extracted_items)))

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
        "Executive_Summary": get_value(fields.get(JiraFields.EXECUTIVE_SUMMARY)),
        "Status": fields.get("status", {}).get("name"),
        "DBC_Files": dbc_filenames, # .dbc가 제거된 파일명 리스트
        "AASP_Combined_Items": extracted_items,
        "Comments_Raw": comments, # 댓글 원문 필요 시 대비
    }
