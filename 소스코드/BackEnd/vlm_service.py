# service/vlm_service.py
import base64
import requests
import re

# 분리수거 가능한 카테고리 리스트
CATEGORIES = ["플라스틱", "종이", "캔", "유리", "일반쓰레기", "비닐"]

def predict_image(file_path: str) -> tuple[str, float, str]:
    """
    이미지 파일 경로를 받아 Ollama LLaVA 모델에 분류 요청을 보내고,
    (label, confidence, raw_response) 형태로 반환합니다.

    Returns:
        label (str): 분류된 카테고리
        confidence (float): 신뢰도 (0.0~1.0)
        raw_text (str): LLaVA 모델의 원본 응답 텍스트
    """
    # 이미지 파일을 base64로 인코딩
    with open(file_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # LLaVA API payload 구성
    payload = {
        "model": "llava",
        "prompt": (
            "너는 분리수거 분류 모델이야.\n"
            "다음 사진 속 쓰레기를 아래 목록 중 정확히 하나로만 분류하고, 신뢰도를 숫자로 말해줘.\n"
            "가능한 항목 : 플라스틱, 종이, 캔, 유리, 일반쓰레기, 비닐\n"
            "다른 말은 절대 하지마. 그리고 반드시 아래 형식만 사용해줘 :\n"
            "분류: [항목명]\n신뢰도: [0~100]%"
        ),
        "images": [image_data],
        "stream": False
    }

    try:
        resp = requests.post("http://localhost:11434/api/generate", json=payload)
        result = resp.json()
        raw_text = result.get("response", "").strip()
    except Exception as e:
        print(f"예외 발생: LLaVA 호출 실패 -> {e}")
        return "분류 실패", 0.0, ""

    # 분류 및 신뢰도 파싱
    label = None
    confidence = 0.0
    for cat in CATEGORIES:
        if cat in raw_text:
            label = cat
            break

    match = re.search(r"(\d{1,3})\s?%", raw_text)
    if match:
        confidence = int(match.group(1)) / 100

    return label or "분류 실패", confidence, raw_text
