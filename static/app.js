function setStatus(el, msg, kind) {
  el.textContent = msg || "";
  el.className = "status" + (kind ? " " + kind : "");
}

async function generate(type) {
  const inputEl = document.getElementById(type + "-input");
  const outputEl = document.getElementById(type + "-output");
  const btn = document.getElementById(type + "-gen");
  const status = document.getElementById(type + "-status");

  const text = inputEl.value.trim();
  if (!text) {
    setStatus(status, "입력이 비어 있습니다.", "error");
    return;
  }

  btn.disabled = true;
  const originalLabel = btn.textContent;
  btn.textContent = "생성 중...";
  setStatus(status, "Claude 호출 중...");

  try {
    const resp = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type, text }),
    });
    const data = await resp.json();
    if (!resp.ok) {
      setStatus(status, data.error || "오류가 발생했습니다.", "error");
      return;
    }
    outputEl.value = data.output || "";
    setStatus(status, "완료", "ok");
  } catch (e) {
    setStatus(status, "네트워크 오류: " + e.message, "error");
  } finally {
    btn.disabled = false;
    btn.textContent = originalLabel;
  }
}

async function copyOutput(type) {
  const outputEl = document.getElementById(type + "-output");
  const status = document.getElementById(type + "-copy-status");
  const text = outputEl.value;
  if (!text) {
    setStatus(status, "복사할 내용이 없습니다.", "error");
    return;
  }
  try {
    await navigator.clipboard.writeText(text);
    setStatus(status, "복사됨", "ok");
    setTimeout(() => setStatus(status, ""), 2000);
  } catch (e) {
    setStatus(status, "복사 실패: " + e.message, "error");
  }
}

document.getElementById("weekly-gen").addEventListener("click", () => generate("weekly"));
document.getElementById("monthly-gen").addEventListener("click", () => generate("monthly"));
document.getElementById("weekly-copy").addEventListener("click", () => copyOutput("weekly"));
document.getElementById("monthly-copy").addEventListener("click", () => copyOutput("monthly"));
