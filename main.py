from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"테스트": "FastAPI 서버 작동 중"}
