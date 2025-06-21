import os
import uuid
from flask import Blueprint, request, jsonify, current_app

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file part'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # 확장자 추출 
        ext = os.path.splitext(file.filename)[1]

        # 고유한 파일명 생성
        unique_filename = f"{uuid.uuid4().hex}{ext}"

        # 저장 경로 설정
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

        # 디렉터리 없으면 생성
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)

        # 파일 저장
        file.save(save_path)

        # 저장된 파일명 반환
        return jsonify({'filename': unique_filename}), 200

    return jsonify({'error': 'File upload failed'}), 500
