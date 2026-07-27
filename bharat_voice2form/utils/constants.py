"""
utils/constants.py
===================
Application constants for Formitra (भारत Formitra).
"""

from __future__ import annotations

APP_TITLE: str = "Formitra — AI-Powered Voice Form Filling for India"
APP_SUBTITLE: str = "Voice-assisted form filling with multilingual AI extraction and scholarship eligibility engine"
APP_VERSION: str = "2.0.0"
POWERED_BY: str = "Powered by Gemma AI & VoiceAssist"

PAGE_HOME: str = "login"
APPLICATION_NUMBER: str = "FMT-2026-89412"

PAGE_ORDER: list[str] = [
    "login",
    "register",
    "home",
    "form_selection",
    "voice_input",
    "ai_processing",
    "auto_fill",
    "preview",
    "success",
    "track_status",
    "help_faq",
]

PAGE_LABELS: dict[str, str] = {
    "login":          "🔑 Login",
    "register":       "📝 Register",
    "home":           "🏠 Home",
    "form_selection": "📋 Select Form",
    "voice_input":    "🎙️ Voice Input",
    "ai_processing":  "🤖 AI Processing",
    "auto_fill":      "✍️ Form Review",
    "preview":        "👁️ Preview",
    "success":        "🎉 Submitted",
    "track_status":   "🔍 Track Status",
    "help_faq":       "❓ Help & FAQ",
}

STEP_LABELS: list[str] = [
    "Select Form",
    "Voice Input",
    "AI Processing",
    "Form Review",
    "Preview",
    "Submitted",
]

ALL_FIELD_NAMES: list[str] = [
    "Full Name",
    "Date of Birth",
    "Gender",
    "Category",
    "Address",
    "City",
    "State",
    "PIN Code",
    "College",
    "Course",
    "Year",
    "Annual Family Income",
    "Phone Number",
    "Email",
    "Percentage / CGPA",
]

SCHOLARSHIP_SECTIONS: list[dict] = [
    {
        "title": "Personal Information",
        "icon": "👤",
        "fields": ["Full Name", "Date of Birth", "Gender", "Category"],
    },
    {
        "title": "Address & Domicile Details",
        "icon": "📍",
        "fields": ["Address", "City", "State", "PIN Code"],
    },
    {
        "title": "Academic Information",
        "icon": "🎓",
        "fields": ["College", "Course", "Year", "Percentage / CGPA"],
    },
    {
        "title": "Financial & Contact Details",
        "icon": "💼",
        "fields": ["Annual Family Income", "Phone Number", "Email"],
    },
]

FORM_TYPES: list[dict] = [
    {
        "icon": "🎓",
        "title": "Post-Matric Scholarship Scheme",
        "desc": "For SC/ST/OBC/EBC students in Class 11, 12, ITI, Degree, Diploma & Higher Education.",
        "badge": "Available Now",
        "available": True,
    },
    {
        "icon": "🏛️",
        "title": "Central Sector Scheme of Scholarships",
        "desc": "For meritorious College and University students with family income under ₹4.5 Lakh.",
        "badge": "Available Now",
        "available": True,
    },
    {
        "icon": "📚",
        "title": "Pre-Matric Scholarship for Minorities",
        "desc": "For Minority community students studying in Class 1 to 10 with family income under ₹1.0 Lakh.",
        "badge": "Available Now",
        "available": True,
    },
    {
        "icon": "🌟",
        "title": "State Higher Education Merit Scholarship",
        "desc": "State-level merit scheme for undergraduate and postgraduate students in technical courses.",
        "badge": "Available Now",
        "available": True,
    },
    {
        "icon": "📜",
        "title": "Income & Caste Certificate Portal",
        "desc": "Government portal for issuing verified EWS and Caste certificates.",
        "badge": "Coming Soon",
        "available": False,
    },
    {
        "icon": "🌾",
        "title": "PM-Kisan Farmer Welfare Scheme",
        "desc": "Direct benefit transfer for agricultural landholding farmer families.",
        "badge": "Coming Soon",
        "available": False,
    },
]

