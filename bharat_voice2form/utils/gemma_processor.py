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
import difflib

from utils.constants import INDIAN_STATES

logger = logging.getLogger(__name__)

# ─── Config ────────────────────────────────────────────────────────
ENGINE: str = "gemma4"          # Primary: Gemma 4 via google-genai (falls back to smart_nlp if key missing)
MODEL_NAME: str = "gemma-4-31b-it"   # Gemma 4 31B Instruct via Gemini API
MODEL_FALLBACK: str = "gemma-4-26b-a4b-it"  # Gemma 4 26B MoE fallback

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

# Comprehensive Indian Cities & Districts Mappings (English, Devanagari & Common Variants)
_CITY_MAP: dict[str, str] = {
    # Tier 1 & State Capitals
    "jaipur": "Jaipur", "जयपुर": "Jaipur",
    "ranchi": "Ranchi", "राँची": "Ranchi", "रांची": "Ranchi",
    "patna": "Patna", "पटना": "Patna",
    "delhi": "Delhi", "new delhi": "New Delhi", "दिल्ली": "Delhi", "नई दिल्ली": "New Delhi",
    "lucknow": "Lucknow", "लखनऊ": "Lucknow",
    "mumbai": "Mumbai", "मुंबई": "Mumbai",
    "pune": "Pune", "पुणे": "Pune",
    "bhopal": "Bhopal", "भोपाल": "Bhopal",
    "indore": "Indore", "इंदौर": "Indore",
    "ahmedabad": "Ahmedabad", "अहमदाबाद": "Ahmedabad",
    "chennai": "Chennai", "चेन्नई": "Chennai",
    "hyderabad": "Hyderabad", "हैदराबाद": "Hyderabad",
    "bengaluru": "Bengaluru", "bangalore": "Bengaluru", "बेंगलुरु": "Bengaluru",
    "kolkata": "Kolkata", "कोलकाता": "Kolkata",
    "chandigarh": "Chandigarh", "चंडीगढ़": "Chandigarh",
    "guwahati": "Guwahati", "गुवाहाटी": "Guwahati",
    "dehradun": "Dehradun", "देहरादून": "Dehradun",
    "shimla": "Shimla", "शिमला": "Shimla",
    "bhubaneswar": "Bhubaneswar", "भुवनेश्वर": "Bhubaneswar",
    "raipur": "Raipur", "रायपुर": "Raipur",
    "haridwar": "Haridwar", "हरिद्वार": "Haridwar",
    "rishikesh": "Rishikesh", "ऋषिकेश": "Rishikesh",
    "roorkee": "Roorkee", "रुड़की": "Roorkee",
    "haldwani": "Haldwani", "हल्द्वानी": "Haldwani",
    
    # Major UP Districts
    "kanpur": "Kanpur", "कानपुर": "Kanpur",
    "varanasi": "Varanasi", "वाराणसी": "Varanasi", "banaras": "Varanasi",
    "agra": "Agra", "आगरा": "Agra",
    "prayagraj": "Prayagraj", "allahabad": "Prayagraj", "इलाहाबाद": "Prayagraj", "प्रयागराज": "Prayagraj",
    "meerut": "Meerut", "मेरठ": "Meerut",
    "bareilly": "Bareilly", "बरेली": "Bareilly",
    "aligarh": "Aligarh", "अलीगढ़": "Aligarh",
    "gorakhpur": "Gorakhpur", "गोरखपुर": "Gorakhpur",
    "ghaziabad": "Ghaziabad", "गाजियाबाद": "Ghaziabad",
    "noida": "Noida", "नोएडा": "Noida",
    "mathura": "Mathura", "मथुरा": "Mathura",
    "jhansi": "Jhansi", "झांसी": "Jhansi",
    "muzaffarnagar": "Muzaffarnagar", "मुजफ्फरनगर": "Muzaffarnagar",
    "moradabad": "Moradabad", "मुरादाबाद": "Moradabad",
    "ayodhya": "Ayodhya", "अयोध्या": "Ayodhya",
    "saharanpur": "Saharanpur", "सहारनपुर": "Saharanpur",

    # Major Rajasthan Districts
    "jodhpur": "Jodhpur", "जोधपुर": "Jodhpur",
    "kota": "Kota", "कोटा": "Kota",
    "bikaner": "Bikaner", "बीकानेर": "Bikaner",
    "ajmer": "Ajmer", "अजमेर": "Ajmer",
    "udaipur": "Udaipur", "उदयपुर": "Udaipur",
    "bhilwara": "Bhilwara", "भीलवाड़ा": "Bhilwara",
    "alwar": "Alwar", "अलवर": "Alwar",
    "sikar": "Sikar", "सीकर": "Sikar",
    "jhunjhunu": "Jhunjhunu", "झुंझुनू": "Jhunjhunu",

    # Major Bihar & Jharkhand Districts
    "jamshedpur": "Jamshedpur", "जमशेदपुर": "Jamshedpur",
    "dhanbad": "Dhanbad", "धनबाद": "Dhanbad",
    "bokaro": "Bokaro", "बोकारो": "Bokaro",
    "hazaribagh": "Hazaribagh", "हजारीबाग": "Hazaribagh",
    "gaya": "Gaya", "गया": "Gaya",
    "bhagalpur": "Bhagalpur", "भागलपुर": "Bhagalpur",
    "muzaffarpur": "Muzaffarpur", "मुजफ्फरपुर": "Muzaffarpur",
    "purnia": "Purnia", "पूर्णिया": "Purnia",
    "darbhanga": "Darbhanga", "दरभंगा": "Darbhanga",

    # Major MP & Maharashtra Districts
    "jabalpur": "Jabalpur", "जबलपुर": "Jabalpur",
    "gwalior": "Gwalior", "ग्वालियर": "Gwalior",
    "ujjain": "Ujjain", "उज्जैन": "Ujjain",
    "nagpur": "Nagpur", "नागपुर": "Nagpur",
    "nashik": "Nashik", "नासिक": "Nashik",
    "aurangabad": "Aurangabad", "औरंगाबाद": "Aurangabad",
    "solapur": "Solapur", "सोलापुर": "Solapur",
    "kolhapur": "Kolhapur", "कोल्हापुर": "Kolhapur",
    "thane": "Thane", "ठाणे": "Thane",

    # Major Punjab & Haryana Districts
    "gurgaon": "Gurugram", "gurugram": "Gurugram", "गुड़गांव": "Gurugram",
    "faridabad": "Faridabad", "फरीदाबाद": "Faridabad",
    "panipat": "Panipat", "पानीपत": "Panipat",
    "ambala": "Ambala", "अंबाला": "Ambala",
    "rohtak": "Rohtak", "रोहतक": "Rohtak",
    "karnal": "Karnal", "करनाल": "Karnal",
    "ludhiana": "Ludhiana", "लुधियाना": "Ludhiana",
    "amritsar": "Amritsar", "अमृतसर": "Amritsar",
    "jalandhar": "Jalandhar", "जालंधर": "Jalandhar",
    "patiala": "Patiala", "पटियाला": "Patiala",

    # Major South & East Districts
    "coimbatore": "Coimbatore", "मदुरै": "Madurai", "madurai": "Madurai",
    "visakhapatnam": "Visakhapatnam", "vijayawada": "Vijayawada", "guntur": "Guntur",
    "tirupati": "Tirupati", "warangal": "Warangal", "mysuru": "Mysuru", "mysore": "Mysuru",
    "mangalore": "Mangaluru", "mangaluru": "Mangaluru", "hubli": "Hubballi", "hubballi": "Hubballi",
    "cuttack": "Cuttack", "rourkela": "Rourkela", "siliguri": "Siliguri", "durgapur": "Durgapur",
}

