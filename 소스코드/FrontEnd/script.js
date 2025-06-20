// script.js (백엔드 연동 완료 버전)
document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("uploadForm");
  const imageInput = document.getElementById("imageInput");
  const resultSection = document.getElementById("resultSection");
  const errorSection = document.getElementById("errorSection");
  const categorySpan = document.getElementById("category");
  const confidenceSpan = document.getElementById("confidence");
  const guideText = document.getElementById("guideText");
  const saveBtn = document.getElementById("saveResultBtn");
  const discardBtn = document.getElementById("discardResultBtn");
  const historySection = document.getElementById("historySection");
  const historyList = document.getElementById("historyList");
  const viewHistoryBtn = document.getElementById("viewHistoryBtn");
  const closeHistoryBtn = document.getElementById("closeHistoryBtn");
  const historyStats = document.getElementById("historyStats");
  const loadingMessage = document.getElementById("loadingMessage");
  const copyGuideBtn = document.getElementById("copyGuideBtn");
  const copyStatus = document.getElementById("copyStatus");

  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    resultSection.classList.add("hidden");
    errorSection.classList.add("hidden");
    const file = imageInput.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    loadingMessage.classList.remove("hidden");

    try {
      const uploadRes = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });
      if (!uploadRes.ok) throw new Error("Upload failed");
      const uploadData = await uploadRes.json();
      const imageId = uploadData.data.file_id;

      const analyzeRes = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ imageId }),
      });
      if (!analyzeRes.ok) throw new Error("Analyze failed");
      const analyzeData = await analyzeRes.json();
      categorySpan.textContent = analyzeData.result;
      confidenceSpan.textContent = `${(analyzeData.confidence * 100).toFixed(1)}%`;

      const guideRes = await fetch("http://localhost:5000/guide", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category: analyzeData.result }),
      });
      if (!guideRes.ok) throw new Error("Guide failed");
      const guideData = await guideRes.json();
      guideText.textContent = guideData.guide;

      resultSection.classList.remove("hidden");

      if (copyGuideBtn) {
        copyGuideBtn.addEventListener("click", () => {
          const text = guideText.textContent;
          navigator.clipboard.writeText(text)
            .then(() => alert("안내문이 복사되었습니다!"))
            .catch(() => alert("복사에 실패했습니다."));
        });
      }

      saveBtn.onclick = async () => {
        await fetch("http://localhost:5000/save", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            imageId,
            category: analyzeData.result,
            confidence: analyzeData.confidence,
          }),
        });
        alert("결과가 저장되었습니다.");
        resultSection.classList.add("hidden");
      };

      discardBtn.onclick = () => {
        alert("결과를 저장하지 않았습니다.");
        resultSection.classList.add("hidden");
      };

    } catch (err) {
      console.error(err);
      errorSection.classList.remove("hidden");
    } finally {
      loadingMessage.classList.add("hidden");
    }
  });

  viewHistoryBtn.addEventListener("click", async () => {
    historyList.innerHTML = "";
    historyStats.innerHTML = "";
    try {
      const res = await fetch("http://localhost:5000/history");
      if (!res.ok) throw new Error("History fetch failed");
      const data = await res.json();
      const categoryCount = {};
      const total = data.length;

      data.forEach(item => {
        categoryCount[item.category] = (categoryCount[item.category] || 0) + 1;
      });

      let statsHTML = `<p><strong>총 업로드 수:</strong> ${total}건</p>`;
      statsHTML += `<p><strong>분류된 쓰레기 종류:</strong></p><ul>`;
      for (const [category, count] of Object.entries(categoryCount)) {
        statsHTML += `<li>${category}: ${count}회</li>`;
      }
      statsHTML += `</ul>`;
      historyStats.innerHTML = statsHTML;

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

      historySection.classList.remove("hidden");

    } catch (err) {
      alert("기록을 불러오는 데 실패했습니다.");
      console.error(err);
    }
  });

  closeHistoryBtn.addEventListener("click", () => {
    historySection.classList.add("hidden");
  });
});
