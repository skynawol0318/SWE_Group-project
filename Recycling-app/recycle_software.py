import base64
import requests
import re

# VLM 연동을 위한 predict_image 함수 (제공해주신 코드 그대로 사용)
def predict_image(file_path: str) -> tuple[str, float]:
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

    # 로컬 Ollama 서버 (http://localhost:11434)에 POST 요청을 보내는 식으로 구현
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        result = response.json()

        # LLaVA 응답 텍스트 추출
        text = result.get("response", "").strip()
        print("LLaVA 응답 : ", text)
    except Exception as ex:
        print(f"예외 발생 LLaVA 호출 실패 : {ex}")
        return "분류 실패", 0.0

    label = None
    confidence = 0.0

    # 분리수거 분류명 파싱
    for type_ in ["플라스틱", "종이", "캔", "유리", "일반쓰레기", "비닐"]:
        if type_ in text:
            label = type_
            break
    
    # 응답 텍스트에서 신뢰도 숫자 (ex. "95%")를 정규식(re)로 찾는다.
    match = re.search(r"(\d{1,3})\s?%", text)

    # match(신뢰도 숫자를 정상적으로 찾음)가 존재한다면 
    if match:
        confidence = int(match.group(1)) / 100

    if label:
        return label, confidence
    else:
        return "분류 실패", 0.0

### 수정된 LLM 로직: `simulate_llm_response_with_vlm`

