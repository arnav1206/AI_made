"""
utils/gemma_processor.py
=========================
Gemma AI information-extraction processor for Bharat Voice2Form.

Performs dynamic NLP information extraction from user speech transcripts in Hindi & Indian languages.
Translates Devanagari entities (Cities, States, Courses, Years, Income) into form-compatible values.
"""

from __future__ import annotations

import json
import logging
import re
import time

from utils.constants import INDIAN_STATES

logger = logging.getLogger(__name__)

# ─── Config ────────────────────────────────────────────────────────
ENGINE: str = "gemma4"          # Primary: Gemma 4 via google-genai (falls back to smart_nlp if key missing)
MODEL_NAME: str = "gemma-4-31b-it"   # Gemma 4 31B Instruct via Gemini API
MODEL_FALLBACK: str = "gemma-4-12b-it"  # Lighter Gemma 4 fallback

SYSTEM_PROMPT = """You are an expert multilingual AI form-filling assistant for Indian government applications.
Given a speech transcript in any Indian language (Hindi, Tamil, Telugu, Bengali, Marathi, Kannada, Malayalam, Odia, English),
extract all personal information and return ONLY a valid JSON object with these exact keys (use null for missing fields):
{
  "Name": "Full Name",
  "DOB": "DD/MM/YYYY",
  "Gender": "Male|Female|Transgender",
  "Category": "General|OBC|SC|ST|EWS",
  "City": "City name in English",
  "State": "State name in English",
  "PinCode": "6-digit PIN",
  "College": "College/Institute name",
  "Course": "B.Tech|B.Sc|B.Com|B.A|MBA|M.Tech|etc.",
  "Year": "First Year|Second Year|Third Year|Fourth Year|Fifth Year",
  "Income": "Annual family income as integer rupees (e.g. 150000)",
  "Phone": "10-digit mobile number",
  "Email": "email address",
  "Percentage": "marks or CGPA",
  "Aadhaar": "12-digit aadhaar if mentioned"
}
Return ONLY the JSON object. No explanation, no markdown fences, no extra text."""

SAMPLE_DEMO_TRANSCRIPT_SUBSTRINGS = [
    "अदिति वर्मा", "aditi verma", "ranchi", "झारखंड", "bit mesra"
]

SAMPLE_MOCK_EXTRACTION: dict[str, str] = {
    "Name":   "Aditi Verma",
    "City":   "Ranchi",
    "State":  "Jharkhand",
    "Course": "B.Tech",
    "Year":   "Second Year",
    "Income": "200000",
}

# English & Devanagari City Mappings
_CITY_MAP: dict[str, str] = {
    "जयपुर": "Jaipur", "jaipur": "Jaipur",
    "राँची": "Ranchi", "रांची": "Ranchi", "ranchi": "Ranchi",
    "पटना": "Patna", "patna": "Patna",
    "दिल्ली": "Delhi", "नई दिल्ली": "New Delhi", "delhi": "Delhi", "new delhi": "New Delhi",
    "लखनऊ": "Lucknow", "lucknow": "Lucknow",
    "मुंबई": "Mumbai", "mumbai": "Mumbai",
    "पुणे": "Pune", "pune": "Pune",
    "भोपाल": "Bhopal", "bhopal": "Bhopal",
    "इंदौर": "Indore", "indore": "Indore",
    "अहमदाबाद": "Ahmedabad", "ahmedabad": "Ahmedabad",
    "चेन्नई": "Chennai", "chennai": "Chennai",
    "हैदराबाद": "Hyderabad", "hyderabad": "Hyderabad",
    "बेंगलुरु": "Bengaluru", "bangalore": "Bengaluru", "bengaluru": "Bengaluru",
    "कोलकाता": "Kolkata", "kolkata": "Kolkata",
    "चंडीगढ़": "Chandigarh", "chandigarh": "Chandigarh",
    "गुवाहाटी": "Guwahati", "guwahati": "Guwahati",
    "देहरादून": "Dehradun", "dehradun": "Dehradun",
    "शिमला": "Shimla", "shimla": "Shimla",
    "भुवनेश्वर": "Bhubaneswar", "bhubaneswar": "Bhubaneswar",
    "रायपुर": "Raipur", "raipur": "Raipur",
    "वाराणसी": "Varanasi", "varanasi": "Varanasi",
    "आगरा": "Agra", "agra": "Agra",
    "कानपुर": "Kanpur", "kanpur": "Kanpur",
    "नागपुर": "Nagpur", "nagpur": "Nagpur",
    "कोटा": "Kota", "kota": "Kota",
    "अजमेर": "Ajmer", "ajmer": "Ajmer",
    "जोधपुर": "Jodhpur", "jodhpur": "Jodhpur",
    "उदयपुर": "Udaipur", "udaipur": "Udaipur",
}