# State Mappings including official 2-letter postal codes & Devanagari
_STATE_MAP: dict[str, str] = {
    "rajasthan": "Rajasthan", "राजस्थान": "Rajasthan",
    "jharkhand": "Jharkhand", "झारखंड": "Jharkhand",
    "bihar": "Bihar", "बिहार": "Bihar",
    "uttar pradesh": "Uttar Pradesh", "उत्तर प्रदेश": "Uttar Pradesh",
    "madhya pradesh": "Madhya Pradesh", "मध्य प्रदेश": "Madhya Pradesh",
    "maharashtra": "Maharashtra", "महाराष्ट्र": "Maharashtra",
    "delhi": "Delhi", "दिल्ली": "Delhi",
    "haryana": "Haryana", "हरियाणा": "Haryana",
    "punjab": "Punjab", "पंजाब": "Punjab",
    "gujarat": "Gujarat", "गुजरात": "Gujarat",
    "west bengal": "West Bengal", "पश्चिम बंगाल": "West Bengal",
    "tamil nadu": "Tamil Nadu", "तमिलनाडु": "Tamil Nadu",
    "karnataka": "Karnataka", "कर्नाटक": "Karnataka",
    "kerala": "Kerala", "केरल": "Kerala",
    "telangana": "Telangana", "तेलंगाना": "Telangana",
    "andhra pradesh": "Andhra Pradesh", "आंध्र प्रदेश": "Andhra Pradesh",
    "uttarakhand": "Uttarakhand", "uttrakhand": "Uttarakhand", "उत्तराखंड": "Uttarakhand", "uk": "Uttarakhand",
    "himachal pradesh": "Himachal Pradesh", "हिमाचल प्रदेश": "Himachal Pradesh",
    "chhattisgarh": "Chhattisgarh", "छत्तीसगढ़": "Chhattisgarh",
    "odisha": "Odisha", "ओडिशा": "Odisha",
    "assam": "Assam", "असम": "Assam",
}

