# SWE_Group-project (dev_민혁)
성결대 소프트웨어 공학 팀 2 조별과제 레지스트리 입니다.


   
> ollama의 llava 기능으로 VLM Model 구현했습니다.

#### vlm_models.py와 image 폴더 추가 (2025.06.12)

#### 코드 일부 수정 (2025.06.13)
**1. 분류 실패 시 원본 응답 텍스트를 출력하여 디버깅이 용이하도록 수정**
```python
# -- 수정 전 --
text = result.get("response", "").strip()

...

if label :
        return label, confidence
    else :
        return "분류 실패", 0.0
```
 - 응답 실패 시, `text`에는 빈 문자열 ("")이 들어가며, 아무런 값을 담지 않았음.
 - label에 값이 없을 경우 단순히 "분류 실패", 0.0만을 반환 해주는 형태임.
 - 에러 응답이 있어도 디버깅할 수 있는 정보가 출력되지 않음.


   
```python
# -- 수정 후 --
text = result.get("response")
if not text:
    print("[LLaVA 응답 없음 또는 빈 응답입니다]", result)
    return "분류 실패", 0.0
text = text.strip()

...

if label :
    return label, confidence
```

- 아무런 응답이 없는 경우 파싱 시도를 사전 차단하도록 코드를 수정함.
- 분류 실패 시 원본 응답 메시지를 로그에 출력해줌 -> 디버깅이 유리해짐..


**2. 카테고리 리스트(CATEGORIS)를 만들어 코드 재사용성 및 유지보수성 향상**
```python
# -- 수정 전 --
for type_ in ["플라스틱", "종이", "캔", "유리", "일반쓰레기", "비닐"]:
    if type_ in text:
        label = type_
        break
```
- 분류 항목이 하드코딩 되어 있음.
- 항목 변경 시 여러 줄을 수정해야 하는 단점이 있음.


```python
# -- 수정 후 --
for type_ in CATEGORIES:
    if type_ in text:
        label = type_
        break
```
- 분류 항목을 카테고리 리스트에서 관리 가능.
- 새로운 항목 추가/수정이 간편해짐.


**3. 이미지 리스트를 순차적으로 처리**
```python
# -- 수정 전 --
label, confidence = predict_image("images/test_Can.jpg")
print("예측 결과:", label)
print("신뢰도:", confidence)
```
- 하나의 이미지만을 처리했음.

   
```python
# -- 수정 후 --
for img_path in test_images:
    print(f"\n [이미지 다중 분류] : {img_path}")
    label, confidence = predict_image(img_path)

    print(f"예측 결과 : {label}")
    print(f"신뢰도 : {confidence:.2f}")
```
- for 반복문을 활용해 이미지 리스트를 순차적으로 처리하도록 구성함.


   
**4. 프롬프트 수정**
```python
# -- 수정 전 --
"prompt": (
    "너는 분리수거 전문가야.\n"
    "다음 사진 속 쓰레기를 아래 6가지 중 하나로 분류하고, 신뢰도도 백분율로 알려줘.\n"
    "1. 종이\n2. 플라스틱\n3. 캔\n4. 유리\n5. 일반쓰레기\n6. 비닐\n\n"
    "반드시 아래 형식만 사용해줘:\n"
    "분류: [종류]\n신뢰도: [0~100]%"
)
```
- 원하지 않는 대답을 하기도 함.


   
```python
# -- 수정 후 --
"prompt": (
            "너는 분리수거 분류 모델이야.\n"
            "다음 사진 속 쓰레기를 아래 목록 중 정확히 하나로만 분류하고, 신뢰도를 숫자로 말해줘.\n"
            "가능한 항목 : 플라스틱, 종이, 캔, 유리, 일반쓰레기, 비닐\n"
            "다른 말은 절대 하지마. 그리고 반드시 아래 형식만 사용해줘 :\n"
            "분류: [항목명]\n신뢰도: [0~100]%"
        )
```
- 프롬프트를 명확하고 단순하게 바꿔 프롬프트가 정확한 답을 낼 수 있도록 변경함.
