document.addEventListener("DOMContentLoaded", () => {
  const grantBtn   = document.getElementById("grantBtn");
  const permStatus = document.getElementById("permStatus");

  async function requestMic() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach(track => track.stop());
      permStatus.innerText = "✅ Microphone permission granted successfully! You can close this tab now.";
      permStatus.style.color = "#10B981";
      grantBtn.innerText = "✓ Permission Granted";
      grantBtn.disabled = true;
      setTimeout(() => {
        window.close();
      }, 2500);
    } catch (err) {
      console.error("Microphone permission error:", err);
      permStatus.innerText = "⚠️ Microphone access denied: " + err.message + ". Please click 'Allow' in Chrome address bar prompt.";
      permStatus.style.color = "#EF4444";
    }
  }

  grantBtn.addEventListener("click", requestMic);
  requestMic();
});
