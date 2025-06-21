// script.js

const uploadBtn     = document.getElementById('uploadButton');
const fileInput     = document.getElementById('imageInput');
const resultSection = document.getElementById('resultSection');
const resultText    = document.getElementById('resultText');
const guideText     = document.getElementById('guideText');  // 새로 추가

uploadBtn.addEventListener('click', async () => {
  // 1) 이전 결과 초기화
  resultText.textContent = '';
  guideText.textContent  = '';
  resultSection.classList.add('hidden');

  // 2) 파일 체크
  if (!fileInput.files.length) {
    return alert('이미지를 선택해주세요.');
  }

  // 3) 업로드
  const formData = new FormData();
  formData.append('image', fileInput.files[0]);

  try {
    const res = await fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData,
      mode: 'cors'
    });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const data = await res.json();

    // 4) 결과 표시
    resultText.textContent = data.category || '알 수 없는 분류';
    guideText.textContent  = data.guidance || '';
    resultSection.classList.remove('hidden');

  } catch (err) {
    console.error('업로드 실패:', err);
    alert('업로드 중 오류가 발생했습니다.');
  } finally {
    // 5) 같은 파일을 다시 선택할 수 있게 input 리셋
    fileInput.value = '';
  }
});

// 기록 보기 버튼 이벤트
const viewLogsButton = document.getElementById('viewLogsButton');
viewLogsButton.addEventListener('click', () => {
  alert('📜 기록 보기 기능은 현재 준비 중입니다.');
});

// 사용 방법 버튼 이벤트
const usageGuideButton = document.getElementById('usageGuideButton');
usageGuideButton.addEventListener('click', () => {
  alert(`❓ 사용 방법 안내입니다:

1. 이미지를 선택 후 '이미지 업로드' 버튼을 누르세요.
2. AI가 분류 및 재활용 가이드를 제공해드립니다.`);
});