SCHOLARSHIP_FORMS: list[dict[str, str]] = [
    {
        "id": "post_matric",
        "title": "Post-Matric Scholarship Scheme",
        "description": "For SC/ST/OBC/EBC students in Class 11, 12, ITI, Degree, Diploma & Higher Education.",
        "icon": "🎓",
        "tag": "Government of India",
        "tag_color": "#FF7A00",
    },
    {
        "id": "central_sector",
        "title": "Central Sector Scheme of Scholarships",
        "description": "For meritorious College and University students with family income under ₹4.5 Lakh.",
        "icon": "🏛️",
        "tag": "Ministry of Education",
        "tag_color": "#0099FF",
    },
    {
        "id": "pre_matric",
        "title": "Pre-Matric Scholarship for Minorities",
        "description": "For Minority community students studying in Class 1 to 10 with family income under ₹1.0 Lakh.",
        "icon": "📚",
        "tag": "Ministry of Minority Affairs",
        "tag_color": "#00CC66",
    },
    {
        "id": "state_merit",
        "title": "State Higher Education Merit Scholarship",
        "description": "State-level merit scheme for undergraduate and postgraduate students in technical courses.",
        "icon": "🌟",
        "tag": "State Govt Scheme",
        "tag_color": "#9933FF",
    },
]

AI_SUGGESTIONS: list[dict] = [
    {
        "icon": "🎓",
        "title": "State Domicile Scholarship Match",
        "body": "Based on your address state, you qualify for State Merit & Domicile Fee Concessions.",
        "color": "#FF7A00",
    },
    {
        "icon": "💰",
        "title": "Income Certificate Requirement",
        "body": "Ensure your Tehsildar-issued Income Certificate is updated for FY 2025-26.",
        "color": "#059669",
    },
    {
        "icon": "🏛️",
        "title": "Bank Account Seeding Notice",
        "body": "Your bank account must be Aadhaar-seeded for direct DBT scholarship transfer.",
        "color": "#2563EB",
    },
]

MOCK_CONFIDENCE_SCORES: dict[str, int] = {
    "Name": 98,
    "City": 95,
    "State": 92,
    "Course": 96,
    "Year": 90,
    "Income": 94,
}

# 9 Supported Indian Languages (including Odia)
LANGUAGES: list[tuple[str, str, str, str]] = [
    ("hi", "Hindi",     "हिन्दी",    "hi-IN"),
    ("or", "Odia",      "ଓଡ଼ିଆ",    "or-IN"),
    ("ta", "Tamil",     "தமிழ்",    "ta-IN"),
    ("te", "Telugu",    "తెలుగు",   "te-IN"),
    ("bn", "Bengali",    "বাংলা",   "bn-IN"),
    ("mr", "Marathi",    "मराठी",   "mr-IN"),
    ("kn", "Kannada",    "ಕನ್ನಡ",   "kn-IN"),
    ("ml", "Malayalam",  "മലയാളം", "ml-IN"),
    ("en", "English",    "English", "en-IN"),
]

LANGUAGE_NAMES: list[str] = [lang[1] for lang in LANGUAGES]

INDIAN_STATES: list[str] = [
    "— Select —",
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Puducherry",
]

