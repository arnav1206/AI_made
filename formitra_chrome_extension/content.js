// content.js — Formitra Web Form Auto-Filler Engine, Google Forms Scraper & Target Form Language Transliteration Engine

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "AUTO_FILL_FORM") {
    const fields = request.fields || {};
    const filledCount = fillPageFormFields(fields);
    sendResponse({ status: "SUCCESS", count: filledCount });
  } else if (request.action === "TRIGGER_FIELD_DICTATION") {
    openFloatingFormitraWidget();
    sendResponse({ status: "STARTED" });
  } else if (request.action === "SCRAPE_FORM_QUESTIONS") {
    if (window.self !== window.top) {
      sendResponse({ status: "SUCCESS", questions: [], hasNextPage: false });
      return true;
    }
    const questions = scrapePageQuestions();
    const hasNext = detectNextPageButton();
    sendResponse({ status: "SUCCESS", questions: questions, hasNextPage: hasNext });
  } else if (request.action === "CLICK_NEXT_SECTION") {
    const clicked = clickNextPageButton();
    sendResponse({ status: clicked ? "SUCCESS" : "FAILED" });
  }
  return true;
});

// Inject Floating Formitra Mic Widget on every webpage containing form inputs
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initExtensionWidget);
} else {
  initExtensionWidget();
}

function initExtensionWidget() {
  setTimeout(maybeInjectFloatingWidget, 800);
}

function maybeInjectFloatingWidget() {
  if (document.getElementById("formitra-floating-btn")) return;

  const isGoogleForms = window.location.href.includes("docs.google.com/forms");
  const inputs = document.querySelectorAll("input, select, textarea, [role='listitem'], [role='textbox']");

  if (inputs.length === 0 && !isGoogleForms) return;

  const btn = document.createElement("button");
  btn.id = "formitra-floating-btn";
  btn.innerHTML = isGoogleForms ? "🎙️ Formitra Google Forms Auto-Fill" : "🎙️ Formitra Voice Auto-Fill";
  btn.title = "Click to dictate & auto-fill this web form in your native language";
  btn.style.cssText = `
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 999999;
    background: linear-gradient(135deg, #FF7A00, #EA580C);
    color: #FFFFFF;
    border: 2px solid #FFFFFF;
    padding: 10px 18px;
    border-radius: 50px;
    font-weight: 800;
    font-size: 13px;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(255, 122, 0, 0.45);
    transition: all 0.3s ease;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  `;

  btn.addEventListener("mouseenter", () => {
    btn.style.transform = "scale(1.06) translateY(-2px)";
  });
  btn.addEventListener("mouseleave", () => {
    btn.style.transform = "scale(1) translateY(0)";
  });
  btn.addEventListener("click", openFloatingFormitraWidget);

  document.body.appendChild(btn);
}