def simulate_llm_response_with_vlm(query: str, image_file_path: str = None) -> str:
    """
    사용자 쿼리와 (선택적) 이미지 파일 경로를 기반으로 분리수거 안내 문장을 생성하는 함수.
    VLM (predict_image)의 분류 결과를 활용합니다.

    Args:
        query (str): 사용자의 질의 텍스트.
        image_file_path (str, optional): 이미지 파일의 경로. VLM이 이미지를 분석하는 데 사용됩니다.
                                         Defaults to None.

    Returns:
        str: 분리수거 방법에 대한 안내 문장.
    """
    lower_query = query.lower()
    vlm_label = None
    vlm_confidence = 0.0

    # 이미지 파일 경로가 제공된 경우 VLM 호출
    if image_file_path:
        print(f"\n[VLM] 이미지 분석 요청: {image_file_path}")
        vlm_label, vlm_confidence = predict_image(image_file_path)
        print(f"[VLM] 분석 결과: 분류='{vlm_label}', 신뢰도={vlm_confidence*100:.2f}%")

        # VLM이 성공적으로 분류했고 신뢰도가 일정 수준 이상인 경우, LLM 응답에 반영
        if vlm_label != "분류 실패" and vlm_confidence > 0.6:  # 신뢰도 임계값 설정
            # VLM이 식별한 물품에 대한 정보 제공
            return (
                f"**VLM 분석 결과:** 이미지를 통해 **'{vlm_label}'** (신뢰도: {vlm_confidence*100:.1f}%)으로 보입니다.\n"
                f"{get_recycling_guide(vlm_label)}"  # VLM 분류 결과에 대한 상세 가이드 제공
            )
        elif vlm_label != "분류 실패":
            # 신뢰도가 낮지만 분류는 된 경우, 사용자에게 확인 요청
            return (
                f"**VLM 분석 결과:** 이미지를 통해 **'{vlm_label}'** (신뢰도: {vlm_confidence*100:.1f}%)으로 추정되나, "
                f"신뢰도가 낮습니다. 해당 물품이 맞는지 확인해주시거나, 다른 질문을 해주세요."
            )
        else:
            # VLM 분류 실패 시 메시지
            return "이미지 분석에 실패했습니다. 물품의 종류를 텍스트로 알려주시겠어요?"

    # 이미지 파일 경로가 없거나 VLM 분석 실패 시, 텍스트 쿼리 기반으로 응답
    # 기존 LLM 로직을 여기에 포함
    if '페트병' in lower_query or 'pet' in lower_query:
        return '**투명 페트병**은 내용물을 비우고 깨끗하게 헹군 후 라벨을 제거하고 압착하여 투명 페트병 수거함에 넣어주세요. 다른 색깔의 페트병은 플라스틱류로 배출합니다.'
    elif '플라스틱' in lower_query or 'plastic' in lower_query:
        return '**플라스틱류 (PP, PE, PS 등)**: 내용물을 비우고 깨끗하게 헹군 후 플라스틱 수거함에 넣어주세요. 이물질이 제거되지 않거나, 다른 재질이 혼합된 경우 (예: 칫솔, 장난감) 일반쓰레기로 버려야 합니다.'
    elif '유리병' in lower_query or 'glass' in lower_query:
        if '깨진' in lower_query or '파손' in lower_query:
            return '**깨진 유리**: 신문지 등에 싸서 다치지 않도록 주의하여 일반쓰레기 종량제 봉투에 넣어 버려주세요. 재활용이 불가능합니다.'
        return '**유리병**: 뚜껑을 제거하고 내용물을 비운 후 깨끗하게 헹궈서 유리병 수거함에 넣어주세요. 거울, 깨진 유리, 크리스탈류는 일반쓰레기입니다.'
    elif '종이' in lower_query or 'paper' in lower_query:
        if any(keyword in lower_query for keyword in ['코팅', '영수증', '비닐', '음식물 묻은']):
            return '**코팅된 종이/영수증/이물질 묻은 종이**: 재활용이 어려우므로 일반쓰레기 종량제 봉투에 버려주세요. (예: 라면 봉지, 택배 송장, 음식물이 묻은 종이컵)'
        return '**종이류**: 물기에 젖지 않도록 묶거나 박스에 담아 종이류 수거함에 넣어주세요. 테이프, 철심 등은 제거 후 배출합니다.'
    elif '음식물 쓰레기' in lower_query or 'food waste' in lower_query:
        return '**음식물 쓰레기**: 물기를 최대한 제거하고 음식물 쓰레기 봉투에 넣어 배출하세요. 뼈, 조개껍데기, 달걀 껍질, 씨앗류, 일회용 컵라면 용기 등은 일반쓰레기입니다.'
    elif any(keyword in lower_query for keyword in ['캔', '알루미늄', '고철']):
        return '**캔/고철류**: 내용물을 비우고 깨끗하게 헹군 후 압착하여 캔류 수거함에 넣어주세요. 담배꽁초 등 이물질은 제거해야 합니다.'
    elif any(keyword in lower_query for keyword in ['비닐류', '봉투']):
        if any(keyword in lower_query for keyword in ['오염', '이물질']):
            return '**오염된 비닐**: 내용물을 비우고 깨끗하게 헹궈도 이물질이 제거되지 않는 비닐은 일반쓰레기 종량제 봉투에 버려주세요.'
        return '**비닐류**: 내용물을 비우고 깨끗하게 헹군 후 비닐류 수거함에 넣어주세요. 과자 봉지, 라면 봉지 등은 재활용 가능 마크가 있더라도 이물질 오염이 심하면 일반쓰레기입니다.'
    elif '스티로폼' in lower_query:
        if any(keyword in lower_query for keyword in ['음식물', '색상']):
            return '**음식물 묻은 스티로폼/색상 스티로폼**: 재활용이 어려우므로 일반쓰레기 종량제 봉투에 넣어 버려주세요. 과일 포장재 등 완충재는 재활용 가능합니다.'
        return '**흰색 스티로폼**: 내용물을 비우고 이물질이 없는 깨끗한 흰색 스티로폼만 재활용이 가능합니다. 이물질이 묻은 것은 일반쓰레기입니다.'
    elif any(keyword in lower_query for keyword in ['건전지', 'battery']):
        return '**폐건전지**: 가까운 주민센터, 아파트 등에 비치된 폐건전지 수거함에 넣어주세요.'
    elif any(keyword in lower_query for keyword in ['형광등', '전구']):
        if '깨진' in lower_query:
            return '**깨진 형광등/전구**: 깨진 파편은 신문지 등에 싸서 다치지 않도록 일반쓰레기 종량제 봉투에 버려주세요.'
        return '**폐형광등/폐전구**: 깨지지 않게 조심하여 폐형광등 수거함에 넣어주세요. LED 전구는 일반쓰레기입니다.'
    elif any(keyword in lower_query for keyword in ['의류', '옷']):
        if any(keyword in lower_query for keyword in ['솜 이불', '베개', '신발', '가방']):
            return '**솜 이불/베개/신발/가방**: 의류수거함에 넣을 수 없으며, 일반쓰레기 또는 대형 폐기물 스티커를 부착하여 버려야 합니다.'
        return '**의류**: 깨끗한 옷가지, 신발, 가방 등은 의류수거함에 넣어주세요. 오염되었거나 훼손된 옷은 재활용이 어렵습니다.'
    elif any(keyword in lower_query for keyword in ['도자기', '사기', '그릇', '화분']):
        return '**도자기/사기/깨진 그릇/화분**: 재활용이 불가능하므로 신문지에 싸서 다치지 않도록 일반쓰레기 종량제 봉투에 버려주세요.'
    elif any(keyword in lower_query for keyword in ['고무', '장갑']):
        return '**고무류/고무장갑**: 재활용이 어려우므로 일반쓰레기 종량제 봉투에 버려주세요.'
    elif any(keyword in lower_query for keyword in ['스티커', '반창고', '기저귀']):
        return '**스티커/반창고/기저귀**: 모두 재활용이 불가능하므로 일반쓰레기 종량제 봉투에 버려주세요.'
    elif '재활용 안 되는 것' in lower_query or '일반쓰레기' in lower_query:
        return '재활용이 안 되는 물건은 **일반쓰레기 종량제 봉투**에 담아 버려야 합니다. 대표적으로 깨진 유리, 오염된 비닐/종이, 음식물 묻은 용기, 도자기류, 고무류, 스티커, 기저귀 등이 있습니다. 품목별로 자세히 문의해주세요.'
    else:
        return '죄송하지만 해당 품목에 대한 정보를 찾을 수 없습니다. 물건의 종류나 재질을 포함하여 좀 더 자세히 설명해주시거나 다른 품목을 말씀해주세요.'