MOCK_TRANSCRIPTS: dict[str, str] = {
    "Hindi": (
        "मेरा नाम राहुल शर्मा है। मैं जयपुर राजस्थान का रहने वाला हूँ। "
        "मैं B.Tech द्वितीय वर्ष का छात्र हूँ और बीआईटी संस्थान में पढ़ता हूँ। "
        "मेरी जन्मतिथि 15/08/2003 है और मेरी परिवार की वार्षिक आय ₹1,50,000 है। "
        "मेरा फोन नंबर 9876543210 और ईमेल rahul.sharma@example.com है।"
    ),
    "Odia": (
        "ମୋର ନାମ ରାହୁଲ ଶର୍ମା | ମୁଁ ଭୁବନେଶ୍ୱର ଓଡ଼ିଶାର ରହୁଛି | "
        "ମୁଁ B.Tech ଦ୍ୱିତୀୟ ବର୍ଷର ଛାତ୍ର | "
        "ମୋର ବାର୍ଷିକ ପରିବାର ଆୟ ₹1,50,000 | "
        "ମୋର ଫୋନ୍ ନମ୍ବର 9876543210 ଏବଂ ଇମେଲ୍ rahul.sharma@example.com |"
    ),
    "English": (
        "My name is Rahul Sharma. I live in Jaipur, Rajasthan. "
        "I am a student of B.Tech Second Year studying at BIT Institute. "
        "My date of birth is 15/08/2003 and my annual family income is ₹1,50,000. "
        "My phone number is 9876543210 and email is rahul.sharma@example.com."
    ),
    "Tamil": (
        "என் பெயர் ராகுல் சர்மா. நான் ஜெய்ப்பூர் ராஜஸ்தானில் வசிக்கிறேன். "
        "நான் பி.டெக் இரண்டாம் ஆண்டு மாணவர். என் ஆண்டு வருமானம் ₹1,50,000. "
        "என் தொலைபேசி எண் 9876543210 மற்றும் மின்னஞ்சல் rahul.sharma@example.com."
    ),
    "Telugu": (
        "నా పేరు రాహుల్ శర్మ. నేను జైపూర్ రాజస్థాన్‌లో నివసిస్తున్నాను. "
        "నేను బి.టెక్ రెండవ సంవత్సరం విద్యార్థిని. నా వార్షిక ఆదాయం ₹1,50,000. "
        "నా ఫోన్ నంబర్ 9876543210 మరియు ఇమెయిల్ rahul.sharma@example.com."
    ),
    "Bengali": (
        "আমার নাম রাহুল শর্মা। আমি জয়পুর রাজস্থানে থাকি। "
        "আমি বি.টেک দ্বিতীয় বর্ষের ছাত্র। আমার বার্ষিক আয় ₹১,৫০,০০০। "
        "আমার ফোন নম্বর ৯৮৭৬৫৪৩২১০ এবং ইমেল rahul.sharma@example.com।"
    ),
    "Marathi": (
        "माझे नाव राहुल शर्मा आहे. मी जयपूर राजस्थान येथे राहतो. "
        "मी बी.टेक द्वितीय वर्षाचा विद्यार्थी आहे. माझे वार्षिक उत्पन्न ₹1,50,000 आहे. "
        "माझा फोन नंबर 9876543210 आणि ई-मेल rahul.sharma@example.com आहे."
    ),
    "Kannada": (
        "ನನ್ನ ಹೆಸರು ರಾಹುಲ್ ಶರ್ಮಾ. ನಾನು ಜೈಪುರ ರಾಜಸ್ಥಾನದಲ್ಲಿ ವಾಸಿಸುತ್ತಿದ್ದೇನೆ. "
        "ನಾನು ಬಿ.ಟೆಕ್ ಎರಡನೇ ವರ್ಷದ ವಿದ್ಯಾರ್ಥಿ. ನನ್ನ ವಾರ್ಷಿಕ ಆದಾಯ ₹1,50,000. "
        "ನನ್ನ ಫೋನ್ ಸಂಖ್ಯೆ 9876543210 ಮತ್ತು ಇಮೇಲ್ rahul.sharma@example.com."
    ),
    "Malayalam": (
        "എന്റെ പേര് രാഹുൽ ശർമ്മ. ഞാൻ ജയ്പൂർ രാജസ്ഥാനിൽ താമസിക്കുന്നു. "
        "ഞാൻ ബി.ടെക് രണ്ടാം വർഷ വിദ്യാർത്ഥിയാണ്. എന്റെ വാർഷിക വരുമാനം ₹1,50,000. "
        "എന്റെ ഫോൺ നമ്പർ 9876543210 ഉം ഇമെയിൽ rahul.sharma@example.com ഉം ആണ്."
    ),
}

AI_PROCESSING_STEPS: list[tuple[str, str, float]] = [
    ("🎙️", "Converting speech audio & running language detection...", 0.4),
    ("🤖", "Applying Gemma AI NLP entity recognition...", 0.5),
    ("📋", "Structuring personal, academic & income entities...", 0.4),
    ("✨", "Evaluating scholarship scheme eligibility rules...", 0.3),
]
