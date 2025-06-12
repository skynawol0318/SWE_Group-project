from flask import Flask

app = Flask(__name__)  # Flask 앱 생성

@app.route('/')  # 루트 경로 (홈페이지)
def hello():
    return '백엔드 테스트중.....'

if __name__ == '__main__':
    app.run(debug=True)  # 개발자 모드로 실행