function openFloatingFormitraWidget() {
  let modal = document.getElementById("formitra-floating-modal");
  if (modal) {
    modal.style.display = modal.style.display === "none" ? "block" : "none";
    return;
  }

  modal = document.createElement("div");
  modal.id = "formitra-floating-modal";
  modal.style.cssText = `
    position: fixed;
    bottom: 80px;
    right: 24px;
    width: 360px;
    z-index: 999999;
    background: #0F172A;
    color: #F8FAFC;
    border: 2px solid #FF7A00;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  `;

  const isGF = window.location.href.includes("docs.google.com/forms");
  const titleText = isGF ? "🎙️ Formitra Google Forms Assistant" : "🎙️ Formitra Screen Voice Assistant";

  modal.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
      <div style="font-weight:800;font-size:14px;color:#FF7A00;">${titleText}</div>
      <button id="fmt-close-btn" style="background:none;border:none;color:#94A3B8;font-size:16px;cursor:pointer;font-weight:bold;">✕</button>
    </div>
    <div style="display:flex;gap:6px;margin-bottom:10px;">
      <button id="fmt-scrape-btn" style="flex:1;background:rgba(255,122,0,0.2);color:#FF7A00;border:1px solid #FF7A00;padding:6px;border-radius:6px;font-size:11px;font-weight:bold;cursor:pointer;">📥 Import Questions</button>
      <button id="fmt-speak-btn" style="flex:1;background:rgba(37,99,235,0.2);color:#60A5FA;border:1px solid #60A5FA;padding:6px;border-radius:6px;font-size:11px;font-weight:bold;cursor:pointer;">🔊 Read Questions</button>
    </div>
    <div id="fmt-q-status" style="font-size:11px;color:#34D399;margin-bottom:8px;display:none;font-weight:bold;"></div>
    <div style="font-size:12px;color:#CBD5E1;margin-bottom:6px;">Speak in your native language to auto-fill the form:</div>
    <textarea id="fmt-modal-text" style="width:100%;height:85px;background:#1E293B;color:#FFF;border:1px solid rgba(255,122,0,0.4);border-radius:8px;padding:8px;font-size:12px;box-sizing:border-box;margin-bottom:10px;" placeholder="Press mic to speak or paste transcript..."></textarea>
    <div style="display:flex;gap:8px;">
      <button id="fmt-mic-toggle" style="flex:1;background:#FF7A00;color:#FFF;border:none;padding:9px;border-radius:8px;font-weight:bold;font-size:12px;cursor:pointer;">🎙️ Start Mic</button>
      <button id="fmt-fill-action" style="flex:1;background:#059669;color:#FFF;border:none;padding:9px;border-radius:8px;font-weight:bold;font-size:12px;cursor:pointer;">✨ Auto-Fill Form</button>
    </div>
  `;

  document.body.appendChild(modal);

  document.getElementById("fmt-close-btn").addEventListener("click", () => {
    modal.style.display = "none";
  });

  let pageQuestions = [];

  document.getElementById("fmt-scrape-btn").addEventListener("click", () => {
    const statusDiv = document.getElementById("fmt-q-status");
    statusDiv.style.display = "block";
    statusDiv.innerText = "⏳ Importing Questions...";

    setTimeout(() => {
      pageQuestions = scrapePageQuestions();
      statusDiv.innerText = `📋 Imported ${pageQuestions.length} questions from Google Form!`;
    }, 200);
  });

  document.getElementById("fmt-speak-btn").addEventListener("click", () => {
    if (pageQuestions.length === 0) {
      pageQuestions = scrapePageQuestions();
    }
    const qList = pageQuestions.map((q, idx) => `${idx + 1}. ${q.title}`);
    const textToSpeak = `Formitra Google Forms Assistant: ${qList.join("। ")}`;

    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      const utt = new SpeechSynthesisUtterance(textToSpeak);
      utt.rate = 0.92;
      window.speechSynthesis.speak(utt);
    }
  });

  let rec = null;
  let recActive = false;
  const micToggle = document.getElementById("fmt-mic-toggle");
  const modalText = document.getElementById("fmt-modal-text");

  let accumStr = "";
  micToggle.addEventListener("click", () => {
    if (recActive && rec) {
      rec.stop();
      recActive = false;
      micToggle.innerText = "🎙️ Start Mic";
      micToggle.style.background = "#FF7A00";
    } else {
      if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        rec = new SR();
        rec.continuous = true;
        rec.interimResults = true;
        rec.lang = "hi-IN";

        rec.onresult = (e) => {
          let interimStr = "";
          for (let i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
              accumStr += e.results[i][0].transcript + " ";
            } else {
              interimStr += e.results[i][0].transcript;
            }
          }
          const fullText = (accumStr + " " + interimStr).trim();
          if (fullText) {
            modalText.value = fullText;
          }
        };

        rec.start();
        recActive = true;
        micToggle.innerText = "⏹️ Stop Mic";
        micToggle.style.background = "#EF4444";
      } else {
        alert("Speech Recognition is not supported in this browser window.");
      }
    }
  });

  document.getElementById("fmt-fill-action").addEventListener("click", () => {
    const text = modalText.value.trim();
    if (!text) {
      alert("⚠️ Please speak or paste transcript text first.");
      return;
    }

    const fields = extractFormFieldsFromText(text);
    const count  = fillPageFormFields(fields);
    alert(`🎉 Formitra auto-filled ${count} form fields on this Google Form!`);
    modal.style.display = "none";
  });
}

// ── Multi-Strategy Google Forms & Web Form Question Extractor ────────
function scrapePageQuestions() {
  const questions = [];
  const isGoogleForms = window.location.href.includes("docs.google.com/forms");

  if (isGoogleForms) {
    // Each question in Google Forms is wrapped inside a role="listitem" container card
    const questionCards = document.querySelectorAll('div[role="listitem"], .ge2dfc, .o3b8eb, div[jsmodel]');

    questionCards.forEach((card, idx) => {
      const headingElem = card.querySelector('.M7eMe, [role="heading"], .freebirdFormviewerComponentsQuestionBaseHeaderTitle, .HoLwm');
      if (!headingElem) return;

      let rawText = headingElem.innerText || headingElem.textContent || "";
      if (rawText.includes("\n")) rawText = rawText.split("\n")[0];
      let cleanText = rawText.replace(/\*/g, "").trim();

      const lower = cleanText.toLowerCase();

      if (
        cleanText &&
        cleanText.length >= 2 &&
        !lower.includes("submit") &&
        !lower.includes("clear form") &&
        !lower.includes("never submit passwords") &&
        !lower.includes("report abuse") &&
        !questions.some(q => q.title.toLowerCase() === lower)
      ) {
        const isReq = card.innerText.includes("*") || card.querySelector('.codefx, [aria-label*="required"]') !== null;

        questions.push({
          id: `gf_q_${idx}`,
          title: cleanText,
          required: isReq,
        });
      }
    });

    if (questions.length === 0) {
      const gfHeaders = document.querySelectorAll('.M7eMe');
      gfHeaders.forEach((hElem, idx) => {
        let rawText = hElem.innerText || hElem.textContent || "";
        if (rawText.includes("\n")) rawText = rawText.split("\n")[0];
        let cleanText = rawText.replace(/\*/g, "").trim();
        const lower = cleanText.toLowerCase();

        if (cleanText && cleanText.length >= 2 && !questions.some(q => q.title.toLowerCase() === lower)) {
          questions.push({
            id: `gf_header_${idx}`,
            title: cleanText,
            required: false,
          });
        }
      });
    }

    return questions;
  }

  // ── Standard Web Form Scraper (Non-Google Forms) ───────────────────
  const inputs = document.querySelectorAll("input, select, textarea");
  inputs.forEach((inp, idx) => {
    if (inp.type === "hidden" || inp.type === "submit" || inp.type === "button" || inp.type === "checkbox" || inp.type === "radio") return;

    const labelText  = getFieldLabelText(inp).replace(/\*/g, "").trim();
    const placeholder = inp.placeholder || inp.name || inp.id || inp.getAttribute("aria-label") || "";
    const displayTitle = labelText || placeholder;

    if (displayTitle && displayTitle.length >= 2 && !questions.some(q => q.title.toLowerCase() === displayTitle.toLowerCase())) {
      questions.push({
        id: `inp_q_${idx}`,
        title: displayTitle,
        required: inp.required || labelText.includes("*"),
      });
    }
  });

  return questions;
}

function extractFormFieldsFromText(text) {
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
  // Attendees / Guest Count
  if (m = text.match(/(?:हम|we|are)?\s*(एक|दो|तीन|चार|पांच|छह|सात|आठ|नौ|दस|\d+)\s*(?:लोग|person|people|guest|guests|attend|अटैंड)/i) || text.match(/(\d+)\s*(?:लोग|people|guests)/i)) {
    const wordMap = { "एक": "1", "दो": "2", "तीन": "3", "चार": "4", "पांच": "5", "छह": "6", "सात": "7", "आठ": "8", "नौ": "9", "दस": "10" };
    const rawNum = m[1].toLowerCase();
    fields["attendees"] = wordMap[rawNum] || rawNum;
  }
  // Dietary Restrictions / Allergies
  if (m = text.match(/(?:allergy|allergies|एलर्जी|diet|food)\s*[:\-]?\s*([^\n\.]+)/i) || text.match(/(?:कोई\s*एलर्जी\s*नहीं|no\s*allergy|no\s*allergies|none)/i)) {
    const rawA = m[0].toLowerCase();
    if (rawA.includes("कोई नहीं") || rawA.includes("कोई एलर्जी नहीं") || rawA.includes("no") || rawA.includes("none")) {
      fields["allergies"] = "None (कोई एलर्जी नहीं)";
    } else {
      fields["allergies"] = m[1] || m[0];
    }
  }
  // RSVP Attendance
  if (m = text.match(/(?:अटैंड\s*करेंगे|will\s*attend|attending|coming|yes|हाँ)/i)) {
    fields["rsvp"] = "Yes (अटैंड करेंगे)";
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

// ── Target Form Language Detector & Transliteration Engine ──────────────
function detectFormTargetLanguage() {
  const formHeadings = Array.from(document.querySelectorAll('.M7eMe, label, [role="heading"], h1, h2, h3, .HoLwm'))
    .map(el => el.innerText || "")
    .join(" ");

  if (/[\u0900-\u097F]/.test(formHeadings)) return "Hindi";
  if (/[\u0B00-\u0B7F]/.test(formHeadings)) return "Odia";
  if (/[\u0B80-\u0BFF]/.test(formHeadings)) return "Tamil";
  if (/[\u0C00-\u0C7F]/.test(formHeadings)) return "Telugu";
  if (/[\u0980-\u09FF]/.test(formHeadings)) return "Bengali";
  if (/[\u0D00-\u0D7F]/.test(formHeadings)) return "Malayalam";
  if (/[\u0C80-\u0CFF]/.test(formHeadings)) return "Kannada";

  return "English";
}

const DEVANAGARI_TO_ENGLISH_DICT = {
  "राहुल": "Rahul",
  "शर्मा": "Sharma",
  "राहुल शर्मा": "Rahul Sharma",
  "जयपुर": "Jaipur",
  "राजस्थान": "Rajasthan",
  "बी.टेक": "B.Tech",
  "बीटेक": "B.Tech",
  "द्वितीय वर्ष": "Second Year",
  "द्वितीय": "Second",
  "प्रथम वर्ष": "First Year",
  "तृतीय वर्ष": "Third Year",
  "अंतिम वर्ष": "Final Year",
  "बीआईटी": "BIT Mesra",
  "पुरुष": "Male",
  "महिला": "Female",
  "सामान्य": "General",
  "ओबीसी": "OBC",
  "अनुसूचित जाति": "SC",
  "अनुसूचित जनजाति": "ST"
};

const ENGLISH_TO_NATIVE_DICT = {
  "city": {
    "Jaipur": { Hindi: "जयपुर", Odia: "ଜୟପୁର", Tamil: "ஜெய்பூர்", Telugu: "జైపూర్", Bengali: "জয়পুর", Marathi: "जयपूर", Kannada: "ಜೈಪುರ", Malayalam: "ജയ്പൂർ", English: "Jaipur" },
    "Delhi": { Hindi: "दिल्ली", Odia: "ଦିଲ୍ଲୀ", Tamil: "டெல்லி", Telugu: "ఢిల్లీ", Bengali: "দিল্লি", Marathi: "दिल्ली", Kannada: "ದೆಹಲಿ", Malayalam: "ഡൽഹി", English: "Delhi" },
    "Bhubaneswar": { Hindi: "भुवनेश्वर", Odia: "ଭୁବନେଶ୍ୱର", Tamil: "ପୁବନେଶ୍ବର", Telugu: "భువనేశ్వర్", Bengali: "ଭୁବନେଶ୍ୱର", Marathi: "भुवनेश्वर", Kannada: "ಭುವನೇಶ್ವರ", Malayalam: "ഭുവനേശ്വർ", English: "Bhubaneswar" }
  },
  "state": {
    "Rajasthan": { Hindi: "राजस्थान", Odia: "ରାଜସ୍ଥାନ", Tamil: "ராஜஸ்தான்", Telugu: "రాజస్థాన్", Bengali: "রাজস্থান", Marathi: "राजस्थान", Kannada: "ರಾಜಸ್ಥಾನ", Malayalam: "രാജസ്ഥാൻ", English: "Rajasthan" },
    "Odisha": { Hindi: "ओडिशा", Odia: "ଓଡ଼િଶା", Tamil: "ஒடிசா", Telugu: "ఒడిషా", Bengali: "ওড়িশা", Marathi: "ओडिशा", Kannada: "ಒಡಿಶಾ", Malayalam: "ഒഡീഷ", English: "Odisha" }
  },
  "year": {
    "Second Year": { Hindi: "द्वितीय वर्ष", Odia: "ଦ୍ୱିତୀୟ ବର୍ଷ", Tamil: "இரண்டாம் ஆண்டு", Telugu: "రెండవ సంవత్సరం", Bengali: "দ্বিতীয় বর্ষ", Marathi: "दुसरे वर्ष", Kannada: "ಎರಡನೇ ವರ್ಷ", Malayalam: "രണ്ടാം വർഷം", English: "Second Year" }
  },
  "course": {
    "B.Tech": { Hindi: "बी.टेक", Odia: "ବି.ଟେକ୍", Tamil: "பி.டெக்", Telugu: "బి.టెక్", Bengali: "বি.টেক", Marathi: "बी.टेक", Kannada: "ಬಿ.ಟೆಕ್", Malayalam: "ബി.ടെക്", English: "B.Tech" }
  },
  "category": {
    "General": { Hindi: "सामान्य", Odia: "ସାଧାରଣ", Tamil: "பொது", Telugu: "సాధారణ", Bengali: "সাধারণ", Marathi: "सामान्य", Kannada: "ಸಾಮಾನ್ಯ", Malayalam: "ജനറൽ", English: "General" }
  },
  "gender": {
    "Male": { Hindi: "पुरुष", Odia: "ପୁରୁଷ", Tamil: "ஆண்", Telugu: "పురుషుడు", Bengali: "পুরুষ", Marathi: "पुरुष", Kannada: "ಪುರುಷ", Malayalam: "ആൺ", English: "Male" }
  }
};

function devanagariPhoneticToEnglish(text) {
  if (!text) return text;
  let str = text;
  Object.keys(DEVANAGARI_TO_ENGLISH_DICT).forEach(k => {
    str = str.replace(new RegExp(k, "g"), DEVANAGARI_TO_ENGLISH_DICT[k]);
  });

  const charMap = {
    'क':'k','ख':'kh','ग':'g','घ':'gh','ङ':'n',
    'च':'ch','छ':'chh','ज':'j','झ':'jh','ञ':'n',
    'ट':'t','ठ':'th','ड':'d','ढ':'dh','ण':'n',
    'त':'t','थ':'th','द':'d','ध':'dh','न':'n',
    'प':'p','फ':'ph','ब':'b','भ':'bh','म':'m',
    'य':'y','र':'r','ल':'l','व':'v','श':'sh','ष':'sh','स':'s','ह':'h',
    'ा':'a','ि':'i','ी':'ee','ु':'u','ू':'oo','े':'e','ै':'ai','ो':'o','ौ':'au',
    '्':'','ं':'n','ः':'h','अ':'A','आ':'Aa','इ':'I','ई':'Ee','उ':'U','ऊ':'Oo','ए':'E','ऐ':'Ai','ओ':'O','औ':'Au'
  };

  let out = "";
  for (let ch of str) {
    if (charMap[ch] !== undefined) out += charMap[ch];
    else out += ch;
  }
  return out.replace(/\b\w/g, c => c.toUpperCase()).trim();
}

function transliterateToTargetFormLanguage(key, rawVal, targetFormLang) {
  if (!rawVal) return rawVal;

  if (targetFormLang === "English") {
    if (/[^\x00-\x7F]/.test(rawVal)) {
      return devanagariPhoneticToEnglish(rawVal);
    }
    return rawVal;
  } else {
    if (ENGLISH_TO_NATIVE_DICT[key] && ENGLISH_TO_NATIVE_DICT[key][rawVal]) {
      const nativeVal = ENGLISH_TO_NATIVE_DICT[key][rawVal][targetFormLang];
      if (nativeVal) return nativeVal;
    }
    return rawVal;
  }
}

function forceClickGoogleFormsOption(optElement) {
  if (!optElement) return;

  if (optElement.getAttribute("aria-checked") !== null) {
    optElement.setAttribute("aria-checked", "true");
  }
  if ("checked" in optElement) {
    optElement.checked = true;
  }

  const targets = [optElement, optElement.parentElement, optElement.firstElementChild].filter(Boolean);
  targets.forEach(target => {
    try { target.focus(); } catch(e) {}
    try { target.click(); } catch(e) {}

    const opts = { bubbles: true, cancelable: true, composed: true };
    target.dispatchEvent(new MouseEvent("mousedown", opts));
    target.dispatchEvent(new MouseEvent("mouseup", opts));
    target.dispatchEvent(new MouseEvent("click", opts));
    target.dispatchEvent(new Event("change", opts));
    target.dispatchEvent(new Event("input", opts));
  });
}

function fillPageFormFields(fields) {
  let count = 0;

  const targetFormLang = detectFormTargetLanguage();
  console.log(`🌐 Formitra Target Form Language: ${targetFormLang}`);

  const formattedFields = {
    name: transliterateToTargetFormLanguage("name", fields.name, targetFormLang),
    city: transliterateToTargetFormLanguage("city", fields.city, targetFormLang),
    state: transliterateToTargetFormLanguage("state", fields.state, targetFormLang),
    course: transliterateToTargetFormLanguage("course", fields.course, targetFormLang),
    year: transliterateToTargetFormLanguage("year", fields.year, targetFormLang),
    college: transliterateToTargetFormLanguage("college", fields.college, targetFormLang),
    dob: fields.dob,
    income: fields.income,
    mobile: fields.mobile,
    email: fields.email,
    gender: transliterateToTargetFormLanguage("gender", fields.gender, targetFormLang),
    category: transliterateToTargetFormLanguage("category", fields.category, targetFormLang),
    attendees: fields.attendees,
    allergies: fields.allergies,
    rsvp: fields.rsvp,
    comments: fields.comments,
  };

  // ── 1. Dedicated Google Forms Deep Auto-Fill Engine ────────────────
  const isGoogleForms = window.location.href.includes("docs.google.com/forms");
  if (isGoogleForms) {
    const gfQuestions = document.querySelectorAll('div[role="listitem"], div[jsmodel], .ge2dfc, .QrT82d, .freebirdFormviewerComponentsQuestionBaseRoot, .o3b8eb');
    
    gfQuestions.forEach((qContainer) => {
      const titleElem = qContainer.querySelector('.M7eMe, [role="heading"], .HoLwm, .freebirdFormviewerComponentsQuestionBaseHeaderTitle, span');
      if (!titleElem) return;

      const qTitle = titleElem.innerText.toLowerCase();

      const textInput = qContainer.querySelector('input[type="text"], input[type="email"], input[type="tel"], input[type="number"], input[type="date"], textarea, [role="textbox"]');
      
      let valToSet = null;
      if (matchRule(qTitle, ["name", "full name", "applicant name", "candidate name", "first name", "last name", "नाम", "पूरा नाम"])) valToSet = formattedFields.name;
      else if (matchRule(qTitle, ["city", "town", "district", "शहर", "जिला"])) valToSet = formattedFields.city;
      else if (matchRule(qTitle, ["state", "domicile", "राज्य"])) valToSet = formattedFields.state;
      else if (matchRule(qTitle, ["income", "annual income", "family income", "आय", "वार्षिक आय"])) valToSet = formattedFields.income;
      else if (matchRule(qTitle, ["course", "degree", "program", "branch", "पाठ्यक्रम"])) valToSet = formattedFields.course;
      else if (matchRule(qTitle, ["year", "academic year", "year of study", "वर्ष"])) valToSet = formattedFields.year;
      else if (matchRule(qTitle, ["college", "institute", "school", "university", "संस्थान", "कॉलेज"])) valToSet = formattedFields.college;
      else if (matchRule(qTitle, ["dob", "date of birth", "birth date", "birthdate", "जन्मतिथि"])) valToSet = formattedFields.dob;
      else if (matchRule(qTitle, ["mobile", "phone", "contact", "फोन", "मोबाइल"])) valToSet = formattedFields.mobile;
      else if (matchRule(qTitle, ["email", "e-mail", "ईमेल"])) valToSet = formattedFields.email;
      else if (matchRule(qTitle, ["attend", "attendees", "people", "guests", "number of", "how many", "कितने लोग", "लोग"])) valToSet = formattedFields.attendees;
      else if (matchRule(qTitle, ["allergy", "allergies", "diet", "dietary", "food", "एलर्जी", "खान-पान"])) valToSet = formattedFields.allergies;
      else if (matchRule(qTitle, ["rsvp", "attend", "coming", "भाग लेंगे", "उपस्थित"])) valToSet = formattedFields.rsvp;
      else if (matchRule(qTitle, ["comment", "remark", "note", "message", "टिप्पणी", "संदेश"])) valToSet = formattedFields.comments;

      if (textInput && valToSet !== null && valToSet !== undefined) {
        setGoogleFormsInputValue(textInput, valToSet);
        highlightFilledInput(textInput, valToSet);
        count++;
        return;
      }

      const options = qContainer.querySelectorAll('[role="radio"], [role="checkbox"], [role="option"], input[type="radio"], input[type="checkbox"], label, div[data-value]');
      if (options.length > 0) {
        let targetVal = null;
        if (matchRule(qTitle, ["gender", "sex", "लिंग"])) targetVal = formattedFields.gender;
        else if (matchRule(qTitle, ["category", "caste", "वर्ग", "श्रेणी"])) targetVal = formattedFields.category;
        else if (matchRule(qTitle, ["course", "degree"])) targetVal = formattedFields.course;
        else if (matchRule(qTitle, ["year", "academic year"])) targetVal = formattedFields.year;
        else if (matchRule(qTitle, ["state", "domicile"])) targetVal = formattedFields.state;

        const checkTargets = targetVal ? [targetVal] : [formattedFields.gender, formattedFields.category, formattedFields.course, formattedFields.year, formattedFields.state].filter(Boolean);

        let optionMatched = false;
        options.forEach((opt) => {
          if (optionMatched && (opt.getAttribute("role") === "radio" || opt.getAttribute("role") === "checkbox")) return;

          const parentText = opt.parentElement ? opt.parentElement.innerText : "";
          const ariaLabel = opt.getAttribute("aria-label") || "";
          const dataVal = opt.getAttribute("data-value") || "";
          const elemText = opt.innerText || opt.value || "";

          const combinedText = `${elemText} ${ariaLabel} ${dataVal} ${parentText}`.toLowerCase();

          for (let tVal of checkTargets) {
            const searchVal = tVal.toLowerCase().trim();
            if (searchVal && searchVal.length >= 2 && combinedText.includes(searchVal)) {
              const clickTarget = opt.closest('[role="checkbox"], [role="radio"]') || opt.querySelector('[role="checkbox"], [role="radio"]') || opt;
              forceClickGoogleFormsOption(clickTarget);
              highlightFilledInput(clickTarget, tVal);
              count++;
              optionMatched = true;
              break;
            }
          }
        });
      }
    });

    if (count > 0) return count;
  }

  // ── 2. Standard Web Form & Streamlit Scanner ───────────────────────
  const inputs = document.querySelectorAll("input, select, textarea");
  inputs.forEach((input) => {
    if (input.type === "hidden" || input.type === "submit" || input.type === "button") return;

    const labelText  = getFieldLabelText(input).toLowerCase();
    const attrText   = `${input.name || ''} ${input.id || ''} ${input.placeholder || ''} ${input.getAttribute('aria-label') || ''}`.toLowerCase();
    const fullSearch = `${labelText} ${attrText}`;

    let valToSet = null;

    if (matchRule(fullSearch, ["name", "full name", "applicant name", "candidate name", "नाम"])) valToSet = formattedFields.name;
    else if (matchRule(fullSearch, ["city", "town", "district", "शहर"])) valToSet = formattedFields.city;
    else if (matchRule(fullSearch, ["state", "domicile", "राज्य"])) valToSet = formattedFields.state;
    else if (matchRule(fullSearch, ["income", "annual income", "family income", "आय"])) valToSet = formattedFields.income;
    else if (matchRule(fullSearch, ["course", "degree", "program", "पाठ्यक्रम"])) valToSet = formattedFields.course;
    else if (matchRule(fullSearch, ["year", "academic year", "वर्ष"])) valToSet = formattedFields.year;
    else if (matchRule(fullSearch, ["college", "institute", "school", "university", "संस्थान"])) valToSet = formattedFields.college;
    else if (matchRule(fullSearch, ["dob", "date of birth", "birth date", "जन्मतिथि"])) valToSet = formattedFields.dob;
    else if (matchRule(fullSearch, ["mobile", "phone", "contact", "फोन"])) valToSet = formattedFields.mobile;
    else if (matchRule(fullSearch, ["email", "e-mail", "ईमेल"])) valToSet = formattedFields.email;

    if (input.type === "checkbox" || input.type === "radio") {
      const valStr = `${labelText} ${input.value || ''} ${input.getAttribute('aria-label') || ''}`.toLowerCase();
      let shouldCheck = false;
      let matchedVal = "";

      if (formattedFields.gender && matchRule(fullSearch, ["gender", "sex", "लिंग"]) && valStr.includes(formattedFields.gender.toLowerCase())) {
        shouldCheck = true; matchedVal = formattedFields.gender;
      } else if (formattedFields.category && matchRule(fullSearch, ["category", "caste", "वर्ग", "श्रेणी"]) && valStr.includes(formattedFields.category.toLowerCase())) {
        shouldCheck = true; matchedVal = formattedFields.category;
      } else if (valStr.includes("agree") || valStr.includes("declaration") || valStr.includes("accept") || valStr.includes("terms")) {
        shouldCheck = true; matchedVal = "Agreed";
      }

      if (shouldCheck) {
        clickCheckboxOrRadio(input);
        highlightFilledInput(input, matchedVal);
        count++;
        return;
      }
    }

    if (valToSet !== null && valToSet !== undefined) {
      setGoogleFormsInputValue(input, valToSet);
      highlightFilledInput(input, valToSet);
      count++;
    }
  });

  return count;
}

function matchRule(text, keywords) {
  return keywords.some((kw) => text.includes(kw));
}

function getFieldLabelText(element) {
  let labelText = "";

  if (element.id) {
    const label = document.querySelector(`label[for="${element.id}"]`);
    if (label) labelText = label.innerText;
  }

  if (!labelText) {
    const stContainer = element.closest('div[data-testid="stForm"], div[data-testid="stVerticalBlock"], div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput, .stSelectbox, .stNumberInput');
    if (stContainer) {
      const stLabel = stContainer.querySelector('label, [data-testid="stWidgetLabel"], p, span');
      if (stLabel) labelText = stLabel.innerText;
    }
  }

  if (!labelText) {
    const parentLabel = element.closest("label");
    if (parentLabel) labelText = parentLabel.innerText;
  }

  if (!labelText && element.previousElementSibling) {
    labelText = element.previousElementSibling.innerText || "";
  }

  return labelText;
}

function setGoogleFormsInputValue(element, value) {
  if (element.tagName && element.tagName.toLowerCase() === "select") {
    let matched = false;
    for (let option of element.options) {
      if (option.text.toLowerCase().includes(value.toLowerCase()) || option.value.toLowerCase().includes(value.toLowerCase())) {
        element.value = option.value;
        matched = true;
        break;
      }
    }
    if (!matched && element.options.length > 0) {
      element.selectedIndex = 1;
    }
  } else {
    element.focus();

    const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set ||
                         Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value")?.set;

    if (nativeSetter) {
      nativeSetter.call(element, value);
    } else {
      element.value = value;
    }
  }

  element.dispatchEvent(new Event("input", { bubbles: true, composed: true }));
  element.dispatchEvent(new Event("change", { bubbles: true, composed: true }));
  element.dispatchEvent(new KeyboardEvent("keydown", { key: "a", bubbles: true, composed: true }));
  element.dispatchEvent(new KeyboardEvent("keyup", { key: "a", bubbles: true, composed: true }));
  element.dispatchEvent(new Event("blur", { bubbles: true, composed: true }));
}

function highlightFilledInput(element, value) {
  const origBorder = element.style.border;
  const origShadow = element.style.boxShadow;

  element.style.border = "2px dashed #10B981";
  element.style.boxShadow = "0 0 14px rgba(16, 185, 129, 0.7)";

  const tooltip = document.createElement("div");
  tooltip.innerText = "✨ Auto-filled by Formitra Voice";
  tooltip.style.cssText = `
    position: absolute;
    background: #059669;
    color: #FFFFFF;
    font-size: 11px;
    font-weight: bold;
    padding: 3px 8px;
    border-radius: 4px;
    z-index: 999999;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    pointer-events: none;
  `;

  const rect = element.getBoundingClientRect();
  tooltip.style.top = `${window.scrollY + rect.top - 24}px`;
  tooltip.style.left = `${window.scrollX + rect.left}px`;

  document.body.appendChild(tooltip);

  setTimeout(() => {
    element.style.border = origBorder;
    element.style.boxShadow = origShadow;
    if (tooltip.parentNode) tooltip.parentNode.removeChild(tooltip);
  }, 4000);
}

function detectNextPageButton() {
  const btns = Array.from(document.querySelectorAll('[role="button"], button, span.NfeDxb'));
  return btns.some(el => {
    const txt = (el.innerText || el.textContent || "").trim().toLowerCase();
    return (txt === "next" || txt === "अगला" || txt === "आगे" || txt === "next section");
  });
}

function clickNextPageButton() {
  const btns = Array.from(document.querySelectorAll('[role="button"], button, span.NfeDxb'));
  const target = btns.find(el => {
    const txt = (el.innerText || el.textContent || "").trim().toLowerCase();
    return (txt === "next" || txt === "अगला" || txt === "आगे" || txt === "next section");
  });
  if (target) {
    target.click();
    return true;
  }
  return false;
}
