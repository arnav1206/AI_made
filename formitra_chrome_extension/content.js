// content.js — Formitra Injected Web Form Auto-Filler Engine

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "AUTO_FILL_FORM") {
    const fields = request.fields || {};
    const filledCount = fillPageFormFields(fields);
    sendResponse({ status: "SUCCESS", count: filledCount });
  }
  return true;
});

function fillPageFormFields(fields) {
  let count = 0;
  const inputs = document.querySelectorAll("input, select, textarea");

  inputs.forEach((input) => {
    if (input.type === "hidden" || input.type === "submit" || input.type === "button") return;

    const labelText  = getFieldLabelText(input).toLowerCase();
    const attrText   = `${input.name || ''} ${input.id || ''} ${input.placeholder || ''} ${input.getAttribute('aria-label') || ''}`.toLowerCase();
    const fullSearch = `${labelText} ${attrText}`;

    let valToSet = null;

    // Smart Intent Field Matching Rules
    if (matchRule(fullSearch, ["name", "full name", "applicant name", "candidate name", "नाम"])) {
      valToSet = fields.name;
    } else if (matchRule(fullSearch, ["city", "town", "district", "शहर"])) {
      valToSet = fields.city;
    } else if (matchRule(fullSearch, ["state", "domicile", "राज्य"])) {
      valToSet = fields.state;
    } else if (matchRule(fullSearch, ["income", "annual income", "family income", "आय"])) {
      valToSet = fields.income;
    } else if (matchRule(fullSearch, ["course", "degree", "program", "पाठ्यक्रम"])) {
      valToSet = fields.course;
    } else if (matchRule(fullSearch, ["year", "academic year", "वर्ष"])) {
      valToSet = fields.year;
    } else if (matchRule(fullSearch, ["college", "institute", "school", "university", "संस्थान"])) {
      valToSet = fields.college;
    } else if (matchRule(fullSearch, ["dob", "date of birth", "birth date", "जन्मतिथि"])) {
      valToSet = fields.dob;
    } else if (matchRule(fullSearch, ["mobile", "phone", "contact", "फोन"])) {
      valToSet = fields.mobile;
    } else if (matchRule(fullSearch, ["email", "e-mail", "ईमेल"])) {
      valToSet = fields.email;
    } else if (matchRule(fullSearch, ["aadhaar", "adhar", "uid", "आधार"])) {
      valToSet = fields.aadhaar;
    }

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
  if (element.id) {
    const label = document.querySelector(`label[for="${element.id}"]`);
    if (label) labelText = label.innerText;
  }
  if (!labelText) {
    const parentLabel = element.closest("label");
    if (parentLabel) labelText = parentLabel.innerText;
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
    // Native React & HTML input value setter
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

  element.dispatchEvent(new Event("input", { bubbles: true }));
  element.dispatchEvent(new Event("change", { bubbles: true }));
  element.dispatchEvent(new Event("blur", { bubbles: true }));
}

function highlightFilledInput(element, value) {
  const origBorder = element.style.border;
  const origShadow = element.style.boxShadow;

  element.style.border = "2px solid #10B981";
  element.style.boxShadow = "0 0 12px rgba(16, 185, 129, 0.6)";

  // Floating Checkmark Tooltip
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