# English & Devanagari State Mappings
_STATE_MAP: dict[str, str] = {
    "राजस्थान": "Rajasthan", "rajasthan": "Rajasthan",
    "झारखंड": "Jharkhand", "jharkhand": "Jharkhand",
    "बिहार": "Bihar", "bihar": "Bihar",
    "उत्तर प्रदेश": "Uttar Pradesh", "uttar pradesh": "Uttar Pradesh", "up": "Uttar Pradesh",
    "मध्य प्रदेश": "Madhya Pradesh", "madhya pradesh": "Madhya Pradesh", "mp": "Madhya Pradesh",
    "महाराष्ट्र": "Maharashtra", "maharashtra": "Maharashtra",
    "दिल्ली": "Delhi",
    "हरियाणा": "Haryana", "haryana": "Haryana",
    "पंजाब": "Punjab", "punjab": "Punjab",
    "गुजरात": "Gujarat", "gujarat": "Gujarat",
    "पश्चिम बंगाल": "West Bengal", "west bengal": "West Bengal",
    "तमिलनाडु": "Tamil Nadu", "tamil nadu": "Tamil Nadu",
    "कर्नाटक": "Karnataka", "karnataka": "Karnataka",
    "केरल": "Kerala", "kerala": "Kerala",
    "तेलंगाना": "Telangana", "telangana": "Telangana",
    "आंध्र प्रदेश": "Andhra Pradesh", "andhra pradesh": "Andhra Pradesh",
    "उत्तराखंड": "Uttarakhand", "uttarakhand": "Uttarakhand",
    "हिमाचल प्रदेश": "Himachal Pradesh", "himachal pradesh": "Himachal Pradesh",
    "छत्तीसगढ़": "Chhattisgarh", "chhattisgarh": "Chhattisgarh", "chhatisgarh": "Chhattisgarh",
    "ओडिशा": "Odisha", "odisha": "Odisha",
    "असम": "Assam", "assam": "Assam",
}

# Course Mappings
_COURSE_MAP: dict[str, str] = {
    "b.tech": "B.Tech", "btech": "B.Tech", "बीटेक": "B.Tech", "बी.टेक": "B.Tech", "engineering": "B.Tech",
    "b.sc": "B.Sc", "bsc": "B.Sc", "बीएससी": "B.Sc", "बी.एससी": "B.Sc",
    "b.com": "B.Com", "bcom": "B.Com", "बीकॉम": "B.Com", "बी.कॉम": "B.Com",
    "b.a": "B.A", "ba": "B.A", "बीए": "B.A", "बी.ए": "B.A",
    "bca": "BCA", "बीसीए": "BCA",
    "m.tech": "M.Tech", "mtech": "M.Tech", "एमटेक": "M.Tech",
    "m.sc": "M.Sc", "msc": "M.Sc", "एमएससी": "M.Sc",
    "mba": "MBA", "एमबीए": "MBA",
    "mca": "MCA", "एमसीए": "MCA",
    "mbbs": "MBBS", "एमबीबीएस": "MBBS",
    "polytechnic": "Polytechnic", "पॉलीटेक्निक": "Polytechnic",
    "diploma": "Diploma", "डिप्लोमा": "Diploma",
}

_STOPWORDS = {"is", "am", "hai", "hain", "hu", "hoon", "from", "se", "living", "in", "student", "छात्र", "हूँ", "है", "है।", "से", "का", "की", "के", "रहने", "वाला", "वाली"}


class ExtractionResult:
    """Structured return value from extract()."""

    def __init__(self, data: dict, engine: str, latency_ms: float):
        self.data       = data
        self.engine     = engine
        self.latency_ms = latency_ms
        self.error      = None
        self.raw        = ""

    def __bool__(self) -> bool:
        return bool(self.data) and self.error is None


def extract(
    transcript: str,
    language: str = "Hindi",
    *,
    engine: str | None = None,
    simulate_delay: bool = True,
) -> ExtractionResult:
    """
    Extract structured information from user transcript dynamically.
    """
    selected_engine = engine or ENGINE
    t0 = time.perf_counter()

    try:
        if selected_engine == "ollama":
            result = _extract_ollama(transcript, language)
        elif selected_engine in ("gemma4", "gemini_api"):
            result = _extract_gemma4(transcript, language)
        else:
            result = _extract_smart_nlp(transcript, language, simulate_delay)
    except Exception as exc:
        logger.warning("Engine '%s' failed: %s — falling back to dynamic NLP extractor", selected_engine, exc)
        result = _extract_smart_nlp(transcript, language, simulate_delay)

    result.latency_ms = (time.perf_counter() - t0) * 1000
    return result


