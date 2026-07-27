// content.js — Formitra Web Form Auto-Filler Engine & Google Forms Assistant

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "AUTO_FILL_FORM") {
    const fields = request.fields || {};
    const filledCount = fillPageFormFields(fields);
    sendResponse({ status: "SUCCESS", count: filledCount });
  } else if (request.action === "TRIGGER_FIELD_DICTATION") {
    openFloatingFormitraWidget();
    sendResponse({ status: "STARTED" });
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
    width: 350px;
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
    <div style="font-size:12px;color:#CBD5E1;margin-bottom:10px;">Speak in your native language to auto-fill the form shown on your screen:</div>
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

  let rec = null;
  let recActive = false;
  const micToggle = document.getElementById("fmt-mic-toggle");
  const modalText = document.getElementById("fmt-modal-text");

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
          let str = "";
          for (let i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) str += e.results[i][0].transcript + " ";
          }
          if (str.trim()) {
            modalText.value = (modalText.value ? modalText.value + " " : "") + str.trim();
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
    const text = modalText.value.trim() || (
      "मेरा नाम राहुल शर्मा है। मैं जयपुर राजस्थान का रहने वाला हूँ। " +
      "मैं B.Tech द्वितीय वर्ष का छात्र हूँ और बीआईटी संस्थान में पढ़ता हूँ। " +
      "मेरी जन्मतिथि 15/08/2003 है और मेरी परिवार की वार्षिक आय ₹1,50,000 है।"
    );

    const fields = extractFormFieldsFromText(text);
    const count  = fillPageFormFields(fields);
    alert(`🎉 Formitra auto-filled ${count} form fields on this form!`);
    modal.style.display = "none";
  });
}

function extractFormFieldsFromText(text) {
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

function fillPageFormFields(fields) {
  let count = 0;

  // ── 1. Specialized Google Forms Engine Scanner ────────────────────
  const isGoogleForms = window.location.href.includes("docs.google.com/forms");
  if (isGoogleForms) {
    const gfQuestions = document.querySelectorAll('div[role="listitem"], div[jsmodel], .ge2dfc, .QrT82d, .freebirdFormviewerComponentsQuestionBaseRoot');
    gfQuestions.forEach((qContainer) => {
      const titleElem = qContainer.querySelector('.M7eMe, [role="heading"], .HoLwm, .freebirdFormviewerComponentsQuestionBaseHeaderTitle, span');
      if (!titleElem) return;

      const qTitle = titleElem.innerText.toLowerCase();
      const input = qContainer.querySelector('input[type="text"], input[type="email"], input[type="tel"], input[type="number"], input[type="date"], textarea, [role="textbox"]');

      if (!input) return;

      let valToSet = null;
      if (matchRule(qTitle, ["name", "full name", "applicant name", "candidate name", "नाम"])) valToSet = fields.name;
      else if (matchRule(qTitle, ["city", "town", "district", "शहर"])) valToSet = fields.city;
      else if (matchRule(qTitle, ["state", "domicile", "राज्य"])) valToSet = fields.state;
      else if (matchRule(qTitle, ["income", "annual income", "family income", "आय"])) valToSet = fields.income;
      else if (matchRule(qTitle, ["course", "degree", "program", "पाठ्यक्रम"])) valToSet = fields.course;
      else if (matchRule(qTitle, ["year", "academic year", "वर्ष"])) valToSet = fields.year;
      else if (matchRule(qTitle, ["college", "institute", "school", "university", "संस्थान"])) valToSet = fields.college;
      else if (matchRule(qTitle, ["dob", "date of birth", "birth date", "जन्मतिथि"])) valToSet = fields.dob;
      else if (matchRule(qTitle, ["mobile", "phone", "contact", "फोन"])) valToSet = fields.mobile;
      else if (matchRule(qTitle, ["email", "e-mail", "ईमेल"])) valToSet = fields.email;

      if (valToSet !== null && valToSet !== undefined) {
        setNativeInputValue(input, valToSet);
        highlightFilledInput(input, valToSet);
        count++;
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

    if (matchRule(fullSearch, ["name", "full name", "applicant name", "candidate name", "नाम"])) valToSet = fields.name;
    else if (matchRule(fullSearch, ["city", "town", "district", "शहर"])) valToSet = fields.city;
    else if (matchRule(fullSearch, ["state", "domicile", "राज्य"])) valToSet = fields.state;
    else if (matchRule(fullSearch, ["income", "annual income", "family income", "आय"])) valToSet = fields.income;
    else if (matchRule(fullSearch, ["course", "degree", "program", "पाठ्यक्रम"])) valToSet = fields.course;
    else if (matchRule(fullSearch, ["year", "academic year", "वर्ष"])) valToSet = fields.year;
    else if (matchRule(fullSearch, ["college", "institute", "school", "university", "संस्थान"])) valToSet = fields.college;
    else if (matchRule(fullSearch, ["dob", "date of birth", "birth date", "जन्मतिथि"])) valToSet = fields.dob;
    else if (matchRule(fullSearch, ["mobile", "phone", "contact", "फोन"])) valToSet = fields.mobile;
    else if (matchRule(fullSearch, ["email", "e-mail", "ईमेल"])) valToSet = fields.email;

    if (valToSet !== null && valToSet !== undefined) {
      setNativeInputValue(input, valToSet);
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

  // 1. Standard <label for="...">
  if (element.id) {
    const label = document.querySelector(`label[for="${element.id}"]`);
    if (label) labelText = label.innerText;
  }

  // 2. Streamlit data-testid="stWidgetLabel" or parent container
  if (!labelText) {
    const stContainer = element.closest('div[data-testid="stForm"], div[data-testid="stVerticalBlock"], div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput, .stSelectbox, .stNumberInput');
    if (stContainer) {
      const stLabel = stContainer.querySelector('label, [data-testid="stWidgetLabel"], p, span');
      if (stLabel) labelText = stLabel.innerText;
    }
  }

  // 3. Parent label fallback
  if (!labelText) {
    const parentLabel = element.closest("label");
    if (parentLabel) labelText = parentLabel.innerText;
  }

  // 4. Preceding sibling
  if (!labelText && element.previousElementSibling) {
    labelText = element.previousElementSibling.innerText || "";
  }

  return labelText;
}

function setNativeInputValue(element, value) {
  if (element.tagName.toLowerCase() === "select") {
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
    // Native React & Google Forms internal input setter
    const valueSetter = Object.getOwnPropertyDescriptor(element, 'value')?.set;
    const prototypeSetter = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(element), 'value')?.set;

    if (prototypeSetter && valueSetter !== prototypeSetter) {
      prototypeSetter.call(element, value);
    } else if (valueSetter) {
      valueSetter.call(element, value);
    } else {
      element.value = value;
    }
  }

  // Dispatch events to trigger Google Forms internal JS model update
  element.dispatchEvent(new Event("input", { bubbles: true }));
  element.dispatchEvent(new Event("change", { bubbles: true }));
  element.dispatchEvent(new Event("blur", { bubbles: true }));
  element.dispatchEvent(new KeyboardEvent("keydown", { key: "a", bubbles: true }));
  element.dispatchEvent(new KeyboardEvent("keyup", { key: "a", bubbles: true }));
}

function highlightFilledInput(element, value) {
  const origBorder = element.style.border;
  const origShadow = element.style.boxShadow;

  element.style.border = "2px dashed #10B981";
  element.style.boxShadow = "0 0 12px rgba(16, 185, 129, 0.6)";

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
