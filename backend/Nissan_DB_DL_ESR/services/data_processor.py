import pandas as pd
import os
from common.constants import JiraFields
from datetime import datetime
from services.parser import parse_issue_info
from services.excel_style import apply_excel_style

# 3. 메인 저장 프로세스
def process_and_save(raw_response):
    if not raw_response or "issues" not in raw_response:
        print("가공할 데이터가 없습니다.")
        return
    
    # 폴더 및 경로 설정
    service_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_dir = os.path.join(service_root_dir, "Excel") # 저장 폴더 절대 경로 설정
    os.makedirs(excel_dir, exist_ok=True) # 폴더 없으면 자동으로 생성

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file_path = os.path.join(excel_dir, f"jira_export_{timestamp}.xlsx")
    
    # 탭별 조합(Combination) 리스트
    total_issues = [] # Sheet 1: 전체 항목
    crq_tab = [] # Sheet 2: 특정 조건 항목
    second_sop_tab = [] # Sheet 3: 2nd sop
    executive_summary_tab = [] # Sheet 4: Executive Summary

    for issue in raw_response["issues"]:
        # 1단계: 모든 정보가 포함된 info 데이터 추출
        info = parse_issue_info(issue) # parse_issue_info
        
        # 2단계 
        # Sheet 1 항목
        total_issues.append({
            "Key": info["Key"],
            "Issue id": info["Issue_id"],
            "Supplier": info["Supplier"],
            "Type": info["Type"],
            "Status": info["Status"],
            "Domain": info["Domain"], # Function Dmain
            "Summary": info["Summary"],
            "Design": info["Design"],
            "Implement": info["Implement"],
            "Verification": info["Verification"],
            "Validation": info["Validation"],
            "Source of Doc": info["Source_of_Doc"],
            "Assignee": info["Assignee"],
            "Assignee Email": info["Assignee_Email"],
            "CRQ No.": info["CRQ_No"],
            "Parent Jira": info["Parent_Jira"],
            "Child Jira": info["Child_Jira"],
            "Count Parent Jira": info["Count_Parent"],
            "Count Child Jira": info["Count_Child"]
        })

        # Sheet 2 Label = "CRQ" or "CRQ_Related"
        if any(word in info["Labels_Raw"] for word in JiraFields.CRQ_TARGETS):
            crq_tab.append({
                "Key": info["Key"],
                "Issue id": info["Issue_id"],
                #"Labels": info["Labels_Str"] # 이미 문자열로 가공된 데이터 사용
            })

        # Sheet 3 (Supplier=LGE & 특정 PI Label 포함)
        # 조건 1: Supplier = "LGE"
        is_lge = str(info["Supplier"]).strip() == JiraFields.TARGET_SUPPLIER
        # 조건 2: Labels에 지정된 PI 키워드가 하나라도 있는지 확인
        has_pi_label = any(label in info["Labels_Raw"] for label in JiraFields.PI_TARGET_LABELS)

        if is_lge and has_pi_label:
            second_sop_tab.append({
                "Key": info["Key"],
                "Issue id": info["Issue_id"],
                "Type": info["Type"],
                "Status": info["Status"],
                "Verification": info["Verification"],
                "Labels": info["Labels_Str"] # 확인용으로 라벨도 포함
            })

        # Sheet 4 Executive Summary
        # 조건 1: Supplier = "LGE"
        # 조건 2: Status가 제외 목록에 포함되지 않는지 확인
        # is_active_status = info["Status"] not in JiraFields.EXCLUDE_STATUS_LIST
        is_active_status = info["Status"].strip().lower() not in [status.lower() for status in JiraFields.EXCLUDE_STATUS_LIST]
        # 조건 3: Executive Summary가 비어있지 않은지 확인 (" " 한 칸 공백은 비어있는 것으로 간주)
        exec_summary = info.get("Executive_Summary", " ")
        is_summary_not_empty = exec_summary.strip() != ""

        if is_lge and is_active_status and is_summary_not_empty:
            executive_summary_tab.append({
                "Key": info["Key"],
                "Issue id": info["Issue_id"],
                # "Type": info["Type"],
                # "Status": info["Status"],
                "Executive Summary": exec_summary
            })

    # 3단계: 멀티 탭 엑셀 저장
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        # 데이터가 있는 경우에만 시트 생성
        if total_issues:
            pd.DataFrame(total_issues).to_excel(writer, sheet_name=JiraFields.SHEET_TOTAL, index=False)

        if crq_tab:
            pd.DataFrame(crq_tab).to_excel(writer, sheet_name=JiraFields.SHEET_CRQ, index=False)

        if second_sop_tab:
            pd.DataFrame(second_sop_tab).to_excel(writer, sheet_name=JiraFields.SHEET_SECOND_SOP, index=False)

        if executive_summary_tab:
            pd.DataFrame(executive_summary_tab).to_excel(writer, sheet_name=JiraFields.SHEET_EXEC, index=False)

    # 4단계: 디자인 스타일 적용 (생성된 모든 시트 대상)
    sheet_names = writer.sheets.keys() # 실제로 생성된 시트 이름만 가져오기
    apply_excel_style(excel_file_path, list(sheet_names))
    
    print(f"성공! 멀티 탭 파일 생성됨: {excel_file_path}")
