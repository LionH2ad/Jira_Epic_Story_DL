import sys
import os
import importlib

# [Enterprise Pattern] 프로젝트 루트를 검색 경로 최상단에 등록
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

def start_service(service_name):
    """지정한 서비스의 main() 함수를 실행합니다."""
    # 모듈 경로 구성 (예: backend.Nissan_DB_DL_ESR.main)
    module_path = f"backend.{service_name}.main"
    
    print(f"실행 시도: {service_name}")
    
    try:
        # 동적 모듈 로드
        service_module = importlib.import_module(module_path)
        if hasattr(service_module, "main"):
            service_module.main()
        else:
            print(f"error: {module_path}에 main() 함수가 없습니다.")
    except ModuleNotFoundError as e:
        print(f"error: please check path. ({e})")
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")

if __name__ == "__main__":
    # 사용법: python run.py Nissan_DB_DL_ESR
    if len(sys.argv) > 1:
        target_service = sys.argv[1]
        start_service(target_service)
    else:
        print("사용법: python run.py [서비스_폴더명]")
        print("예시: python run.py Nissan_DB_DL_ESR")
