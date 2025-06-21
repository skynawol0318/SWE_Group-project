import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.datastructures import FileStorage
from flask.typing import ResponseReturnValue

# 이미지 업로드 라우터
upload_bp: Blueprint = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_image() -> ResponseReturnValue:
  
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400

    file: FileStorage = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    if file:
        # 파일 확장자 추출
        extension: str = os.path.splitext(file.filename)[1]

        # 고유한 파일명 생성
        unique_filename: str = f"{uuid.uuid4().hex}{extension}"

        # 저장 경로 지정
        upload_folder: str = current_app.config['UPLOAD_FOLDER']
        save_path: str = os.path.join(upload_folder, unique_filename)

        # 디렉터리 없을 경우 생성
        os.makedirs(upload_folder, exist_ok=True)

        # 파일 저장
        file.save(save_path)

        # 고유 파일명을 file_id로 반환
        return jsonify({
            'success': True,
            'data': {
                'file_id': unique_filename
            }
        }), 200

    return jsonify({'success': False, 'error': 'File upload failed'}), 500
