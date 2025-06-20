from flask import Flask
from flask_cors import CORS

# 라우트 파일 import
from routes.upload_route import upload_bp
from routes.analyze_route import analyze_bp
from routes.guide_route import guide_bp

app = Flask(__name__)

# 업로드 파일 저장 경로 설정
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 프론트엔드와 연동 위한 CORS 허용
CORS(app)

# 블루프린트 등록 (라우트 연결)
app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(analyze_bp, url_prefix='/analyze')
app.register_blueprint(guide_bp, url_prefix='/guide')

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
