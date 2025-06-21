🧠 SWE_Group-project (소웨공 002 수업 2팀)

1️⃣ 주제: AI 기반 분리수거 도우미 (Web 기반)
사용자가 이미지를 업로드하면, AI가 쓰레기 종류를 자동으로 분류하고,
그에 맞는 분리수거 가이드를 제공합니다.

2️⃣ 주요 기능
이미지 업로드 및 분류 요청

VLM 모델을 이용한 쓰레기 종류 자동 판별

LLM 모델을 이용한 분리수거 가이드 생성 및 안내

3️⃣ 기술 스택
Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

AI 모델: Ollama 기반 VLM / LLM 연동

4️⃣ 디렉터리 구조
project-root/
│
├── app.py                # Flask 백엔드 실행 파일
├── vlm_service.py        # 이미지 분류 함수 (VLM 연동)
├── llm_service.py        # 분리수거 가이드 생성 함수 (LLM 연동)
├── requirements.txt      # 의존성 패키지 목록
├── README.md             # 프로젝트 설명 문서
│
├── uploads/              # 업로드된 이미지 저장 폴더
│
├── index.html            # 프론트엔드 메인 HTML
├── style.css             # 프론트엔드 스타일시트
└── script.js             # 프론트엔드 JavaScript 로직

5️⃣ 전체 흐름 요약
사용자가 이미지를 업로드

Flask가 VLM 모델로 쓰레기 분류 수행

분류 결과를 바탕으로 LLM 모델이 가이드 생성

결과와 안내문을 웹 페이지에 출력
