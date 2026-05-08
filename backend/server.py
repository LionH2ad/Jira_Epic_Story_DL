import sys
import os
import subprocess
import asyncio
from concurrent.futures import ThreadPoolExecutor # 스레드 관리를 위한 라이브러리
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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
    각 폴더의 main.py를 직접 실행하는 대신, 
    루트의 run.py를 통해 서비스를 실행하여 경로 문제를 해결합니다.
    """
    # 1. 프로젝트 루트 경로 계산 (backend 폴더의 상위)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(backend_dir) # NISSAN_CDC 루트

    # 2. 실행할 run.py의 절대 경로
    run_py = os.path.join(root_dir, "run.py")

    print(f"\n[{folder_name}] 작업을 시작합니다...", flush=True)

    # - main_file 대신 run_py를 실행합니다.
    # - 인자로 folder_name(서비스명)을 전달합니다.
    # - cwd를 root_dir로 설정하여 run.py가 shared를 찾게 합니다.
    process = subprocess.Popen(
        [sys.executable, "-u", run_py, folder_name], # run.py 실행 + 서비스명 전달
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=root_dir,  # <--- 매우 중요: 프로젝트 루트에서 실행
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

async def run_live_generator(folder_name):
    # 1. 경로 설정
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(backend_dir)
    run_py = os.path.join(root_dir, "run.py")

    # 2. 환경변수 설정 (버퍼링 강제 제거)
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    # 3. 프로세스 실행 (바이트 모드로 유지하여 인코딩 문제 방지)
    process = subprocess.Popen(
        [sys.executable, "-u", run_py, folder_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=False,
        cwd=root_dir,
        env=env
    )

    yield f"data: [{folder_name}] 프로세스 연결 성공\n\n"

    # 4. 실시간 로그 읽기
    while True:
        line = process.stdout.readline()
        if not line:
            if process.poll() is not None: break
            await asyncio.sleep(0.1)
            continue
            
        # 인코딩 방어 처리 (UTF-8 -> CP949)
        try:
            decoded = line.decode('utf-8').strip()
        except:
            decoded = line.decode('cp949', errors='replace').strip()
        
        if decoded:
            yield f"data: {decoded}\n\n"
            await asyncio.sleep(0.01) # UI 갱신을 위한 미세 지연

    process.wait()
    yield f"data: [{folder_name}] 작업이 완료되었습니다.\n\n"

@app.get("/run/{folder_name}")
async def run_service(folder_name: str):
    # StreamingResponse를 사용하여 실시간으로 로그를 쏨
    return StreamingResponse(run_live_generator(folder_name), media_type="text/event-stream")

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
