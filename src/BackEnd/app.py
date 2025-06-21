# BackEnd/app.py

import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS

# VLM(비전) 모델 분류 함수
from vlm_service import predict_image
# LLM 서비스 함수
from llm_service import get_guidance_for_category

app = Flask(__name__)
CORS(app)  # http://127.0.0.1:5500 에서 오는 요청 허용

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # 1) 파일 검사
        if 'image' not in request.files:
            return jsonify(error='이미지 파일을 찾을 수 없습니다.'), 400
        img = request.files['image']

        # 2) FileStorage → 임시 파일로 저장
        #    (predict_image는 경로(str)를 받도록 작성된 경우)
        suffix = os.path.splitext(img.filename)[1] or ''
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            temp_path = tmp.name
            img.save(temp_path)

        # 3) VLM 모델로 분류 (경로 전달)
        category = predict_image(temp_path)

        # 4) 임시 파일 삭제
        try:
            os.remove(temp_path)
        except OSError:
            app.logger.warning(f"임시 파일 삭제 실패: {temp_path}")

        # 5) LLM 서비스로 가이드 생성
        guidance = get_guidance_for_category(category)

        # 6) 결과 반환
        return jsonify({
            'category': category,
            'guidance': guidance
        }), 200

    except Exception as e:
        app.logger.error("🔥 업로드 처리 중 예외 발생", exc_info=True)
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    # debug=True 로 실행하면 에러가 터미널과 브라우저에 자세히 표시됩니다.
    app.run(host='0.0.0.0', port=8000)