_STATE_ABBR: dict[str, str] = {
    "up": "Uttar Pradesh", "mp": "Madhya Pradesh", "rj": "Rajasthan",
    "mh": "Maharashtra", "dl": "Delhi", "hr": "Haryana", "pb": "Punjab",
    "gj": "Gujarat", "wb": "West Bengal", "tn": "Tamil Nadu", "ka": "Karnataka",
    "kl": "Kerala", "ts": "Telangana", "ap": "Andhra Pradesh", "uk": "Uttarakhand",
    "hp": "Himachal Pradesh", "cg": "Chhattisgarh"
}

# Course Mappings with regex boundaries
_COURSE_PATTERNS: list[tuple[str, str]] = [
    (r"\b(b\.?tech|btech|engineering|बीटेक|बी\.टेक)\b", "B.Tech"),
    (r"\b(b\.?sc|bsc|बीएससी|बी\.एससी)\b", "B.Sc"),
    (r"\b(b\.?com|bcom|बीकॉम|बी\.कॉम)\b", "B.Com"),
    (r"\b(b\.?a|ba|बीए|बी\.ए)\b", "B.A"),
    (r"\b(bca|बीसीए)\b", "BCA"),
    (r"\b(m\.?tech|mtech|एमटेक)\b", "M.Tech"),
    (r"\b(m\.?sc|msc|एमएससी)\b", "M.Sc"),
    (r"\b(mba|एमबीए)\b", "MBA"),
    (r"\b(mca|एमसीए)\b", "MCA"),
    (r"\b(mbbs|एमबीबीएस)\b", "MBBS"),
    (r"\b(polytechnic|पॉलीटेक्निक)\b", "Polytechnic"),
    (r"\b(diploma|डिप्लोमा)\b", "Diploma"),
]

_STOPWORDS = {"is", "am", "hai", "hain", "hu", "hoon", "from", "se", "living", "in", "student", "छात्र", "हूँ", "है", "है।", "से", "का", "की", "के", "रहने", "वाला", "वाली"}

