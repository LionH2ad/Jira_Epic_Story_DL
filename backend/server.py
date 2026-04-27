import sys
import os
import subprocess
import asyncio
from concurrent.futures import ThreadPoolExecutor # 스레드 관리를 위한 라이브러리
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import traceback # 에러 추적용

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4) # 스레드 실행을 위한 전용 풀 생성

# 앱과의 통신 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 프로젝트별로 독립된 main()을 호출하는 함수
def run_script_with_live_logs(folder_name):
    """
    각 폴더의 main.py를 독립된 프로세스로 실행하고
    터미널에 로그를 즉시(flush) 출력합니다.
    """
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(backend_dir, folder_name)
    main_file = os.path.join(project_dir, "main.py")

    print(f"\n[{folder_name}] 작업을 시작합니다...", flush=True)

    # subprocess.Popen을 사용해 터미널 명령어를 실행하는 것과 동일한 효과
    # -u 옵션은 파이썬 로그가 쌓이지 않고 바로 나오게 합니다.
    process = subprocess.Popen(
        [sys.executable, "-u", main_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=project_dir, # 해당 프로젝트 폴더 안에서 실행 (중요)
        bufsize=1,
        encoding='utf-8',
        errors='replace'
    )

    # 로그를 한 줄씩 읽어서 실시간으로 서버 터미널에 출력
    if process.stdout:
        for line in process.stdout:
            print(f"[{folder_name}] {line.strip()}", flush=True)

    process.wait()
    return process.returncode

@app.get("/")
def read_root():
    return {"message": "Nissan CDC Backend Server is Running!"}
    
@app.get("/run/Nissan_DB_DL_ESR")
async def run_p1(): # async 추가
    print("Nissan_DB_DL_ESR 실행 시작...")
    # Nissan_DB_DL_ESR의 main.py 안에 있는 실행 함수를 호출
    loop = asyncio.get_event_loop()
    try:
        # 개별 스레드에서 main 실행
        result = await loop.run_in_executor(executor, run_script_with_live_logs, "Nissan_DB_DL_ESR")
        print(f"Nissan_DB_DL_ESR 완료: {result}")
        return {"status": "success", "message": "Jira 수집 및 엑셀 저장 완료", "data": str(result)}
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        return {"status": "error", "message": str(e)}
    
@app.get("/run/Nissan_DB_DL_REU")
async def run_p2(): # async 추가
    print("Nissan_DB_DL_REU 실행 시작...")
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(executor, run_script_with_live_logs, "Nissan_DB_DL_REU")
        print(f"Nissan_DB_DL_REU 완료: {result}")
        return {"status": "success", "message": "Jira 수집 및 엑셀 저장 완료", "data": str(result)}
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
