# VLM:함수: predict_image(file_path: str) -> (label: str, confidence: float)
# 반환값: 예측 분류명, 신뢰도 수치
"""
    설치 목록
    # 1. pip install ollama

    실행 방법
    # 1. 터미널에 ollama run llava 실행
    # 2. ollama 서버 실행 중인 상태로 새로운 터미널 열어 python vlm_models.py 입력
    # 3. 시간이 지나면 (좀 오래 걸림) 분석해줌

"""

import base64 # 바이너리 데이터를 base64 문자열로 인코딩하려고 사용 (이미지 전송용)
import requests # HTTP 요청을 보내려고 사용 (LLaVA API와 통신용)
import re #정규 표현식을 사용해 텍스트서 신뢰도 수치 추출

def predict_image(file_path: str )-> tuple[str, float]:
    """
    입력된 이미지 파일 경로를 기반으로 ollama의 LLaVA 모델에 쓰레기 분리수거 분류 요청

    Input :
        file_path: str : 입력된(분류할) 이미지 파일 경로
    
    Output :
        label (str) : 예측된 쓰레기 분류명 
        confidence (number) : 신뢰도 (0 ~ 1 사이)
    """

    # 입력된 이미지 파일을 base64로 인코딩
    with open(file_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # VLM 모델에게 요청할 payload 요청메시지 구성
    payload = {
        "model": "llava",
        "prompt": (
            "너는 분리수거 전문가야.\n"
            "다음 사진 속 쓰레기를 아래 6가지 중 하나로 분류하고, 신뢰도도 백분율로 알려줘.\n"
            "1. 종이\n2. 플라스틱\n3. 캔\n4. 유리\n5. 일반쓰레기\n6. 비닐\n\n"
            "반드시 아래 형식만 사용해줘:\n"
            "분류: [종류]\n신뢰도: [0~100]%"
        ),
        "images": [image_data],
        "stream": False
    }

    # 로컬 Ollama 서버 (http://localhost:11434)에 POST 요청을 보내는 식으로 구현  # 참고 : https://ollama.com/library/llava
    try :
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        result = response.json()

        # LLaVA 응답 텍스트 추출
        text = result.get("response", "").strip()
        print("LLaVA 응답 : ", text)
    except Exception as ex:
        # 추가로 try-except로 예외처리
        print(f"예외 발생 LLaVA 호출 실패 : {ex}")
        return "분류 실패", 0.0


    label = None # 분리수거 품목이 무엇인가 담을 변수
    confidence = 0.0 # 정확도, 확신도 담을 변수수

    # 분리수거 분류명 파싱
    for type_ in ["플라스틱", "종이", "캔", "유리", "일반쓰레기", "비닐"]:
        if type_ in text:
            label = type_
            break
    
    # 응답 텍스트에서 신뢰도 숫자 (ex. "95%")를 정규식(re)로 찾는다.
    # \d{1,3} : 1~3자리 숫자 의미,  \s?% : 그 숫자 뒤에 공백이 오거나 '%'기호가 붙어야한다
    match = re.search(r"(\d{1,3})\s?%", text)

    # match(신뢰도 숫자를 정상적으로 찾음)가 존재한다면 
    if match:
        confidence = int(match.group(1)) / 100

    # label이 정상적으로 파싱 됐다면, 라벨명과 신뢰도 리턴
    # 못 찾았따면, 분류 실패 및 신뢰도 0.0 반환
    if label :
        return label, confidence
    else :
        return "분류 실패", 0.0

# 테스트용 / pridect_image() 작동하는지 참고용 코드라서 지우셔도 됩니다
label, confidence = predict_image("images/test_Can.jpg")
print("예측 결과:", label)
print("신뢰도:", confidence)