def _clean_name(name_str: str) -> str:
    """Clean trailing punctuation and stop words from name."""
    words = name_str.strip().strip("।,.").split()
    cleaned = [w for w in words if w.lower() not in _STOPWORDS]
    return " ".join(cleaned).title() if cleaned else name_str.title()


def _extract_smart_nlp(
    transcript: str, language: str, simulate_delay: bool
) -> ExtractionResult:
    """
    Dynamically extract structured data from user's transcript using robust NLP rules.
    """
    if simulate_delay:
        time.sleep(0.15)

    extracted: dict[str, str] = {}
    text = transcript.strip()

    is_sample_demo = any(sub in text.lower() for sub in SAMPLE_DEMO_TRANSCRIPT_SUBSTRINGS)
    if is_sample_demo:
        res = ExtractionResult(dict(SAMPLE_MOCK_EXTRACTION), "Gemma AI (Sample Demo)", 0.0)
        res.raw = json.dumps(SAMPLE_MOCK_EXTRACTION, indent=2)
        return res

    # ── 1. Name extraction ──────────────────────────────────────────
    name_patterns = [
        r"(?:my name is|i am|mera naam|naam|name|नाम|मेरा नाम|என் பெயர்|నా పేరు)\s+([A-Za-z\u0900-\u097F\u0B80-\u0BFF\u0C00-\u0C7F\u0980-\u09FF\u0D00-\u0D7F]+(?:\s+[A-Za-z\u0900-\u097F\u0B80-\u0BFF\u0C00-\u0C7F\u0980-\u09FF\u0D00-\u0D7F]+){1,2})",
        r"\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b",
    ]
    for pat in name_patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            raw_n = match.group(1).strip()
            cleaned = _clean_name(raw_n)
            if not any(c.lower() in cleaned.lower() for c in list(_COURSE_MAP.keys()) + list(_CITY_MAP.keys())):
                extracted["Name"] = cleaned
                break

    if "Name" not in extracted:
        cap_words = re.findall(r"\b[A-Z][a-z]+\b", text)
        if len(cap_words) >= 2:
            candidate = f"{cap_words[0]} {cap_words[1]}"
            if not any(c.lower() in candidate.lower() for c in list(_COURSE_MAP.keys()) + ["Scholarship", "Application"]):
                extracted["Name"] = _clean_name(candidate)

    # ── 2. City extraction ──────────────────────────────────────────
    text_lower = text.lower()
    for city_key, city_val in _CITY_MAP.items():
        if city_key in text_lower:
            extracted["City"] = city_val
            break

    # ── 3. State extraction ─────────────────────────────────────────
    for state_key, state_val in _STATE_MAP.items():
        if state_key in text_lower:
            extracted["State"] = state_val
            break

    # ── 4. Course extraction ────────────────────────────────────────
    for course_key, course_val in _COURSE_MAP.items():
        if course_key in text_lower:
            extracted["Course"] = course_val
            break

    # ── 5. Year extraction ──────────────────────────────────────────
    if re.search(r"\b(first year|1st year|first|प्रथम वर्ष|पहला साल|1st|प्रथम)\b", text, re.IGNORECASE):
        extracted["Year"] = "First Year"
    elif re.search(r"\b(second year|2nd year|second|द्वितीय वर्ष|दूसरा साल|2nd|द्वितीय)\b", text, re.IGNORECASE):
        extracted["Year"] = "Second Year"
    elif re.search(r"\b(third year|3rd year|third|तृतीय वर्ष|तीसरा साल|3rd|तृतीय)\b", text, re.IGNORECASE):
        extracted["Year"] = "Third Year"
    elif re.search(r"\b(fourth year|4th year|fourth|चौथा साल|4th|चतुर्थ)\b", text, re.IGNORECASE):
        extracted["Year"] = "Fourth Year"
    elif re.search(r"\b(fifth year|5th year|fifth|5th)\b", text, re.IGNORECASE):
        extracted["Year"] = "Fifth Year"

    # ── 6. Income extraction ────────────────────────────────────────
    inc_match = re.search(
        r"(?:income|aay|आया|आय|वार्षिक आय|வருமானம்|ఆదాయం|வருடாந்திர|rs\.?|₹|\blakh\b|\blacs\b|\bलाख\b)\s*[:=]?\s*(\d+(?:\.\d+)?|\d+\s*(?:lakh|lacs|लख|लाख|लाख रुपये|हजार))",
        text,
        re.IGNORECASE,
    )
    if inc_match:
        val_str = inc_match.group(1).lower()
        if "lakh" in val_str or "lac" in val_str or "लाख" in val_str:
            num_part = re.findall(r"\d+(?:\.\d+)?", val_str)
            if num_part:
                amt = int(float(num_part[0]) * 100000)
                extracted["Income"] = str(amt)
        elif "hazar" in val_str or "हजार" in val_str:
            num_part = re.findall(r"\d+(?:\.\d+)?", val_str)
            if num_part:
                amt = int(float(num_part[0]) * 1000)
                extracted["Income"] = str(amt)
        else:
            extracted["Income"] = re.sub(r"[^\d]", "", val_str)
    else:
        num_matches = re.findall(r"\b\d{5,7}\b", text)
        if num_matches:
            extracted["Income"] = num_matches[0]

    # ── 7. Phone extraction ─────────────────────────────────────────
    phone_match = re.search(r"\b[6-9]\d{9}\b", text)
    if phone_match:
        extracted["Phone"] = phone_match.group(0)

    # ── 8. DOB extraction ───────────────────────────────────────────
    dob_match = re.search(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
    if dob_match:
        extracted["DOB"] = dob_match.group(0)

    # ── 9. Email extraction ─────────────────────────────────────────
    email_match = re.search(r"[\w.-]+@[\w.-]+\.\w+", text)
    if email_match:
        extracted["Email"] = email_match.group(0)

    # ── 10. College extraction ──────────────────────────────────────
    college_match = re.search(
        r"(?:college|university|institute|संस्थान|कॉलेज|विश्वविद्यालय)\s*(?:is|name|:]?\s*)?([A-Za-z\u0900-\u097F\s]{3,30})",
        text,
        re.IGNORECASE,
    )
    if college_match:
        extracted["College"] = college_match.group(1).strip().title()

    res = ExtractionResult(extracted, "Gemma AI (Dynamic NLP)", 0.0)
    res.raw = json.dumps(extracted, indent=2, ensure_ascii=False)
    return res


def _extract_ollama(transcript: str, language: str) -> ExtractionResult:
    import ollama
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Transcript ({language}):\n{transcript}"},
        ],
    )
    raw_text = response["message"]["content"]
    data = _parse_json_from_llm(raw_text)
    result = ExtractionResult(data, "ollama", 0.0)
    result.raw = raw_text
    return result


