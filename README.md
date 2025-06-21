

🧠 SWE_Group-project (소웨공 002 수업 2팀)
1. 📌 주제: AI 기반 분리수거 도우미 (Web 기반)
사용자가 이미지를 업로드하면, AI가 해당 쓰레기의 종류를 판별하고 적절한 분리수거 가이드를 제공합니다.

2. 🔧 주요 기능
이미지 업로드 기능

쓰레기 종류 자동 분류 (VLM 모델 활용)

항목에 맞는 분리수거 가이드 제공 (LLM 모델 활용)

3. 🛠️ 기술 스택
Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

AI 모델: Ollama 기반 VLM / LLM 연동

4. 📁 디렉터리 구조
project-root/
│
├── app.py                  # Flask 백엔드 메인 실행 파일
├── vlm_service.py         # 이미지 분류 함수 (VLM 모델 연동)
├── llm_service.py         # 분리수거 가이드 생성 함수 (LLM 모델 연동)
├── requirements.txt       # 필요한 Python 패키지 목록
├── README.md              # 프로젝트 소개 문서
│
├── uploads/               # 업로드된 이미지 저장 폴더
│
├── index.html             # 웹 페이지 메인 HTML
├── style.css              # 프론트엔드 스타일시트
└── script.js              # 프론트엔드 JavaScript 로직


5. 🔄 전체 흐름 요약
사용자가 이미지를 업로드하면, VLM이 분류 결과를 추론하고 해당 결과를 기반으로 LLM이 분리수거 가이드를 생성하여 웹에 출력합니다.
프론트엔드는 HTML/CSS/JS로 구성되며, Flask 백엔드가 두 모델과 연동되어 전체 흐름을 처리합니다.

