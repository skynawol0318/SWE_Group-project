🧠 SWE_Group-project (소웨공 002 수업 2팀)
📖 프로젝트 개요
AI 기반 분리수거 도우미 (Web 기반)
사용자가 이미지를 업로드하면 AI가 쓰레기 종류를 자동 분류하고, 그에 적합한 분리수거 가이드(방법, 주의사항 등)를 제공하는 웹 애플리케이션입니다.

✨ 주요 기능
이미지 업로드 및 분류 요청

사용자가 웹 페이지에서 쓰레기 이미지를 업로드

VLM 모델 기반 쓰레기 종류 분류

업로드된 이미지를 VLM(Vision-Language Model)로 분석하여 쓰레기 종류를 판별

LLM 모델 기반 분리수거 안내 생성

분류된 쓰레기 종류를 바탕으로 LLM을 활용해 분리수거 안내 메시지를 동적으로 생성

결과 웹 출력

분류 결과(쓰레기 종류)와 가이드(안내문)를 사용자에게 실시간 출력

🧰 기술 스택
구분	기술
Frontend	HTML, CSS, JavaScript
Backend	Python (Flask)
AI 모델	Ollama 기반 VLM, LLM 연동

🔄 프로젝트 동작 흐름:
사용자가 이미지를 업로드

Flask 백엔드에서 VLM 모델 호출 → 쓰레기 종류 판별

LLM 모델 호출 → 분리수거 안내 메시지 생성

분류 결과와 안내를 사용자 웹 화면에 표시

📂 깃허브 프로젝트 디렉터리 구조
**SWE_Group-project/
├── __pycache__/             # 파이썬 캐시 파일 폴더
├── src/
│   ├── BackEnd/
│   │   ├── __pycache__/     # 백엔드 캐시 폴더
│   │   ├── static/          # 정적 파일 (CSS, JS, 업로드된 이미지 등)
│   │   ├── __init__.py      # 파이썬 초기화 파일
│   │   ├── app.py           # Flask 메인 앱 실행 파일
│   │   ├── llm_service.py   # LLM 호출 및 안내 메시지 생성
│   │   ├── vlm_service.py   # VLM 호출 및 쓰레기 분류 처리
│   │   └── package-lock.json# 의존성 관련 파일
│   │
│   ├── FrontEnd/
│       ├── ...              # (프론트엔드 관련 정적 파일, HTML/CSS/JS 등)
├── README.md                # 프로젝트 설명 파일**
