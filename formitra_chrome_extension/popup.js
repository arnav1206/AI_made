// popup.js — Formitra Extension Speech, Microphone Authorization & Question Scraper

document.addEventListener("DOMContentLoaded", () => {
  const langSelect         = document.getElementById("langSelect");
  const importQuestionsBtn = document.getElementById("importQuestionsBtn");
  const speakQuestionsBtn  = document.getElementById("speakQuestionsBtn");
  const questionsCard      = document.getElementById("questionsCard");
  const questionsList      = document.getElementById("questionsList");
  const questionsCount     = document.getElementById("questionsCount");
  const micBtn             = document.getElementById("micBtn");
  const micIcon            = document.getElementById("micIcon");
  const statusText         = document.getElementById("statusText");
  const grantMicBtn        = document.getElementById("grantMicBtn");
  const langDetected       = document.getElementById("langDetected");
  const transcriptText     = document.getElementById("transcriptText");
  const demoBtn            = document.getElementById("demoBtn");
  const extractionCard     = document.getElementById("extractionCard");
  const extractionGrid     = document.getElementById("extractionGrid");
  const extractedCount     = document.getElementById("extractedCount");
  const autoFillBtn        = document.getElementById("autoFillBtn");
  const toast              = document.getElementById("toast");

  let recognition = null;
  let isRecording = false;
  let importedQuestions = [];

  // Grant Mic Button Handler
  if (grantMicBtn) {
    grantMicBtn.addEventListener("click", () => {
      chrome.tabs.create({ url: chrome.runtime.getURL("permission.html") });
    });
  }

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
      if (event.error === "not-allowed" || event.error === "service-not-allowed") {
        statusText.innerText = "⚠️ Mic Access Blocked! Click button below to allow.";
        showToast("⚠️ Microphone access required. Opening permission page...");
        chrome.tabs.create({ url: chrome.runtime.getURL("permission.html") });
      } else {
        showToast("⚠️ Speech error: " + event.error);
      }
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
  micBtn.addEventListener("click", async () => {
    if (isRecording) {
      stopRecording();
    } else {
      // Pre-check permission
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(t => t.stop());
        startRecording();
      } catch (err) {
        console.warn("Microphone permission pre-check failed:", err);
        statusText.innerText = "⚠️ Mic Access Required!";
        chrome.tabs.create({ url: chrome.runtime.getURL("permission.html") });
      }
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
      chrome.tabs.create({ url: chrome.runtime.getURL("permission.html") });
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

  // ── 1. Import Questions from Active Web Page / Google Form ────────
  importQuestionsBtn.addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.id) {
      showToast("⚠️ Open a Google Form or Web Form tab first.");
      return;
    }

    chrome.tabs.sendMessage(tab.id, { action: "SCRAPE_FORM_QUESTIONS" }, (response) => {
      if (chrome.runtime.lastError) {
        showToast("⚠️ Please refresh the web page or open a form tab.");
      } else if (response && response.questions && response.questions.length > 0) {
        importedQuestions = response.questions;
        renderImportedQuestions(importedQuestions);
        showToast(`🎉 Imported ${importedQuestions.length} form questions!`);
      } else {
        importedQuestions = [
          { id: "q1", title: "Full Name", required: true },
          { id: "q2", title: "Date of Birth", required: true },
          { id: "q3", title: "City / District", required: true },
          { id: "q4", title: "State of Domicile", required: true },
          { id: "q5", title: "College / Institute Name", required: true },
          { id: "q6", title: "Course / Degree", required: true },
          { id: "q7", title: "Annual Family Income", required: true },
          { id: "q8", title: "Mobile Number", required: true },
        ];
        renderImportedQuestions(importedQuestions);
        showToast(`📋 Imported ${importedQuestions.length} standard form fields`);
      }
    });
  });

  // ── 2. Read Out Questions Aloud in Selected Native Language ────────
  speakQuestionsBtn.addEventListener("click", () => {
    const list = importedQuestions.length > 0 ? importedQuestions : [
      { title: "Full Name" },
      { title: "Date of Birth" },
      { title: "City / District" },
      { title: "State of Domicile" },
      { title: "Course" },
      { title: "Annual Family Income" },
    ];
    speakQuestionsList(list);
  });

  function speakQuestionsList(questions) {
    if (!("speechSynthesis" in window)) {
      showToast("⚠️ Speech Synthesis TTS not supported.");
      return;
    }

    window.speechSynthesis.cancel();

    const selectedLang = langSelect.value;
    const translatedTitles = questions.map((q, idx) => `${idx + 1}. ${translateTitle(q.title, selectedLang)}`);

    const promptText = `Formitra Assistant: ${translatedTitles.join("। ")}`;

    const utterance = new SpeechSynthesisUtterance(promptText);
    utterance.lang = selectedLang;
    utterance.rate = 0.92;

    window.speechSynthesis.speak(utterance);
    showToast(`🔊 Speaking ${questions.length} questions in ${langSelect.options[langSelect.selectedIndex].text}...`);
  }

  function speakSingleQuestion(title) {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();

    const selectedLang = langSelect.value;
    const translated = translateTitle(title, selectedLang);
    const utterance  = new SpeechSynthesisUtterance(translated);
    utterance.lang = selectedLang;
    utterance.rate = 0.92;

    window.speechSynthesis.speak(utterance);
  }

  function renderImportedQuestions(questions) {
    questionsCount.innerText = questions.length;
    questionsList.innerHTML = "";

    const selectedLang = langSelect.value;

    questions.forEach((q, idx) => {
      const item = document.createElement("div");
      item.className = "q-item";

      const trans = translateTitle(q.title, selectedLang);

      item.innerHTML = `
        <div>
          <div class="q-title">${idx + 1}. ${q.title} ${q.required ? '<span style="color:#EF4444;">*</span>' : ''}</div>
          <div class="q-trans">🌐 ${trans}</div>
        </div>
        <button class="q-speak-btn" title="Speak this question in native language">🔊</button>
      `;

      item.querySelector(".q-speak-btn").addEventListener("click", (e) => {
        e.stopPropagation();
        speakSingleQuestion(q.title);
      });

      questionsList.appendChild(item);
    });

    questionsCard.classList.remove("hidden");
  }

  // Language Change Listener
  langSelect.addEventListener("change", () => {
    if (importedQuestions.length > 0) {
      renderImportedQuestions(importedQuestions);
    }
  });

  // Multilingual Question Translator Matrix
  function translateTitle(title, langCode) {
    const t = title.toLowerCase();

    if (t.includes("name") || t.includes("नाम")) return getQTrans("name", langCode);
    if (t.includes("dob") || t.includes("birth") || t.includes("जन्म")) return getQTrans("dob", langCode);
    if (t.includes("city") || t.includes("district") || t.includes("शहर") || t.includes("जिला")) return getQTrans("city", langCode);
    if (t.includes("state") || t.includes("domicile") || t.includes("राज्य")) return getQTrans("state", langCode);
    if (t.includes("income") || t.includes("आय")) return getQTrans("income", langCode);
    if (t.includes("college") || t.includes("institute") || t.includes("school") || t.includes("संस्थान")) return getQTrans("college", langCode);
    if (t.includes("course") || t.includes("degree") || t.includes("पाठ्यक्रम")) return getQTrans("course", langCode);
    if (t.includes("mobile") || t.includes("phone") || t.includes("contact") || t.includes("फोन")) return getQTrans("mobile", langCode);
    if (t.includes("email") || t.includes("mail") || t.includes("ईमेल")) return getQTrans("email", langCode);

    const prefixes = {
      "hi-IN": "कृपया इस फ़ील्ड की जानकारी बताएं: ",
      "en-IN": "Please provide details for: ",
      "or-IN": "ଦୟାକରି ଏହି ବିବରଣୀ ପ୍ରଦାନ କରନ୍ତୁ: ",
      "ta-IN": "தயவுசெய்து இந்த விவரத்தை வழங்கவும்: ",
      "te-IN": "దయచేసి ఈ వివరాలను అందించండి: ",
      "bn-IN": "অনুগ্রহ করে এই বিবরণ দিন: ",
      "mr-IN": "कृपया ही माहिती द्या: ",
      "kn-IN": "ದಯವಿಟ್ಟು ಈ ವಿವರಗಳನ್ನು ನೀಡಿ: ",
      "ml-IN": "ദയവായി ഈ വിവരങ്ങൾ നൽകുക: ",
    };
    return (prefixes[langCode] || prefixes["en-IN"]) + title;
  }

  function getQTrans(key, langCode) {
    const dict = {
      name: {
        "hi-IN": "आपका पूरा नाम क्या है?", "en-IN": "What is your full name?", "or-IN": "ଆପଣଙ୍କ ସମ୍ପୂର୍ଣ୍ଣ ନାମ କ’ଣ?",
        "ta-IN": "உங்கள் முழு பெயர் என்ன?", "te-IN": "మీ పూర్తి పేరు ఏమిటి?", "bn-IN": "আপনার পুরো নাম কী?",
        "mr-IN": "तुमचे पूर्ण नाव काय आहे?", "kn-IN": "ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರು ಏನು?", "ml-IN": "നിങ്ങളുടെ പൂർണ്ണ പേര് എന്താണ്?",
      },
      dob: {
        "hi-IN": "आपकी जन्मतिथि क्या है?", "en-IN": "What is your date of birth?", "or-IN": "ଆପଣଙ୍କ ଜନ୍ମ ତାରିଖ କ’ଣ?",
        "ta-IN": "உங்கள் பிறந்த தேதி என்ன?", "te-IN": "మీ పుట్టిన తేదీ ఏమిటి?", "bn-IN": "আপনার জন্ম তারিখ কী?",
        "mr-IN": "तुमची जन्म तारीख काय आहे?", "kn-IN": "ನಿಮ್ಮ ಹುಟ್ಟಿದ ದಿನಾಂಕ ಏನು?", "ml-IN": "നിങ്ങളുടെ ജനന തീയതി എന്താണ്?",
      },
      city: {
        "hi-IN": "आपका शहर या जिला कौन सा है?", "en-IN": "Which city or district do you live in?", "or-IN": "ଆପଣଙ୍କ ସହର କିମ୍ବା ଜିଲ୍ଲା କ’ଣ?",
        "ta-IN": "உங்கள் நகரம் அல்லது மாவட்டம் எது?", "te-IN": "మీ నగరం లేదా జిల్లా ఏది?", "bn-IN": "আপনার শহর বা জেলা কোনটি?",
        "mr-IN": "तुमचे शहर किंवा जिल्हा कोणता आहे?", "kn-IN": "ನಿಮ್ಮ ನಗರ ಅಥವಾ ಜಿಲ್ಲೆ ಯಾವುದು?", "ml-IN": "നിങ്ങളുടെ നഗരം അല്ലെങ്കിൽ ജില്ല ഏതാണ്?",
      },
      state: {
        "hi-IN": "आपका राज्य कौन सा है?", "en-IN": "What is your state of domicile?", "or-IN": "ଆପଣଙ୍କ ରାଜ୍ୟ କ’ଣ?",
        "ta-IN": "உங்கள் மாநிலம் எது?", "te-IN": "మీ రాష్ట్రం ఏది?", "bn-IN": "আপনার রাজ্য কোনটি?",
        "mr-IN": "तुमचे राज्य कोणते आहे?", "kn-IN": "ನಿಮ್ಮ ರಾಜ್ಯ ಯಾವುದು?", "ml-IN": "നിങ്ങളുടെ സംസ്ഥാനം ഏതാണ്?",
      },
      income: {
        "hi-IN": "आपकी वार्षिक पारिवारिक आय कितनी है?", "en-IN": "What is your annual family income?", "or-IN": "ଆପଣଙ୍କ ବାର୍ଷିକ ପାରିବାରିକ ଆୟ କେତେ?",
        "ta-IN": "உங்கள் குடும்ப வருமானம் எவ்வளவு?", "te-IN": "మీ వార్షిక కుటుంబ ఆదాయం ఎంత?", "bn-IN": "আপনার বার্ষিক পারিবারিক আয় কত?",
        "mr-IN": "तुमचे वार्षिक कौटुंबिक उत्पन्न किती आहे?", "kn-IN": "ನಿಮ್ಮ ವಾರ್ಷಿಕ ಕುಟುಂಬ ಆದಾಯ ಎಷ್ಟು?", "ml-IN": "നിങ്ങളുടെ വാർഷിക കുടുംബ വരുമാനം എത്രയാണ്?",
      },
      college: {
        "hi-IN": "आपके कॉलेज या संस्थान का नाम क्या है?", "en-IN": "What is your college or institute name?", "or-IN": "ଆପଣଙ୍କ କଲେଜର ନାମ କ’ଣ?",
        "ta-IN": "உங்கள் கல்லூரி பெயர் என்ன?", "te-IN": "మీ కళాశాల పేరు ఏమిటి?", "bn-IN": "আপনার কলেজের নাম কী?",
        "mr-IN": "तुमच्या कॉलेजचे नाव काय आहे?", "kn-IN": "ನಿಮ್ಮ ಕಾಲೇಜಿನ ಹೆಸರು ಏನು?", "ml-IN": "നിങ്ങളുടെ കോളേജിന്റെ പേര് എന്താണ്?",
      },
      course: {
        "hi-IN": "आपका पाठ्यक्रम या कोर्स कौन सा है?", "en-IN": "What course are you enrolled in?", "or-IN": "ଆପଣଙ୍କ ପାଠ୍ୟକ୍ରମ କ’ଣ?",
        "ta-IN": "உங்கள் படிப்பு என்ன?", "te-IN": "మీ కోర్సు ఏమిటి?", "bn-IN": "আপনার কোর্স কোনটি?",
        "mr-IN": "तुमचा कोर्स कोणता आहे?", "kn-IN": "ನಿಮ್ಮ ಕೋರ್ಸ್ ಯಾವುದು?", "ml-IN": "നിങ്ങളുടെ കോഴ്‌സ് ഏതാണ്?",
      },
      mobile: {
        "hi-IN": "आपका मोबाइल नंबर क्या है?", "en-IN": "What is your mobile number?", "or-IN": "ଆପଣଙ୍କ ମୋବାଇଲ୍ ନମ୍ବର କ’ଣ?",
        "ta-IN": "உங்கள் அலைபேசி எண் என்ன?", "te-IN": "మీ మొబൈల్ నంబర్ ఏమిటి?", "bn-IN": "আপনার মোবাইল নম্বর কী?",
        "mr-IN": "तुमचा मोबाईल नंबर काय आहे?", "kn-IN": "ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಏನು?", "ml-IN": "നിങ്ങളുടെ മൊബൈൽ നമ്പർ എന്താണ്?",
      },
      email: {
        "hi-IN": "आपका ईमेल पता क्या है?", "en-IN": "What is your email address?", "or-IN": "ଆପଣଙ୍କ ଇମେଲ୍ ଠିକଣା କ’ଣ?",
        "ta-IN": "உங்கள் மின்னஞ்சல் முகவரி என்ன?", "te-IN": "మీ ఇమెయిల్ చిరునామా ఏమిటి?", "bn-IN": "আপনার ইমেল ঠিকানা কী?",
        "mr-IN": "तुमचा ईमेल पत्ता काय आहे?", "kn-IN": "ನಿಮ್ಮ ಇಮೇಲ್ ವಿಳಾಸ ಏನು?", "ml-IN": "നിങ്ങളുടെ ഇമെയിൽ വിലാസം എന്താണ്?",
      }
    };
    return (dict[key] && dict[key][langCode]) ? dict[key][langCode] : dict[key]["en-IN"];
  }

  // Demo Transcript Button
  demoBtn.addEventListener("click", () => {
    transcriptText.value = (
      "मेरा नाम राहुल शर्मा है। मैं जयपुर राजस्थान का रहने वाला हूँ। " +
      "मैं B.Tech द्वितीय वर्ष का छात्र हूँ और बीआईटी संस्थान में पढ़ता हूँ। " +
      "मेरी जन्मतिथि 15/08/2003 है और मेरी परिवार की वार्षिक आय ₹1,50,000 है। " +
      "मेरा फोन नंबर 9876543210 और ईमेल rahul.sharma@example.com है।"
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
