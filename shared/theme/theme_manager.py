import json
import os

class ThemeManager:
    """
    안드로이드의 ThemeManager와 유사한 역할:
    JSON 토큰을 로드하고 각 서비스에 맞는 스타일 명세(Spec)를 생성합니다.
    """
    _TOKEN_PATH = os.path.join(os.path.dirname(__file__), "tokens.json")
    _CACHED_TOKENS = None

    @classmethod
    def _load_tokens(cls):
        if cls._CACHED_TOKENS is None:
            with open(cls._TOKEN_PATH, "r", encoding="utf-8") as f:
                cls._CACHED_TOKENS = json.load(f)
        return cls._CACHED_TOKENS

    @classmethod
    def get_theme(cls, override_semantic=None):
        tokens = cls._load_tokens()
        palette = tokens["primitive"]
        
        # 기본 시맨틱 설정 가져오기
        theme = tokens["semantic"].copy()
        
        # 오버라이드 적용 (안드로이드의 style override)
        if override_semantic:
            theme.update(override_semantic)

        # 색상 별칭을 실제 HEX 코드로 변환
        for key, val in theme.items():
            theme[key] = palette.get(val, val)

        return {
            "styles": theme,
            "rules": tokens["column_rules"]
        }