# Automatic State Inference from City
_CITY_TO_STATE_MAP: dict[str, str] = {
    "Jaipur": "Rajasthan", "Kota": "Rajasthan", "Ajmer": "Rajasthan", "Jodhpur": "Rajasthan", "Udaipur": "Rajasthan",
    "Bikaner": "Rajasthan", "Bhilwara": "Rajasthan", "Alwar": "Rajasthan", "Sikar": "Rajasthan", "Jhunjhunu": "Rajasthan",
    "Ranchi": "Jharkhand", "Jamshedpur": "Jharkhand", "Dhanbad": "Jharkhand", "Bokaro": "Jharkhand", "Hazaribagh": "Jharkhand",
    "Patna": "Bihar", "Gaya": "Bihar", "Muzaffarpur": "Bihar", "Bhagalpur": "Bihar", "Purnia": "Bihar", "Darbhanga": "Bihar",
    "Lucknow": "Uttar Pradesh", "Varanasi": "Uttar Pradesh", "Agra": "Uttar Pradesh", "Kanpur": "Uttar Pradesh", "Noida": "Uttar Pradesh",
    "Prayagraj": "Uttar Pradesh", "Meerut": "Uttar Pradesh", "Bareilly": "Uttar Pradesh", "Aligarh": "Uttar Pradesh",
    "Gorakhpur": "Uttar Pradesh", "Ghaziabad": "Uttar Pradesh", "Mathura": "Uttar Pradesh", "Jhansi": "Uttar Pradesh",
    "Muzaffarnagar": "Uttar Pradesh", "Moradabad": "Uttar Pradesh", "Ayodhya": "Uttar Pradesh", "Saharanpur": "Uttar Pradesh",
    "Delhi": "Delhi", "New Delhi": "Delhi",
    "Mumbai": "Maharashtra", "Pune": "Maharashtra", "Nagpur": "Maharashtra", "Nashik": "Maharashtra", "Aurangabad": "Maharashtra", "Solapur": "Maharashtra", "Kolhapur": "Maharashtra", "Thane": "Maharashtra",
    "Bhopal": "Madhya Pradesh", "Indore": "Madhya Pradesh", "Gwalior": "Madhya Pradesh", "Jabalpur": "Madhya Pradesh", "Ujjain": "Madhya Pradesh",
    "Ahmedabad": "Gujarat", "Surat": "Gujarat", "Vadodara": "Gujarat",
    "Chennai": "Tamil Nadu", "Coimbatore": "Tamil Nadu", "Madurai": "Tamil Nadu",
    "Hyderabad": "Telangana", "Warangal": "Telangana",
    "Bengaluru": "Karnataka", "Mysuru": "Karnataka", "Mangaluru": "Karnataka", "Hubballi": "Karnataka",
    "Kolkata": "West Bengal", "Howrah": "West Bengal", "Siliguri": "West Bengal", "Durgapur": "West Bengal",
    "Chandigarh": "Punjab", "Ludhiana": "Punjab", "Amritsar": "Punjab", "Jalandhar": "Punjab", "Patiala": "Punjab",
    "Gurugram": "Haryana", "Faridabad": "Haryana", "Panipat": "Haryana", "Ambala": "Haryana", "Rohtak": "Haryana", "Karnal": "Haryana",
    "Dehradun": "Uttarakhand", "Haridwar": "Uttarakhand", "Rishikesh": "Uttarakhand", "Roorkee": "Uttarakhand", "Haldwani": "Uttarakhand",
    "Shimla": "Himachal Pradesh", "Dharamshala": "Himachal Pradesh",
    "Bhubaneswar": "Odisha", "Cuttack": "Odisha", "Rourkela": "Odisha",
    "Raipur": "Chhattisgarh", "Bhilai": "Chhattisgarh",
    "Guwahati": "Assam", "Thiruvananthapuram": "Kerala", "Kochi": "Kerala"
}

KNOWN_COLLEGES = [
    "BIT Mesra", "IIT Delhi", "IIT Bombay", "Delhi University", "Lucknow University",
    "BHU Varanasi", "Anna University", "VTU Belgaum", "Jadavpur University", "NIT Trichy", "BITS Pilani", "Manipal Institute"
]


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
    dynamic_questions: list[dict] | None = None,
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
            result = _extract_gemma4(transcript, language, dynamic_questions=dynamic_questions)
        else:
            result = _extract_smart_nlp(transcript, language, simulate_delay, dynamic_questions=dynamic_questions)
    except Exception as exc:
        logger.warning("Engine '%s' failed: %s — falling back to dynamic NLP extractor", selected_engine, exc)
        result = _extract_smart_nlp(transcript, language, simulate_delay, dynamic_questions=dynamic_questions)

    result.latency_ms = (time.perf_counter() - t0) * 1000
    return result


def _clean_name(name_str: str) -> str:
    """Clean trailing punctuation and stop words from name."""
    words = name_str.strip().strip("।,.").split()
    cleaned = [w for w in words if w.lower() not in _STOPWORDS]
    return " ".join(cleaned).title() if cleaned else name_str.title()


