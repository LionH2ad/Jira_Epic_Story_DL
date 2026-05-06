import re

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

def get_value(field_data, default=" "):
    """데이터가 없으면 공백 한 칸(" ")을 반환하는 함수"""
    if field_data is None: 
        return default

    # 딕셔너리 형태(Jira 선택 목록 등)인 경우 'value' 추출
    if isinstance(field_data, dict):
        val = field_data.get("value")
        return val if val else default
    
    # 일반 문자열이나 숫자인데 비어있는 경우 체크
    val_str = str(field_data).strip()
    return field_data if val_str else default

def get_list_values(field_data, delimiter=", ", default=" "):
    """리스트 형태의 필드 데이터를 쉼표로 구분된 문자열로 변환 (없으면 공백 한 칸)"""
    if not field_data: return default
    if isinstance(field_data, list):
        # 리스트 내 항목이 딕셔너리일 경우 'value' 추출, 문자열이면 그대로 사용
        items = []
        for item in field_data:
            if isinstance(item, dict):
                # 기존 로직: value -> name -> str(item) 순서 시도
                items.append(item.get("value") or item.get("name") or str(item))
            else:
                items.append(str(item))
            # 항목들을 쉼표와 공백으로 연결 (예: "CRQ, D4_IntelligentE, ...")
        result = delimiter.join(items)
        return result if result.strip() else default
    # 리스트가 아닌 단일 값일 경우 기존 로직(get_value) 활용
    return get_value(field_data, default=default)
