import pandas as pd
import json
import os
import re
from datetime import datetime
from constants import JiraFields

def get_value(field_data):
    """데이터가 없으면 공백 한 칸(" ")을 반환하는 함수"""
    if field_data is None: return " "

    # 딕셔너리 형태(선택 목록 등)인 경우 'value' 추출
    if isinstance(field_data, dict):
        val = field_data.get("value")
        return val if val else " "

    # 일반 문자열이나 숫자인데 비어있는 경우 체크
    val_str = str(field_data).strip()
    return field_data if val_str else " "

def clean_text(text):
    """엑셀 저장 시 오류를 일으키는 제어 문자를 제거하는 함수"""
    if not isinstance(text, str):
        return text
    # ASCII 0-31번 사이의 제어 문자 중 탭(\t), 줄바꿈(\n, \r)을 제외한 나머지를 제거
    # 엑셀 IllegalCharacterError 방지용 정규식
    illegal_xml_chars = re.compile(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f\ud800-\udfff\ufdd0-\ufdef\ufffe\uffff]"
    )
    return illegal_xml_chars.sub("", text)

def get_list_values(field_data):
    """리스트 형태의 필드 데이터를 쉼표로 구분된 문자열로 변환 (없으면 공백 한 칸)"""
    if not field_data: return " "
    if isinstance(field_data, list):
        # 리스트 내 항목이 딕셔너리일 경우 'value' 추출, 문자열이면 그대로 사용
        items = []
        for item in field_data:
            if isinstance(item, dict):
                items.append(item.get("value") or item.get("name") or str(item))
            else:
                items.append(str(item))
        # 항목들을 쉼표와 공백으로 연결 (예: "CRQ, D4_IntelligentE, ...")
        result = ", ".join(items)
        return result if result.strip() else " "    
    # 리스트가 아닌 단일 값일 경우 기존 로직 활용
    return get_value(field_data)

# 2. 통합 데이터 추출 로직 (이슈 하나당 모든 정보를 raw 딕셔너리로 반환)
def extract_issue_data(issue):
    fields = issue.get("fields", {})
    links = fields.get('issuelinks', [])
    # 담당자(Assignee) 정보는 별도 처리
    assignee = fields.get('assignee') or {}

    # Issue ID 숫자 변환 (값이 없으면 None으로 두어 엑셀 빈칸 처리)
    raw_id = issue.get("id")
    try:
        issue_id_num = int(raw_id) if raw_id else None
    except:
        issue_id_num = None

    # 특정 링크(parent/child) 데이터 추출
    outward_keys = []
    inward_keys = []
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
        #"Assignee Name": assignee.get("displayName", "Unassigned"),
        "Assignee_Email": get_value(fields.get(JiraFields.ASSIGNEE_EMAIL)),
        "CRQ_No": get_value(fields.get(JiraFields.CRQ_NO)),
        "Parent_Jira": " ".join(inward_keys),
        "Child_Jira": " ".join(outward_keys),
        "Count_Parent": len(inward_keys),
        "Count_Child": len(outward_keys),
        "Labels_Raw": raw_labels,  # 필터링용 리스트
        "Labels_Str": get_list_values(raw_labels), # 표시용 문자열
        "Executive_Summary": get_value(fields.get(JiraFields.EXECUTIVE_SUMMARY)),
        #"Created": fields.get("created"),
        #"Spec Update Reason": get_value(fields.get(JiraFields.SPEC_UPDATE_REASON)),
    }

# 3. 메인 저장 프로세스
def process_and_save(data):
    if not data or "issues" not in data:
        print("가공할 데이터가 없습니다.")
        return
    
    # 폴더 및 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__)) 
    excel_dir = os.path.join(current_dir, "Excel") # 저장 폴더 절대 경로 설정
    os.makedirs(excel_dir, exist_ok=True) # 폴더 없으면 자동으로 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file_path = os.path.join(excel_dir, f"jira_export_{timestamp}.xlsx")

    # Json 폴더에 로그 저장
    json_dir = os.path.join(current_dir, "Json")
    os.makedirs(json_dir, exist_ok=True)
    json_file_path = os.path.join(json_dir, f"log_{timestamp}.json")
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"로그 저장 완료: {json_file_path}")

    # 탭별 조합(Combination) 리스트
    total_tap = [] # 첫 번째 탭: 전체 항목

    for issue in data["issues"]:
        # 1단계: 모든 정보가 포함된 raw 데이터 추출
        raw = extract_issue_data(issue)
        
        # 2단계 
        # 첫 번째 탭용 항목 조합 (기존 항목 전부)
        total_tap.append({
            "Key": raw["Key"],
            "Issue id": raw["Issue_id"],
            "Supplier": raw["Supplier"],
            "Type": raw["Type"],
            "Status": raw["Status"],
            "Domain": raw["Domain"], # Function Dmain
            "Summary": raw["Summary"],
            "Design": raw["Design"],
            "Implement": raw["Implement"],
            "Verification": raw["Verification"],
            "Validation": raw["Validation"],
            "Source of Doc": raw["Source_of_Doc"],
            "Assignee": raw["Assignee"],
            "Assignee Email": raw["Assignee_Email"],
            "CRQ No.": raw["CRQ_No"],
            "Parent Jira": raw["Parent_Jira"],
            "Child Jira": raw["Child_Jira"],
            "Count Parent Jira": raw["Count_Parent"],
            "Count Child Jira": raw["Count_Child"]
        })

    # 3단계: 멀티 탭 엑셀 저장
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        # Sheet1: 전체 데이터
        pd.DataFrame(total_tap).to_excel(writer, sheet_name='Total_Issues', index=False)

    print(f"성공! 파일 생성됨: {excel_file_path}")
