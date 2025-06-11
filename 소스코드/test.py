
# 플라스크 백엔드 테스트용 파이썬코드, 작성자: 박규선,작성 날짜:2025/6/11

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])

def home():
    return jsonify({
        "status": "success",
        "message": "Flask 서버 연결 성공!"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