# VLM 분류 결과에 따라 상세 가이드를 제공하는 헬퍼 함수 (이전 LLM 로직에서 분리)
def get_recycling_guide(label: str) -> str:
    """
    분리수거 분류명(label)을 입력받아
    분리수거 방법과 주의사항 안내 문장을 생성하는 함수.
    """
    guide_dict = {
        "플라스틱": "플라스틱은 내용물을 깨끗이 비우고 물로 헹군 후 배출하세요. 라벨이나 스티커는 가능한 제거해 주세요.",
        "종이": "종이는 이물질을 제거하고, 물기에 젖지 않게 모아서 배출해야 합니다. 스프링이나 코팅지 등은 분리해 주세요.",
        "캔": "캔은 내용물을 완전히 비우고 물로 헹군 후 압축해서 배출하면 좋습니다. 알루미늄과 철은 구분하지 않아도 됩니다.",
        "유리": "유리는 깨지지 않도록 주의하여 배출하고, 병 안의 내용물은 완전히 비워주세요. 뚜껑은 따로 분리하세요.",
        "비닐": "비닐은 깨끗이 씻어 이물질을 제거한 후, 물기를 말린 뒤 배출하세요. 음식물이 묻은 비닐은 일반쓰레기입니다.",
        "일반쓰레기": "재활용이 불가능한 물건은 일반쓰레기로 분류합니다. 음식물 쓰레기, 오염된 종이, 깨진 유리 등은 해당됩니다."
    }
    return guide_dict.get(label, "해당 항목에 대한 분리수거 정보가 없습니다.")


if __name__ == "__main__":
    print("--- VLM 연동 LLM 테스트 (이미지 경로 존재) ---")
    # 실제 이미지를 'images/test_Can.jpg' 경로에 두고 테스트해야 합니다.
    # VLM 서버 (ollama run llava)가 실행 중이어야 합니다.
    
    # 예시 1: VLM이 '캔'으로 분류하고 신뢰도가 높은 경우
    print(f"질의: 이거 뭐야 (이미지: images/test_Can.jpg)")
    # 이 부분은 실제 predict_image가 호출되어 결과를 반환하도록 시뮬레이션
    # 가정: predict_image("images/test_Can.jpg") -> ("캔", 0.95) 반환
    guide_with_image = simulate_llm_response_with_vlm("이거 뭐야", image_file_path="images/test_Can.jpg")
    print(f"응답: {guide_with_image}\n")

    # 예시 2: VLM이 '플라스틱'으로 분류하고 신뢰도가 낮은 경우
    print(f"질의: 이거 뭐야 (이미지: images/test_Plastic_Low_Conf.jpg)")
    # 가정: predict_image("images/test_Plastic_Low_Conf.jpg") -> ("플라스틱", 0.55) 반환
    guide_with_low_conf_image = simulate_llm_response_with_vlm("이거 뭐야", image_file_path="images/test_Plastic_Low_Conf.jpg")
    print(f"응답: {guide_with_low_conf_image}\n")

    # 예시 3: VLM 분류가 실패한 경우
    print(f"질의: 이거 뭐야 (이미지: images/test_Failure.jpg)")
    # 가정: predict_image("images/test_Failure.jpg") -> ("분류 실패", 0.0) 반환
    guide_with_vlm_failure = simulate_llm_response_with_vlm("이거 뭐야", image_file_path="images/test_Failure.jpg")
    print(f"응답: {guide_with_vlm_failure}\n")

    print("\n--- 텍스트 기반 질의 테스트 (이미지 경로 없음) ---")
    print(f"질의: 페트병")
    print(f"응답: {simulate_llm_response_with_vlm('페트병')}\n")

    print(f"질의: 깨진 유리")
    print(f"응답: {simulate_llm_response_with_vlm('깨진 유리')}\n")
    
    print(f"질의: 잘 모르겠어요")
    print(f"응답: {simulate_llm_response_with_vlm('잘 모르겠어요')}\n")
