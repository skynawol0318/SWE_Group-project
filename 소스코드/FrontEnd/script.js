document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("uploadForm");              // 이미지 업로드 폼
  const imageInput = document.getElementById("imageInput");              // 이미지 선택 input
  const resultSection = document.getElementById("resultSection");        // 분석 결과 영역
  const errorSection = document.getElementById("errorSection");          // 에러 표시 영역
  const categorySpan = document.getElementById("category");              // 분석된 쓰레기 종류 표시
  const confidenceSpan = document.getElementById("confidence");          // 신뢰도 표시
  const guideText = document.getElementById("guideText");                // 분리수거 안내 텍스트
  const saveBtn = document.getElementById("saveResultBtn");              // 결과 저장 버튼
  const discardBtn = document.getElementById("discardResultBtn");        // 저장하지 않기 버튼
  const historySection = document.getElementById("historySection");      // 기록 모달 창
  const historyList = document.getElementById("historyList");            // 기록 리스트 영역
  const viewHistoryBtn = document.getElementById("viewHistoryBtn");      // 기록 보기 버튼
  const closeHistoryBtn = document.getElementById("closeHistoryBtn");    // 기록 모달 닫기 버튼
  const historyStats = document.getElementById("historyStats");          // 기록 통계 표시 영역

  // 아래 세 줄 추가된 요소
  const loadingMessage = document.getElementById("loadingMessage");      // 분석 중 메시지 영역 
  const copyGuideBtn = document.getElementById("copyGuideBtn");          // 안내문 복사 버튼
  const copyStatus = document.getElementById("copyStatus");              // 복사 상태 텍스트

  //이미지 업로드 및 분석 처리
  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    resultSection.classList.add("hidden");
    errorSection.classList.add("hidden");

    const file = imageInput.files[0];
    if (!file) return;

    const formData = new FormData();           //FormData에 이미지 추가
    formData.append("image", file);

     // 추가된 요소
    loadingMessage.classList.remove("hidden"); // 분석 중 메시지 표시

    try {
      //이미지 업로드
      const uploadRes = await fetch("/upload", {
        method: "POST",
        body: formData,
      });
      if (!uploadRes.ok) throw new Error("Upload failed");

      const uploadData = await uploadRes.json();
      const imageId = uploadData.imageId;

      //업로드된 이미지 분석 요청
      const analyzeRes = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ imageId }),
      });
      if (!analyzeRes.ok) throw new Error("Analyze failed");

      const analyzeData = await analyzeRes.json();
      categorySpan.textContent = analyzeData.category;                               // 분류 결과 표시
      confidenceSpan.textContent = `${(analyzeData.confidence * 100).toFixed(1)}%`;  // 신뢰도 퍼센트 표시

      //분리수거 가이드 요청
      const guideRes = await fetch("/guide", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category: analyzeData.category }),
      });
      if (!guideRes.ok) throw new Error("Guide failed");

      const guideData = await guideRes.json();
      guideText.textContent = guideData.guide;        //가이드 텍스트 표시

      resultSection.classList.remove("hidden");       //결과 영역 보여주기

      // 추가된 요소 - 안내문 복사 버튼 기능
      const copyGuideBtn = document.getElementById("copyGuideBtn");
      if (copyGuideBtn) {
       copyGuideBtn.addEventListener("click", () => {
         const text = guideText.textContent;
         navigator.clipboard.writeText(text)
           .then(() => alert("안내문이 복사되었습니다!"))
           .catch(() => alert("복사에 실패했습니다."));
       });
      } 
     

      //결과 저장
      saveBtn.onclick = async () => {
        await fetch("/save", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            imageId,
            category: analyzeData.category,
            confidence: analyzeData.confidence,
          }),
        });
        alert("결과가 저장되었습니다.");
        resultSection.classList.add("hidden");
      };

      // 저장하지 않기
      discardBtn.onclick = () => {
        alert("결과를 저장하지 않았습니다.");
        resultSection.classList.add("hidden");
      };
      //오류
    } catch (err) {
      console.error(err);
      errorSection.classList.remove("hidden");
    } finally { 
      // 추가된 요소
      loadingMessage.classList.add("hidden");   // 분석 완료 후 메시지 숨기기
    }  
  });

  //사용법 모달 처리
  const guideModal = document.getElementById("guideModal");
  const toggleGuideBtn = document.getElementById("toggleGuideBtn");
  const closeGuideBtn = document.getElementById("closeGuideBtn");

  toggleGuideBtn.addEventListener("click", () => {
    guideModal.classList.remove("hidden"); //사용법 모달 열기
  });

  closeGuideBtn.addEventListener("click", () => {
    guideModal.classList.add("hidden"); //사용법 모달 닫기
  });

  //모달 외부 클릭 시 닫기
  window.addEventListener("click", (e) => {
    if (e.target === guideModal) guideModal.classList.add("hidden");
    if (e.target === historySection) historySection.classList.add("hidden");
  });

  //기록 보기
  viewHistoryBtn.addEventListener("click", async () => {
    historyList.innerHTML = "";
    historyStats.innerHTML = "";

    try {
      const res = await fetch("/history"); //기록 요청
      if (!res.ok) throw new Error("History fetch failed");

      const data = await res.json();

      //통계 계산
      const categoryCount = {};
      const total = data.length;

      data.forEach(item => {
        categoryCount[item.category] = (categoryCount[item.category] || 0) + 1;
      });

      //통계 생성
      let statsHTML = `<p><strong>총 업로드 수:</strong> ${total}건</p>`;
      statsHTML += `<p><strong>분류된 쓰레기 종류:</strong></p><ul>`;
      for (const [category, count] of Object.entries(categoryCount)) {
        statsHTML += `<li>${category}: ${count}회</li>`;
      }
      statsHTML += `</ul>`;
      historyStats.innerHTML = statsHTML;

      //기록 리스트 표시
      if (data.length === 0) {
        historyList.innerHTML = "<li>저장된 기록이 없습니다.</li>";
      } else {
        data.forEach(item => {
          const li = document.createElement("li");
          li.innerHTML = `
            <img src="${item.imageUrl}" width="100px" style="vertical-align: middle; margin-right: 10px; border-radius: 5px;"/>
            <strong>${item.category}</strong> (${(item.confidence * 100).toFixed(1)}%)<br/>
            <small>${new Date(item.date).toLocaleString()}</small>
          `;
          historyList.appendChild(li);
        });
      }

      historySection.classList.remove("hidden"); //기록 모달 열기

    } catch (err) {
      alert("기록을 불러오는 데 실패했습니다.");
      console.error(err);
    }
  });

  //기록 모달 닫기 버튼 처리
  closeHistoryBtn.addEventListener("click", () => {
    historySection.classList.add("hidden");
  });
});