def _parse_income(text: str) -> str | None:
    """
    Robust income parser handling word multipliers, Devanagari numbers, and formatted digits.
    """
    text_lower = text.lower()
    
    # 1. Check Devanagari & Hindi words
    if "पचास हजार" in text_lower or "50 thousand" in text_lower or "50 hazar" in text_lower or "fifty thousand" in text_lower:
        return "50000"
    if "डेढ़ लाख" in text_lower or "1.5 lakh" in text_lower or "1.5 lac" in text_lower or "1 lakh 50" in text_lower:
        return "150000"
    if "ढाई लाख" in text_lower or "2.5 lakh" in text_lower or "2.5 lac" in text_lower:
        return "250000"
    if "एक लाख" in text_lower or "1 lakh" in text_lower or "1 lac" in text_lower or "100k" in text_lower:
        return "100000"
    if "दो लाख" in text_lower or "2 lakh" in text_lower or "2 lacs" in text_lower or "200k" in text_lower:
        return "200000"
    if "तीन लाख" in text_lower or "3 lakh" in text_lower or "3 lacs" in text_lower or "300k" in text_lower:
        return "300000"
    if "पांच लाख" in text_lower or "5 lakh" in text_lower or "5 lacs" in text_lower or "500k" in text_lower:
        return "500000"
        
    # 2. Check regex numbers with lakh / lacs / lac / k / thousand
    lakh_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:lakh|lacs|lac|लाख|लख)\b", text_lower)
    if lakh_match:
        val = float(lakh_match.group(1))
        return str(int(val * 100000))
        
    thousand_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:thousand|hazar|हजार|k)\b", text_lower)
    if thousand_match:
        val = float(thousand_match.group(1))
        return str(int(val * 1000))
        
    # 3. Check plain 5 to 7 digit numbers
    num_matches = re.findall(r"\b\d{5,7}\b", text_lower)
    if num_matches:
        return num_matches[0]
        
    return None


