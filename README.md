### **Jira Epic Story DownLoad Program**

---

- `서버 실행`
1) 폴더 이동 <br>
backend 폴더로 이동
2) 파이썬 버퍼링 끄기 <br>
$env:PYTHONUNBUFFERED="1"
3) 서버 실행 <br>
python -m uvicorn server:app --port 8000

- `웹뷰 실행`
1) 폴더 이동 <br>
frontend 폴더로 이동
2) 웹뷰 실행 <br>
npx.cmd expo start --web