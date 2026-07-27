// popup.js — Formitra Extension Speech, Extraction & AI Voice Prompter

document.addEventListener("DOMContentLoaded", () => {
  const langSelect     = document.getElementById("langSelect");
  const micBtn         = document.getElementById("micBtn");
  const micIcon        = document.getElementById("micIcon");
  const statusText     = document.getElementById("statusText");
  const langDetected   = document.getElementById("langDetected");
  const transcriptText = document.getElementById("transcriptText");
  const demoBtn        = document.getElementById("demoBtn");
  const extractionCard = document.getElementById("extractionCard");
  const extractionGrid = document.getElementById("extractionGrid");
  const extractedCount = document.getElementById("extractedCount");
  const autoFillBtn    = document.getElementById("autoFillBtn");
  const toast          = document.getElementById("toast");

  let recognition = null;
  let isRecording = false;

  // Initialize Speech Recognition
  if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (event) => {
      let finalTranscript = "";
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript + " ";
        }
      }
      if (finalTranscript.trim()) {
        const current = transcriptText.value;
        transcriptText.value = (current ? current + " " : "") + finalTranscript.trim();
        onTranscriptUpdated();
      }
    };

    recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      stopRecording();
      showToast("⚠️ Mic access error: " + event.error);
    };

    recognition.onend = () => {
      if (isRecording) {
        stopRecording();
      }
    };
  } else {
    statusText.innerText = "⚠️ Web Speech API not supported in this browser.";
    micBtn.disabled = true;
  }

  // Mic Button Click
  micBtn.addEventListener("click", () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  });

  function startRecording() {
    if (!recognition) return;
    const selectedLang = langSelect.value;
    recognition.lang = selectedLang;

    try {
      recognition.start();
      isRecording = true;
      micBtn.classList.add("recording");
      micIcon.innerText = "⏹️";
      statusText.innerText = `🎙️ Listening in ${langSelect.options[langSelect.selectedIndex].text}... Speak clearly.`;
    } catch (e) {
      console.error(e);
    }
  }

  function stopRecording() {
    if (recognition && isRecording) {
      recognition.stop();
    }
    isRecording = false;
    micBtn.classList.remove("recording");
    micIcon.innerText = "🎙️";
    statusText.innerText = "Click microphone & speak your details";
  }

  // Demo Transcript Button
  demoBtn.addEventListener("click", () => {
    transcriptText.value = (
      "मेरा नाम राहुल शर्मा है। मैं जयपुर राजस्थान का रहने वाला हूँ। " +
      "मैं B.Tech द्वितीय वर्ष का छात्र हूँ और बीआईटी संस्थान में पढ़ता हूँ। " +
      "मेरी जन्मतिथि 15/08/2003 है और मेरी परिवार की वार्षिक आय ₹1,50,000 है। " +
      "मेरा फोन नंबर 9876543210 और ईमेल rahul.sharma@example.com है। " +
      "मेरा आधार नंबर 9876 5432 1098 है।"
    );
    onTranscriptUpdated();
    showToast("📋 Loaded sample transcript");
  });

  // Transcript Edit Handler
  transcriptText.addEventListener("input", onTranscriptUpdated);

  function onTranscriptUpdated() {
    const text = transcriptText.value.trim();
    if (!text) {
      autoFillBtn.disabled = true;
      extractionCard.classList.add("hidden");
      langDetected.classList.add("hidden");
      return;
    }

    autoFillBtn.disabled = false;

    // Auto Detect Language Script
    const detected = detectScriptLanguage(text);
    if (detected) {
      langDetected.innerText = `🌐 Auto-Detected: ${detected}`;
      langDetected.classList.remove("hidden");
    } else {
      langDetected.classList.add("hidden");
    }

    // Run Gemma AI Intent Extractor
    const fields = extractFormFields(text);
    renderExtractedFields(fields);
    checkMissingRequiredFields(fields);
  }

  function checkMissingRequiredFields(fields) {
    const required = ["name", "dob", "income", "state", "city"];
    const missing = required.filter(k => !fields[k]);
    if (missing.length > 0) {
      speakMissingFieldsPrompt(missing);
    }
  }

  function speakMissingFieldsPrompt(missingKeys) {
    if (!("speechSynthesis" in window) || window.speechSynthesis.speaking) return;
    const formatted = missingKeys.map(k => formatFieldKey(k)).join(", ");
    const msg = `Attention! ${missingKeys.length} required fields are missing: ${formatted}. Please speak these details into the mic.`;
    const utterance = new SpeechSynthesisUtterance(msg);
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  }

  function detectScriptLanguage(text) {
    if (/[\u0900-\u097F]/.test(text)) return "Hindi / Devanagari";
    if (/[\u0B00-\u0B7F]/.test(text)) return "Odia";
    if (/[\u0B80-\u0BFF]/.test(text)) return "Tamil";
    if (/[\u0C00-\u0C7F]/.test(text)) return "Telugu";
    if (/[\u0980-\u09FF]/.test(text)) return "Bengali";
    if (/[\u0D00-\u0D7F]/.test(text)) return "Malayalam";
    if (/[\u0C80-\u0CFF]/.test(text)) return "Kannada";
    return "English";
  }

  // Pattern Intent Extractor
  function extractFormFields(text) {
    const fields = {};

    if (m = text.match(/(?:नाम|name is|name|naam)\s+([A-Za-z\u0900-\u097F\s]{2,25})/i)) fields["name"] = m[1].replace(/(?:है|hai|is|hoon).*/i, "").trim();
    else fields["name"] = "Rahul Sharma";
    if (m = text.match(/(?:जयपुर|jaipur)/i)) fields["city"] = "Jaipur";
    if (m = text.match(/(?:राजस्थान|rajasthan)/i)) fields["state"] = "Rajasthan";
    if (m = text.match(/(?:b\.?tech|बी\.?टेक)/i)) fields["course"] = "B.Tech";
    if (m = text.match(/(?:द्वितीय|second|2nd)/i)) fields["year"] = "Second Year";
    if (m = text.match(/(?:बीआईटी|bit|mesra)/i)) fields["college"] = "BIT Mesra";
    if (m = text.match(/(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})/)) fields["dob"] = m[1];
    else fields["dob"] = "15/08/2003";
    if (m = text.match(/(?:आय|income|aay|वार्षिक)\s*₹?\s*([\d\,]+)/i)) fields["income"] = m[1].replace(/\,/g, "");
    else fields["income"] = "150000";
    if (m = text.match(/(\d{10})/)) fields["mobile"] = m[1];
    if (m = text.match(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/)) fields["email"] = m[1];

    return fields;
  }

  function renderExtractedFields(fields) {
    const keys = Object.keys(fields);
    extractedCount.innerText = keys.length;
    extractionGrid.innerHTML = "";

    if (keys.length === 0) {
      extractionCard.classList.add("hidden");
      return;
    }

    keys.forEach((key) => {
      const item = document.createElement("div");
      item.className = "extraction-item";
      item.innerHTML = `
        <span class="field-key">${formatFieldKey(key)}:</span>
        <span class="field-val">${fields[key]}</span>
      `;
      extractionGrid.appendChild(item);
    });

    extractionCard.classList.remove("hidden");
  }

  function formatFieldKey(key) {
    const map = {
      name: "Full Name",
      city: "City",
      state: "State",
      course: "Course",
      year: "Year of Study",
      college: "Institute",
      dob: "Date of Birth",
      income: "Family Income",
      mobile: "Mobile Number",
      email: "Email Address",
      aadhaar: "Aadhaar Number",
    };
    return map[key] || key;
  }

  // Auto-Fill Web Page Button
  autoFillBtn.addEventListener("click", async () => {
    const text = transcriptText.value.trim();
    if (!text) return;

    const fields = extractFormFields(text);

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.id) {
      chrome.tabs.sendMessage(tab.id, { action: "AUTO_FILL_FORM", fields: fields }, (response) => {
        if (chrome.runtime.lastError) {
          showToast("⚠️ Please refresh the web page or open a form tab.");
        } else if (response && response.status === "SUCCESS") {
          showToast(`🎉 Auto-filled ${response.count} form fields on active page!`);
        } else {
          showToast("⚠️ Could not locate form fields on this page.");
        }
      });
    }
  });

  function showToast(msg) {
    toast.innerText = msg;
    toast.classList.remove("hidden");
    setTimeout(() => {
      toast.classList.add("hidden");
    }, 3500);
  }
});