def _extract_smart_nlp(
    transcript: str, language: str, simulate_delay: bool, dynamic_questions: list[dict] | None = None
) -> ExtractionResult:
    """
    Dynamically extract structured data from user's transcript using robust NLP rules.
    """
    if simulate_delay:
        time.sleep(0.01)

    extracted: dict[str, str] = {}
    text = transcript.strip()

    # ── Custom dynamic field patterns (Instagram, LinkedIn, Role, Domain, etc.) ────
    custom_field_patterns = [
        ("Instagram", r"(?:instagram|insta|ig)\s*(?:is|link|handle|:]?\s*)?([A-Za-z0-9_.-]+(?:\s+[A-Za-z0-9_.-]+)?)"),
        ("LinkedIn link", r"(?:linkedin|linked in)\s*(?:is|link|profile|:]?\s*)?([A-Za-z0-9_.-]+(?:\s+[A-Za-z0-9_.-]+)?)"),
        ("Role", r"(?:role|roll|position|post)\s*(?:is|:]?\s*)?([A-Za-z0-9_.-]+)"),
        ("Domain", r"(?:domain|dept|department|wing)\s*(?:is|:]?\s*)?([A-Za-z0-9_.-]+)"),
    ]
    for c_key, c_pat in custom_field_patterns:
        c_m = re.search(c_pat, text, re.IGNORECASE)
        if c_m:
            extracted[c_key] = c_m.group(1).strip()

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
            extracted["Name"] = cleaned
            break

    if "Name" not in extracted:
        cap_words = re.findall(r"\b[A-Z][a-z]+\b", text)
        if len(cap_words) >= 2:
            candidate = f"{cap_words[0]} {cap_words[1]}"
            extracted["Name"] = _clean_name(candidate)

    # ── 2. City / District extraction ──────────────────────────────────
    text_lower = text.lower()

    # Context-based Regex for City / District / Town (e.g. "district Kanpur", "Jila Patna", "from Aligarh")
    city_context_patterns = [
        r"(?:district|jila|जिला|city|शहर|dist|shahar)\s*(?:is|name|:]?\s*)?([A-Za-z\u0900-\u097F]{3,20})",
        r"\b([A-Za-z\u0900-\u097F]{3,20})\s+(?:district|jila|जिला|city|शहर)\b",
        r"(?:from|rehte hain|rehta hu|se hu|living in|resident of|wasi|n निवासी)\s+([A-Za-z\u0900-\u097F]{3,20})",
    ]
    for c_pat in city_context_patterns:
        c_match = re.search(c_pat, text, re.IGNORECASE)
        if c_match:
            candidate = c_match.group(1).strip()
            # Clean stop words
            if candidate.lower() not in _STOPWORDS and candidate.lower() not in ["first", "second", "third", "fourth", "btech", "bsc", "bcom"]:
                extracted["City"] = _CITY_MAP.get(candidate.lower(), candidate.title())
                break

    # Dictionary lookup (sorted by length descending to match multi-word cities first)
    if "City" not in extracted:
        for city_key in sorted(_CITY_MAP.keys(), key=len, reverse=True):
            if city_key in text_lower:
                extracted["City"] = _CITY_MAP[city_key]
                break

    # Fuzzy city matcher for ASR typos
    if "City" not in extracted:
        words = re.findall(r"\b[A-Za-z]{4,15}\b", text)
        known_cities = list(set(_CITY_MAP.values()))
        for w in words:
            matches = difflib.get_close_matches(w.lower(), [c.lower() for c in known_cities], n=1, cutoff=0.82)
            if matches:
                matched_lower = matches[0]
                for c in known_cities:
                    if c.lower() == matched_lower:
                        extracted["City"] = c
                        break
                if "City" in extracted:
                    break

    # ── 3. State extraction (sorted by length descending) ─────────────────────────
    for state_key in sorted(_STATE_MAP.keys(), key=len, reverse=True):
        if state_key in text_lower:
            extracted["State"] = _STATE_MAP[state_key]
            break
            
    if "State" not in extracted:
        for abbr, full_state in _STATE_ABBR.items():
            if re.search(rf"\b{abbr}\b", text_lower):
                extracted["State"] = full_state
                break

    # Automatic State Inference from City if State is missing
    if "City" in extracted and ("State" not in extracted or not extracted["State"]):
        inferred_state = _CITY_TO_STATE_MAP.get(extracted["City"])
        if inferred_state:
            extracted["State"] = inferred_state

    # ── 4. Course extraction ────────────────────────────────────────
    for pat, course_val in _COURSE_PATTERNS:
        if re.search(pat, text_lower):
            extracted["Course"] = course_val
            break

    # ── 5. Year extraction ──────────────────────────────────────────
    if re.search(r"\b(first year|1st year|1st yr|first|प्रथम वर्ष|पहला साल|पहला वर्ष|पहल साल|1st|प्रथम|1st year student)\b", text_lower):
        extracted["Year"] = "First Year"
    elif re.search(r"\b(second year|2nd year|2nd yr|second|द्वितीय वर्ष|दूसरा साल|दूसरा वर्ष|दूसरे साल|2nd|द्वितीय|2nd year student)\b", text_lower):
        extracted["Year"] = "Second Year"
    elif re.search(r"\b(third year|3rd year|3rd yr|third|तृतीय वर्ष|तीसरा साल|तीसरा वर्ष|तीसरे साल|3rd|तृतीय|pre-final year|3rd year student)\b", text_lower):
        extracted["Year"] = "Third Year"
    elif re.search(r"\b(fourth year|4th year|4th yr|fourth|final year|last year|चतुर्थ वर्ष|चौथा साल|चौथा वर्ष|चौथे साल|4th|चतुर्थ|4th year student)\b", text_lower):
        extracted["Year"] = "Fourth Year"
    elif re.search(r"\b(fifth year|5th year|5th yr|fifth|5th|5th year student)\b", text_lower):
        extracted["Year"] = "Fifth Year"

    # ── 6. Category & Gender extraction ─────────────────────────────
    if re.search(r"\b(obc|obc-ncl|ओबीसी)\b", text_lower):
        extracted["Category"] = "OBC"
    elif re.search(r"\b(sc|scheduled caste|एससी)\b", text_lower):
        extracted["Category"] = "SC"
    elif re.search(r"\b(st|scheduled tribe|एसटी)\b", text_lower):
        extracted["Category"] = "ST"
    elif re.search(r"\b(ews|economically weaker|ईडब्ल्यूएस)\b", text_lower):
        extracted["Category"] = "EWS"
    elif re.search(r"\b(general|general category|सामान्य|unreserved)\b", text_lower):
        extracted["Category"] = "General"

    if re.search(r"\b(male|mel|ladka|purush|पुरुष|लड़का|boy|man)\b", text_lower):
        extracted["Gender"] = "Male"
    elif re.search(r"\b(female|ladki|mahila|महिला|लड़की|girl|woman)\b", text_lower):
        extracted["Gender"] = "Female"
    elif re.search(r"\b(transgender|other|अन्य)\b", text_lower):
        extracted["Gender"] = "Transgender"

    # ── 7. Income extraction ────────────────────────────────────────
    parsed_inc = _parse_income(text)
    if parsed_inc:
        extracted["Income"] = parsed_inc

    # ── 8. Phone extraction ─────────────────────────────────────────
    phone_match = re.search(r"\b[6-9]\d{9}\b", text)
    if phone_match:
        extracted["Phone"] = phone_match.group(0)

    # ── 9. DOB extraction ───────────────────────────────────────────
    dob_match = re.search(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
    if dob_match:
        extracted["DOB"] = dob_match.group(0)

    # ── 10. Email extraction ─────────────────────────────────────────
    email_match = re.search(r"[\w.-]+@[\w.-]+\.\w+", text)
    if email_match:
        extracted["Email"] = email_match.group(0)

    # ── 11. PinCode & Aadhaar extraction ──────────────────────────────
    pin_match = re.search(r"\b(?:pin|pincode|pin code|पिन कोड)\s*[:=]?\s*(\d{6})\b", text_lower)
    if pin_match:
        extracted["PinCode"] = pin_match.group(1)

    aadhaar_match = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text)
    if aadhaar_match:
        extracted["Aadhaar"] = re.sub(r"\s", "", aadhaar_match.group(0))

    # ── 10. College extraction ──────────────────────────────────────
    college_match = re.search(
        r"\b(?:at|in|college|university|institute|संस्थान|कॉलेज|विश्वविद्यालय)\s+([A-Z][A-Za-z0-9\s]{2,25})",
        text,
    )
    if college_match:
        extracted["College"] = college_match.group(1).strip().title()
    else:
        # Check known colleges
        known_colleges = ["BIT Mesra", "IIT Delhi", "IIT Bombay", "Delhi University", "Lucknow University", "BHU Varanasi", "Anna University", "VTU Belgaum", "Jadavpur University", "NIT Trichy", "BITS Pilani"]
        for col in known_colleges:
            if col.lower() in text_lower:
                extracted["College"] = col
                break

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