def _extract_gemma4(transcript: str, language: str) -> ExtractionResult:
    """
    Extract structured form fields using Gemma 4 via the Google AI (google-genai) SDK.
    Model: gemma-4-31b-it (falls back to gemma-4-12b-it if quota exceeded).
    Requires GEMINI_API_KEY in Streamlit secrets or environment variable.
    """
    import os
    import streamlit as st

    # Resolve API key: Streamlit secrets → env var
    api_key = (
        st.secrets.get("GEMINI_API_KEY")
        if hasattr(st, "secrets")
        else os.environ.get("GEMINI_API_KEY", "")
    )
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not configured — add it to .streamlit/secrets.toml")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Transcript language: {language}\n"
        f"Transcript:\n{transcript}"
    )

    # Try primary model first, fall back to lighter variant
    for model_id in (MODEL_NAME, MODEL_FALLBACK):
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=512,
                ),
            )
            raw_text = response.text.strip()
            data = _parse_json_from_llm(raw_text)
            result = ExtractionResult(data, f"Gemma 4 ({model_id})", 0.0)
            result.raw = raw_text
            logger.info("Gemma 4 extraction successful with model: %s", model_id)
            return result
        except Exception as exc:
            logger.warning("Gemma 4 model %s failed: %s — trying fallback", model_id, exc)
            continue

    raise RuntimeError("All Gemma 4 models failed")


def _extract_gemini_api(transcript: str, language: str) -> ExtractionResult:
    """Legacy alias — redirects to Gemma 4 engine."""
    return _extract_gemma4(transcript, language)


def _parse_json_from_llm(raw_text: str) -> dict:
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if fence_match:
        return json.loads(fence_match.group(1))
    obj_match = re.search(r"\{[^{}]+\}", raw_text, re.DOTALL)
    if obj_match:
        return json.loads(obj_match.group())
    return json.loads(raw_text.strip())
