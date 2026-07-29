// popup.js — Formitra Extension Speech, Google Forms Scraper & Multilingual Voice Prompter

document.addEventListener("DOMContentLoaded", () => {
  const langSelect         = document.getElementById("langSelect");
  const importQuestionsBtn = document.getElementById("importQuestionsBtn");
  const speakQuestionsBtn  = document.getElementById("speakQuestionsBtn");
  const questionsCard      = document.getElementById("questionsCard");
  const questionsList      = document.getElementById("questionsList");
  const questionsCount     = document.getElementById("questionsCount");
  const importingSpinner   = document.getElementById("importingSpinner");
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
  
  // Transient single-session questions (persisted via chrome.storage.local)
  let importedQuestions = [];

  chrome.storage.local.get(["storedFormitraQuestions"], (data) => {
    if (data && data.storedFormitraQuestions && data.storedFormitraQuestions.length > 0) {
      importedQuestions = data.storedFormitraQuestions;
      if (typeof renderImportedQuestions === "function") {
        renderImportedQuestions(importedQuestions);
        if (questionsCard) questionsCard.classList.remove("hidden");
      }
    }
  });

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

    let accumTranscript = "";
    recognition.onresult = (event) => {
      let interimTranscript = "";
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          accumTranscript += event.results[i][0].transcript + " ";
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }
      const fullVoiceText = (accumTranscript + " " + interimTranscript).trim();
      if (fullVoiceText) {
        transcriptText.value = fullVoiceText;
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

  let lastMicClickTime = 0;
  micBtn.addEventListener("click", async () => {
    const now = Date.now();
    if (now - lastMicClickTime < 400) return;
    lastMicClickTime = now;

    if (isRecording) {
      stopRecording();
    } else {
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

    if (transcriptText.value.trim()) {
      triggerAutoFillFromVoice();
    }
  }

  async function triggerAutoFillFromVoice() {
    const text = transcriptText.value.trim();
    if (!text) return;

    const fields = extractFormFields(text);
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.id) {
      chrome.tabs.sendMessage(tab.id, { action: "AUTO_FILL_FORM", fields: fields }, (response) => {
        if (response && response.status === "SUCCESS") {
          showToast(`🎉 Auto-filled ${response.count} form fields from voice input!`);
        }
      });
    }
  }

  // ── 1. Import Questions & Automatically Take to Voice Input ──────────────
  importQuestionsBtn.addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.id) {
      showToast("⚠️ Open a Google Form or Web Form tab first.");
      return;
    }

    // Step 1: Display loading popup notification while importing
    showToast("⏳ Importing & Analyzing Form Questions... Please wait.");
    questionsCard.classList.remove("hidden");
    if (importingSpinner) importingSpinner.classList.remove("hidden");
    questionsList.innerHTML = "";
    importedQuestions = [];

    const nextSectionContainer = document.getElementById("nextSectionContainer");
    const importNextSectionBtn  = document.getElementById("importNextSectionBtn");

    const processResponse = (res) => {
      if (importingSpinner) importingSpinner.classList.add("hidden");

      if (res && res.questions && res.questions.length > 0) {
        importedQuestions = res.questions;
        renderImportedQuestions(importedQuestions);
        
        if (res.hasNextPage && nextSectionContainer) {
          nextSectionContainer.classList.remove("hidden");
        } else if (nextSectionContainer) {
          nextSectionContainer.classList.add("hidden");
        }

        showToast(`🎉 Imported ${importedQuestions.length} questions! Ready for voice input...`);
        
        setTimeout(() => {
          document.querySelector(".mic-section")?.scrollIntoView({ behavior: "smooth" });
          statusText.innerText = `🎙️ Ready! Speak details for ${importedQuestions.length} imported questions.`;
          micBtn.focus();
        }, 500);
      } else {
        importedQuestions = [];
        questionsCard.classList.add("hidden");
        showToast("⚠️ No question fields detected on active page.");
      }
    };

    chrome.tabs.sendMessage(tab.id, { action: "SCRAPE_FORM_QUESTIONS" }, (response) => {
      if (chrome.runtime.lastError) {
        console.warn("Injecting content.js fallback:", chrome.runtime.lastError.message);
        chrome.scripting.executeScript({
          target: { tabId: tab.id, allFrames: false },
          files: ["content.js"]
        }, () => {
          setTimeout(() => {
            chrome.tabs.sendMessage(tab.id, { action: "SCRAPE_FORM_QUESTIONS" }, (res2) => {
              processResponse(res2);
            });
          }, 350);
        });
      } else {
        processResponse(response);
      }
    });
  });

  if (document.getElementById("importNextSectionBtn")) {
    document.getElementById("importNextSectionBtn").addEventListener("click", async () => {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab) return;

      const nextSecCont = document.getElementById("nextSectionContainer");
      showToast("⏳ Navigating & importing next section...");
      chrome.tabs.sendMessage(tab.id, { action: "CLICK_NEXT_SECTION" }, () => {
        setTimeout(() => {
          chrome.tabs.sendMessage(tab.id, { action: "SCRAPE_FORM_QUESTIONS" }, (res2) => {
            if (res2 && res2.questions && res2.questions.length > 0) {
              const existingTitles = new Set(importedQuestions.map(q => q.title.toLowerCase()));
              res2.questions.forEach(q => {
                if (!existingTitles.has(q.title.toLowerCase())) {
                  importedQuestions.push(q);
                }
              });
              renderImportedQuestions(importedQuestions);
              showToast(`🎉 Imported next section! Total questions: ${importedQuestions.length}`);
              if (!res2.hasNextPage && nextSecCont) {
                nextSecCont.classList.add("hidden");
              }
            } else {
              showToast("⚠️ No additional questions found in next section.");
            }
          });
        }, 900);
      });
    });
  }

  // ── 2. Speak ONLY the Questions Given in the Imported Form ─────────────
  speakQuestionsBtn.addEventListener("click", () => {
    if (importedQuestions.length === 0) {
      showToast("⚠️ Please click '📥 Import Questions' first to scan form questions!");
      return;
    }
    speakQuestionsList(importedQuestions);
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
    showToast(`🔊 Speaking ${questions.length} form questions in ${langSelect.options[langSelect.selectedIndex].text}...`);
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
    if (chrome.storage && chrome.storage.local) {
      chrome.storage.local.set({ storedFormitraQuestions: questions });
    }
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

  // Multilingual Question Translator Matrix for Google Form Questions
  function translateTitle(title, langCode) {
    const t = title.toLowerCase();

    if (t.includes("name") || t.includes("नाम")) return getQTrans("name", langCode);
    if (t.includes("dob") || t.includes("birth") || t.includes("जन्म")) return getQTrans("dob", langCode);
    if (t.includes("city") || t.includes("district") || t.includes("town") || t.includes("शहर") || t.includes("जिला")) return getQTrans("city", langCode);
    if (t.includes("state") || t.includes("domicile") || t.includes("राज्य")) return getQTrans("state", langCode);
    if (t.includes("income") || t.includes("salary") || t.includes("आय")) return getQTrans("income", langCode);
    if (t.includes("college") || t.includes("institute") || t.includes("school") || t.includes("university") || t.includes("संस्थान") || t.includes("कॉलेज")) return getQTrans("college", langCode);
    if (t.includes("course") || t.includes("degree") || t.includes("branch") || t.includes("पाठ्यक्रम")) return getQTrans("course", langCode);
    if (t.includes("year") || t.includes("academic year") || t.includes("वर्ष")) return getQTrans("year", langCode);
    if (t.includes("mobile") || t.includes("phone") || t.includes("contact") || t.includes("फोन")) return getQTrans("mobile", langCode);
    if (t.includes("email") || t.includes("mail") || t.includes("ईमेल")) return getQTrans("email", langCode);

    const prefixes = {
      "hi-IN": "प्रश्न: " + title + " — कृपया इसका उत्तर दें",
      "en-IN": "Question: " + title + " — Please provide your answer",
      "or-IN": "ପ୍ରଶ୍ନ: " + title + " — ଦୟାକରି ଏହାର ଉତ୍ତର ଦିଅନ୍ତୁ",
      "ta-IN": "கேள்வி: " + title + " — தயவுசெய்து பதிலளிக்கவும்",
      "te-IN": "ప్రశ్న: " + title + " — దయచేసి సమాధానం ఇవ్వండి",
      "bn-IN": "প্রশ্ন: " + title + " — অনুগ্রহ করে উত্তর দিন",
      "mr-IN": "प्रश्न: " + title + " — कृपया याचे उत्तर द्या",
      "kn-IN": "ಪ್ರಶ್ನೆ: " + title + " — ದಯವಿಟ್ಟು ಉತ್ತರಿಸಿ",
      "ml-IN": "ചോദ്യം: " + title + " — ദയവായി ഉത്തരം നൽകുക",
    };
    return (prefixes[langCode] || prefixes["en-IN"]);
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
        "mr-IN": "तुमची जन्म तारीख काय आहे?", "kn-IN": "ನಿಮ್ಮ ಹುಟ್ಟಿದ ದಿನಾಂକ ಏನು?", "ml-IN": "നിങ്ങളുടെ ജനന തീയതി എന്താണ്?",
      },
      city: {
        "hi-IN": "आपका शहर या जिला कौन सा है?", "en-IN": "Which city or district do you live in?", "or-IN": "ଆପଣଙ୍କ ସହର କିମ୍ବା ଜିଲ୍ଲା କ’ଣ?",
        "ta-IN": "உங்கள் நகரம் அல்லது மாவட்டம் எது?", "te-IN": "మీ నగరం లేదా జిల్లా ఏది?", "bn-IN": "আপনার শহর বা জেলা কোনটি?",
        "mr-IN": "तुमचे शहर किंवा जिल्हा कोणता आहे?", "kn-IN": "ನಿಮ್ಮ ನಗರ किंवा जिल्हा ಯಾವುದು?", "ml-IN": "നിങ്ങളുടെ നഗരം അല്ലെങ്കിൽ ജില്ല ഏതാണ്?",
      },
      state: {
        "hi-IN": "आपका राज्य कौन सा है?", "en-IN": "What is your state of domicile?", "or-IN": "ଆପଣଙ୍କ ରାଜ୍ୟ କ’ଣ?",
        "ta-IN": "உங்கள் மாநிலம் எது?", "te-IN": "మీ రాష్ట్రం ఏది?", "bn-IN": "আপনার রাজ্য কোনটি?",
        "mr-IN": "तुमचे राज्य कोणते आहे?", "kn-IN": "ನಿಮ್ಮ રાજ્ય ಯಾವುದು?", "ml-IN": "ನಿങ്ങളുടെ സംസ്ഥാനം ഏതാണ്?",
      },
      income: {
        "hi-IN": "आपकी वार्षिक पारिवारिक आय कितनी है?", "en-IN": "What is your annual family income?", "or-IN": "ଆପଣଙ୍କ ବାର୍ଷିକ ପାରିବାରିକ ଆୟ କେତେ?",
        "ta-IN": "உங்கள் குடும்ப வருமானம் எவ்வளவு?", "te-IN": "మీ వార్షిక కుటుంబ ఆదాయం ఎంత?", "bn-IN": "আপনার বার্ষিক পারিবারিক আয় কত?",
        "mr-IN": "तुमचे वार्षिक कौटुंबिक उत्पन्न किती आहे?", "kn-IN": "<ctrl42>ನಿಮ್ಮ ವಾರ್ಷಿಕ ಕುಟುಂಬ ಆದಾಯ ಎಷ್ಟು?", "ml-IN": "നിങ്ങളുടെ വാർഷിക കുടുംബ വരുമാനം എത്രയാണ്?",
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
      year: {
        "hi-IN": "आपका अध्ययन का वर्ष कौन सा है?", "en-IN": "What is your year of study?", "or-IN": "ଆପଣଙ୍କ ପାଠପଢ଼ା ବର୍ଷ କ’ଣ?",
        "ta-IN": "உங்கள் படிப்பு ஆண்டு என்ன?", "te-IN": "మీ చదువు సంవత్సరం ఏమిటి?", "bn-IN": "আপনার অধ্যয়নের বছর কোনটি?",
        "mr-IN": "तुमचे अभ्यासाचे वर्ष कोणते आहे?", "kn-IN": "ನಿಮ್ಮ ಅಧ್ಯಯನದ ವರ್ಷ ಯಾವುದು?", "ml-IN": "നിങ്ങളുടെ പഠന വർഷം ഏതാണ്?",
      },
      mobile: {
        "hi-IN": "आपका मोबाइल नंबर क्या है?", "en-IN": "What is your mobile number?", "or-IN": "ଆପଣଙ୍କ ମୋବାଇଲ୍ ନମ୍ବର କ’ଣ?",
        "ta-IN": "உங்கள் அலைபேசி எண் என்ன?", "te-IN": "మీ మొబైల్ నంబర్ ఏమిటి?", "bn-IN": "আপনার মোবাইল নম্বর কী?",
        "mr-IN": "तुमचा मोबाईल नंबर काय आहे?", "kn-IN": "ನಿಮ್ಮ ಮೊಬೈଲ୍ ಸಂಖ್ಯೆ ಏನು?", "ml-IN": "നിങ്ങളുടെ മൊബൈൽ നമ്പർ എന്താണ്?",
      },
      email: {
        "hi-IN": "आपका ईमेल पता क्या है?", "en-IN": "What is your email address?", "or-IN": "ଆପଣଙ୍କ ଇମେଲ୍ ଠିକଣା କ’ଣ?",
        "ta-IN": "உங்கள் மின்னஞ்சல் முகவரி என்ன?", "te-IN": "మీ ఇమెయિલ చిరుနာమా ఏమిటి?", "bn-IN": "আপনার ইমেল ঠিকানা কী?",
        "mr-IN": "तुमचा ईमेल पत्ता काय आहे?", "kn-IN": "ನಿಮ್ಮ ഇಮೇൽ വിളಾಸ ಏನು?", "ml-IN": "നിങ്ങളുടെ ഇമെയിൽ വിലാസം എന്താണ്?",
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

  // Pattern Intent Extractor (Expanded NLP Entity Extractor)
  function extractFormFields(text) {
    const fields = {};
    let m;

    // Name
    if (m = text.match(/(?:नाम|name is|name|naam|applicant|candidate)\s+([A-Za-z\u0900-\u097F\s]{2,30})/i)) {
      fields["name"] = m[1].replace(/(?:है|hai|is|hoon|and|category|gender|male|female).*/i, "").trim();
    }
    // Gender
    if (m = text.match(/(?:gender|sex|लिंग)\s*[:\-]?\s*(male|female|transgender|पुरुष|महिला)/i) || text.match(/\b(male|female|transgender|पुरुष|महिला)\b/i)) {
      const rawG = m[1].toLowerCase();
      if (rawG === "female" || rawG === "महिला") fields["gender"] = "Female";
      else if (rawG === "male" || rawG === "पुरुष") fields["gender"] = "Male";
      else fields["gender"] = "Transgender";
    }
    // Category
    if (m = text.match(/(?:category|caste|वर्ग|श्रेणी)\s*[:\-]?\s*(general|obc|sc|st|ews|सामान्य|ओबीसी)/i) || text.match(/\b(general|obc|sc|st|ews|सामान्य|ओबीसी)\b/i)) {
      const rawC = m[1].toUpperCase();
      if (rawC.includes("OBC") || rawC.includes("ओबीसी")) fields["category"] = "OBC";
      else if (rawC.includes("SC")) fields["category"] = "SC";
      else if (rawC.includes("ST")) fields["category"] = "ST";
      else if (rawC.includes("EWS")) fields["category"] = "EWS / EBC";
      else fields["category"] = "General";
    }
    // City
    if (m = text.match(/(?:city|district|शहर|जिला)\s*[:\-]?\s*([A-Za-z\u0900-\u097F\s]{2,20})/i) || text.match(/(?:जयपुर|jaipur|दिल्ली|delhi|भुवनेश्वर|bhubaneswar|ranchi|patna|mumbai)/i)) {
      fields["city"] = m[1] || m[0];
    }
    // State
    if (m = text.match(/(?:state|domicile|राज्य)\s*[:\-]?\s*([A-Za-z\u0900-\u097F\s]{2,20})/i) || text.match(/(?:राजस्थान|rajasthan|ओडिशा|odisha|jharkhand|bihar|maharashtra|uttar pradesh)/i)) {
      fields["state"] = m[1] || m[0];
    }
    // Course
    if (m = text.match(/(?:b\.?tech|बी\.?टेक|b\.?sc|m\.?tech|mba|diploma|b.a|m.a)/i)) {
      fields["course"] = m[0].toUpperCase();
    }
    // Year
    if (m = text.match(/(?:first|second|third|fourth|1st|2nd|3rd|4th|प्रथम|द्वितीय|तृतीय)\s*(?:year|वर्ष)?/i)) {
      const rawY = m[0].toLowerCase();
      if (rawY.includes("1st") || rawY.includes("first") || rawY.includes("प्रथम")) fields["year"] = "First Year";
      else if (rawY.includes("3rd") || rawY.includes("third") || rawY.includes("तृतीय")) fields["year"] = "Third Year";
      else if (rawY.includes("4th") || rawY.includes("fourth")) fields["year"] = "Fourth Year";
      else fields["year"] = "Second Year";
    }
    // College
    if (m = text.match(/(?:college|institute|university|school|संस्थान|कॉलेज)\s*[:\-]?\s*([A-Za-z\u0900-\u097F\s]{2,30})/i) || text.match(/(?:bit\s*mesra|jaipur\s*national|iit|nit)/i)) {
      fields["college"] = m[1] || m[0];
    }
    // DOB
    if (m = text.match(/(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})/)) fields["dob"] = m[1];
    // Income
    if (m = text.match(/(?:आय|income|aay|वार्षिक)\s*₹?\s*([\d\,]+)/i)) fields["income"] = m[1].replace(/\,/g, "");
    else if (m = text.match(/([\d\.]+)\s*(?:lakh|lakhs|लाख)/i)) {
      const num = parseFloat(m[1]) * 100000;
      fields["income"] = String(Math.round(num));
    }
    // Mobile
    if (m = text.match(/(\d{10})/)) fields["mobile"] = m[1];
    // Email
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

  // ── 3. Auto-Fill Form & Transient Delete Session Questions ──────────────
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
          showToast(`🎉 Auto-filled ${response.count} fields & deleted session questions!`);
          
          // Clear and delete imported questions after completion for single-session privacy
          importedQuestions = [];
          questionsCard.classList.add("hidden");
          transcriptText.value = "";
          extractionCard.classList.add("hidden");
          autoFillBtn.disabled = true;
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