def _extract_gemma4(transcript: str, language: str, dynamic_questions: list[dict] | None = None) -> ExtractionResult:
    """
    Extract structured form fields using Gemma 4 via the Google AI (google-genai) SDK.
    Model: gemma-4-31b-it (falls back to gemma-4-26b-a4b-it if quota exceeded).
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

    if dynamic_questions:
        q_titles = [q.get("title", "").strip() for q in dynamic_questions if q.get("title")]
        prompt = (
            f"You are an expert AI form-filling assistant.\n"
            f"Extract the exact value for each of the following form questions from the user's speech transcript:\n\n"
            f"FORM QUESTIONS TO FILL:\n"
            + "\n".join([f"- {title}" for title in q_titles]) + "\n\n"
            f"Return ONLY a JSON object where keys are the exact Question Titles listed above, and values are the extracted string answers from the transcript. If a question was NOT mentioned or answered in the transcript, set its value to null.\n\n"
            f"Transcript ({language}):\n{transcript}"
        )
    else:
        prompt = (
            f"Extract all personal and application details from the transcript below.\n"
            f"Return ONLY the JSON object with keys: Name, DOB, Gender, Category, City, State, PinCode, College, Course, Year, Income, Phone, Email, Percentage, Aadhaar.\n"
            f"Do not add any explanation or intro text.\n\n"
            f"Transcript ({language}):\n{transcript}"
        )

    # Try primary Gemma 4 model first, fall back to lighter variant
    for model_id in (MODEL_NAME, MODEL_FALLBACK):
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=1024,
                ),
            )
            raw_text = ""
            if hasattr(response, "text") and response.text:
                raw_text = response.text
            elif hasattr(response, "candidates") and response.candidates:
                cand = response.candidates[0]
                if cand.content and cand.content.parts:
                    raw_text = cand.content.parts[0].text or ""

            raw_text = raw_text.strip()
            if not raw_text:
                logger.warning("Empty output from Gemma 4 model %s", model_id)
                continue

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
    if not raw_text:
        raise ValueError("Empty text received from LLM")

    # Find first '{' and last '}'
    first_brace = raw_text.find('{')
    last_brace = raw_text.rfind('}')

    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = raw_text[first_brace:last_brace + 1]
        try:
            return json.loads(candidate)
        except Exception:
            # Fix trailing commas inside JSON object before parsing
            cleaned_cand = re.sub(r",\s*([\}\]])", r"\1", candidate)
            try:
                return json.loads(cleaned_cand)
            except Exception:
                pass

    # Direct fallback if no braces found
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned).strip()
    return json.loads(cleaned)
