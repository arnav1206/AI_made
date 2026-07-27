"""
utils/translations.py
======================
Multilingual translation dictionary for Formitra.
Supports 9 Indian Languages: Hindi, Odia, Tamil, Telugu, Bengali, Marathi, Kannada, Malayalam, English.
"""

from __future__ import annotations

import streamlit as st
from utils.constants import LANGUAGES

# Full Translation Registry
_TRANSLATIONS: dict[str, dict[str, str]] = {
    # ── App Header & Brand ──────────────────────────────────────────
    "app_title": {
        "English": "Formitra", "Hindi": "फॉर्ममित्र", "Odia": "ଫର୍ମମିତ୍ର",
        "Tamil": "ஃபார்ம்மিত্রா", "Telugu": "ఫార్మ్‌మిత్ర", "Bengali": "ফর্মমিত্র",
        "Marathi": "फॉर्ममित्र", "Kannada": "ಫಾರ್ಮ್‌ಮಿತ್ರ", "Malayalam": "ഫോംമിത്ര",
    },
    "app_sub": {
        "English": "AI Voice-Powered Form Filling & Scholarship Portal",
        "Hindi": "एआई वोइस-संचालित फॉर्म भरने और छात्रवृत्ति पोर्टल",
        "Odia": "ଏଆଇ ଭଏସ୍-ଚାଳିତ ଫର୍ମ ପୂରଣ ଏବଂ ଛାତ୍ରବୃତ୍ତି ପୋର୍ଟାଲ୍",
        "Tamil": "AI குரல்-இயக்கப்படும் படிவம் நிரப்புதல் மற்றும் உதவித்தொகை போர்டல்",
        "Telugu": "AI వాయిస్-ఆధారిత ఫారమ్ నింపడం మరియు స్కాలర్‌షిప్ పోర్టల్",
        "Bengali": "এআই ভয়েস-চালিত ফর্ম পূরণ এবং স্কলারশিপ পোর্টাল",
        "Marathi": "एआय व्हॉइस-संचालित फॉर्म भरणे आणि शिष्यवृत्ती पोर्टल",
        "Kannada": "AI ಧ್ವನಿ-ಚಾಲಿತ ಫಾರ್ಮ್ ಭರ್ತಿ ಮತ್ತು ಸ್ಕಾಲರ್‌ಶಿಪ್ ಪೋರ್ಟಲ್",
        "Malayalam": "AI വോയ്‌സ്-അധിഷ്‌ഠിത ഫോം ഫില്ലിംഗ് & സ്കോളർഷിപ്പ് പോർട്ടൽ",
    },

    # ── Theme Toggle ────────────────────────────────────────────────
    "theme_light": {
        "English": "☀️ Light Mode", "Hindi": "☀️ लाइट मोड", "Odia": "☀️ ଲାଇଟ୍ ମୋଡ୍",
        "Tamil": "☀️ ஒளி முறை", "Telugu": "☀️ లైట్ మోడ్", "Bengali": "☀️ 라이ট মোড",
        "Marathi": "☀️ लाईट मोड", "Kannada": "☀️ ಲೈಟ್ ಮೋಡ್", "Malayalam": "☀️ ലൈറ്റ് മോಡ್",
    },
    "theme_dark": {
        "English": "🌙 Dark Mode", "Hindi": "🌙 डार्क मोड", "Odia": "🌙 ଡାର୍କ ମୋଡ୍",
        "Tamil": "🌙 இருண்ட முறை", "Telugu": "🌙 డార్క్ మోడ్", "Bengali": "🌙 ডার্ক મોડ",
        "Marathi": "🌙 डार्क मोड", "Kannada": "🌙 ಡಾರ್ಕ್ ಮೋಡ್", "Malayalam": "🌙 ഡાર્ക്ക് മോഡ്",
    },

    # ── Sidebar Navigation ──────────────────────────────────────────
    "nav_heading": {
        "English": "NAVIGATION", "Hindi": "नेविगेशन", "Odia": "ନେଭିଗେସନ୍",
        "Tamil": "வழிசெலுத்தல்", "Telugu": "నావిగేషన్", "Bengali": "ন্যাভিগেশন",
        "Marathi": "नेव्हिगेशन", "Kannada": "ನ್ಯಾವಿಗೇಷನ್", "Malayalam": "നാവിഗേഷൻ",
    },
    "nav_login": {
        "English": "🔑 User Login", "Hindi": "🔑 लॉगिन", "Odia": "🔑 ଲଗଇନ୍",
        "Tamil": "🔑 உள்நுழை", "Telugu": "🔑 లాగిన్", "Bengali": "🔑 লগইন",
        "Marathi": "🔑 लॉगिन", "Kannada": "🔑 ಲಾಗಿನ್", "Malayalam": "🔑 ലോഗിൻ",
    },
    "nav_register": {
        "English": "📝 Register", "Hindi": "📝 पंजीकरण", "Odia": "📝 ପଞ୍ଜୀକରଣ",
        "Tamil": "📝 பதிவு", "Telugu": "📝 నమోదు", "Bengali": "📝 নিবন্ধন",
        "Marathi": "📝 नोंदणी", "Kannada": "📝 ನೋಂದಣಿ", "Malayalam": "📝 രജിസ്ട്രേഷൻ",
    },
    "nav_admin": {
        "English": "🛡️ Admin Portal", "Hindi": "🛡️ एडमिन पोर्टल", "Odia": "🛡️ ଆଡମିନ୍ ପୋର୍ଟାଲ୍",
        "Tamil": "🛡️ நிர்வாகி போர்டல்", "Telugu": "🛡️ అడ్మిన్ పోర్టల్", "Bengali": "🛡️ অ্যাডমিন পোর্টাল",
        "Marathi": "🛡️ ॲडमिन पोर्टल", "Kannada": "🛡️ ಅಡ್ಮಿನ್ ಪೋರ್ಟಲ್", "Malayalam": "🛡️ അഡ്മിൻ പോർട്ടൽ",
    },
    "nav_home": {
        "English": "🏠 Home", "Hindi": "🏠 मुख्य पृष्ठ", "Odia": "🏠 ମୁଖ୍ୟ ପୃଷ୍ଠା",
        "Tamil": "🏠 முகப்பு", "Telugu": "🏠 హోమ్", "Bengali": "🏠 হোম",
        "Marathi": "🏠 मुख्यपृष्ठ", "Kannada": "🏠 ಮುಖಪುಟ", "Malayalam": "🏠 ഹോം",
    },
    "nav_form_selection": {
        "English": "📋 Select Form", "Hindi": "📋 फॉर्म चुनें", "Odia": "📋 ଫର୍ମ ବାଛନ୍ତୁ",
        "Tamil": "📋 படிவம் தேர்வு", "Telugu": "📋 ఫారమ్ ఎంచుకోండి", "Bengali": "📋 ফর্ম নির্বাচন",
        "Marathi": "📋 फॉर्म निवडा", "Kannada": "📋 ಫಾರ್ಮ್ ಆಯ್ಕೆಮಾಡಿ", "Malayalam": "📋 ഫോം തിരഞ്ഞെടുക്കുക",
    },
    "nav_voice_input": {
        "English": "🎙️ Voice Input", "Hindi": "🎙️ वॉइस इनपुट", "Odia": "🎙️ ଭଏସ୍ ଇନପୁଟ୍",
        "Tamil": "🎙️ குரல் உள்ளீடு", "Telugu": "🎙️ వాయిస్ ఇన్‌పుట్", "Bengali": "🎙️ ভয়েস ইনপুট",
        "Marathi": "🎙️ व्हॉइस इनपुट", "Kannada": "🎙️ ಧ್ವನಿ ಇನ್ಪುಟ್", "Malayalam": "🎙️ വോയ്‌സ് ഇൻപുട്ട്",
    },
    "nav_ai_processing": {
        "English": "🤖 AI Processing", "Hindi": "🤖 AI प्रोसेसिंग", "Odia": "🤖 AI ପ୍ରୋସେସିଂ",
        "Tamil": "🤖 AI လုပ်முறை", "Telugu": "🤖 AI ప్రాసెసింగ్", "Bengali": "🤖 এআই প্রসেসিং",
        "Marathi": "🤖 AI प्रोसेसिंग", "Kannada": "🤖 AI ಪ್ರೊಸೆಸಿಂಗ್", "Malayalam": "🤖 AI പ്രോസസിംഗ്",
    },
    "nav_auto_fill": {
        "English": "✍️ Form Review", "Hindi": "✍️ फॉर्म समीक्षा", "Odia": "✍️ ଫର୍ମ ସମୀକ୍ଷା",
        "Tamil": "✍️ படிவ ஆய்வு", "Telugu": "✍️ ఫారమ్ సమీక్ష", "Bengali": "✍️ ফর্ম পর্যালোচনা",
        "Marathi": "✍️ फॉर्म पुनरावलोकन", "Kannada": "✍️ ಪರಿಶೀಲನೆ", "Malayalam": "✍️ ഫോം അവലോകനം",
    },
    "nav_preview": {
        "English": "👁️ Preview", "Hindi": "👁️ पूर्वावलोकन", "Odia": "👁️ ପୂର୍ବାବଲୋକନ",
        "Tamil": "👁️ முன்னோட்டம்", "Telugu": "👁️ పూర్వవీక్షణం", "Bengali": "👁️ প্রাকদর্শন",
        "Marathi": "👁️ पूर्वदृश्य", "Kannada": "👁️ ಮುನ್ನೋಟ", "Malayalam": "👁️ ପ୍ରୀବୂ",
    },
    "nav_success": {
        "English": "🎉 Submitted", "Hindi": "🎉 जमा हुआ", "Odia": "🎉 ଦାଖଲ ହେଲା",
        "Tamil": "🎉 சமர்ப்பிக்கப்பட்டது", "Telugu": "🎉 సమర్పించబడింది", "Bengali": "🎉 জমা দেওয়া হয়েছে",
        "Marathi": "🎉 सबमिट केले", "Kannada": "🎉 ಸಲ್ಲಿಸಲಾಗಿದೆ", "Malayalam": "🎉 സമർപ്പിച്ചു",
    },
    "nav_track_status": {
        "English": "🔍 Track Status", "Hindi": "🔍 ट्रैक स्थिति", "Odia": "🔍 ଟ୍ରାକ୍ ସ୍ଥିତି",
        "Tamil": "🔍 தடமறி நிலை", "Telugu": "🔍 ట్రాక్ స్థితి", "Bengali": "🔍 ট্র্যাকিং স্ট্যাটাস",
        "Marathi": "🔍 ट्रॅक स्थिती", "Kannada": "🔍 ಟ್ರ್ಯಾಕ್ ಸ್ಥಿತಿ", "Malayalam": "🔍 ട്രാക്ക് സ്റ്റാറ്റസ്",
    },
    "nav_help_faq": {
        "English": "❓ Help & FAQ", "Hindi": "❓ सहायता व प्रश्न", "Odia": "❓ ସହାୟତା ଏବଂ ପ୍ରଶ୍ନ",
        "Tamil": "❓ உதவி & கேள்வி", "Telugu": "❓ సహాయం & ప్రశ్నలు", "Bengali": "❓ সাহায্য ও প্রশ্ন",
        "Marathi": "❓ मदत आणि प्रश्न", "Kannada": "❓ ಸಹಾಯ & ಪ್ರಶ್ನೆಗಳು", "Malayalam": "❓ സഹായവും ചോദ്യങ്ങളും",
    },

    # ── Voice Input View ───────────────────────────────────────────
    "voice_title": {
        "English": "🎙️ Voice Input & Multilingual Speech Dictation",
        "Hindi": "🎙️ वॉइस इनपुट एवं बहुभाषी वाक् डिक्टेशन",
        "Odia": "🎙️ ଭଏସ୍ ଇନପୁଟ୍ ଏବଂ ବହୁଭାଷୀ ଡିକ୍ଟେସନ୍",
    },
    "voice_sub": {
        "English": "Speak in your native language or upload an audio clip for real-time AI transcription.",
        "Hindi": "अपनी मातृभाषा में बोलें या रीयल-टाइम एआई ट्रांसक्रिप्शन के लिए ऑडियो रिकॉर्ड करें।",
        "Odia": "ଆପଣଙ୍କ ମାତୃଭାଷାରେ କୁହନ୍ତୁ କିମ୍ବା ଅଡିଓ ରେକର୍ଡ କରନ୍ତୁ।",
    },
    "select_language": {
        "English": "Select Dictation Language",
        "Hindi": "डिक्टेशन भाषा चुनें",
        "Odia": "ଡିକ୍ଟେସନ୍ ଭାଷା ବାଛନ୍ତୁ",
    },
    "demo_note": {
        "English": "💡 Tip: Tap 'Load Sample Transcript' to test Gemma AI extraction without microphone recording.",
        "Hindi": "💡 सुझाव: बिना माइक के परीक्षण करने के लिए 'नमूना ट्रांसक्रिप्ट लोड करें' पर टैप करें।",
        "Odia": "💡 ଟିପ୍: 'ନମୁନା ଟ୍ରାନ୍ସକ୍ରିପ୍ଟ ଲୋଡ୍ କରନ୍ତୁ' ଉପରେ ଟ୍ୟାପ୍ କରନ୍ତୁ।",
    },
    "no_transcript": {
        "English": "Please dictate speech or type text into the transcript area before proceeding.",
        "Hindi": "आगे बढ़ने से पहले कृपया बोलें या पाठ दर्ज करें।",
        "Odia": "ଆଗକୁ ବଢିବା ପୂର୍ବରୁ ଦୟାକରି କୁହନ୍ତୁ।",
    },

    # ── AI Processing View ─────────────────────────────────────────
    "ai_title": {
        "English": "🤖 Gemma AI Multilingual Entity Extraction",
        "Hindi": "🤖 गेम्मा एआई बहुभाषी संस्था निष्कर्षण",
        "Odia": "🤖 Gemma AI ବହୁଭାଷୀ ତଥ୍ୟ ନିଷ୍କାସନ",
    },
    "ai_sub": {
        "English": "Structuring speech audio into verified scholarship application entities.",
        "Hindi": "वाक् ऑडियो को सत्यापित छात्रवृत्ति आवेदन संस्थाओं में संरचित करना।",
        "Odia": "ଭଏସ୍ ଅଡିଓକୁ ଯାଞ୍ଚ ହୋଇଥିବା ତଥ୍ୟରେ ସଂରଚିତ କରିବା।",
    },
    "field_mapping": {
        "English": "📋 Field Mapping Audit",
        "Hindi": "📋 फ़ील्ड मैपिंग ऑडिट",
        "Odia": "📋 ଫିଲ୍ଡ ମ୍ୟାପିଂ ଅଡିଟ୍",
    },
    "field_mapping_sub": {
        "English": "Comparison between extracted audio data and required scholarship fields.",
        "Hindi": "निकाले गए ऑडियो डेटा और आवश्यक छात्रवृत्ति फ़ील्ड के बीच तुलना।",
        "Odia": "ବାହାର କରାଯାଇଥିବା ତଥ୍ୟ ଏବଂ ଆବଶ୍ୟକ ଫିଲ୍ଡ ମଧ୍ୟରେ ତୁଳନା।",
    },

    # ── Auto-Fill & Review View ────────────────────────────────────
    "autofill_title": {
        "English": "✍️ Form Review & Voice Auto-Fill",
        "Hindi": "✍️ फॉर्म समीक्षा एवं वॉइस ऑटो-फिल",
        "Odia": "✍️ ଫର୍ମ ସମୀକ୍ଷା ଏବଂ ଭଏସ୍ ଅଟୋ-ଫିଲ୍",
    },
    "autofill_sub": {
        "English": "Review extracted application details or speak directly into any field to auto-update.",
        "Hindi": "निकाले गए आवेदन विवरण की समीक्षा करें या स्वतः अपडेट करने के लिए किसी भी फ़ील्ड में बोलें।",
        "Odia": "ବାହାର କରାଯାଇଥିବା ଆବେଦନ ବିବରଣୀ ସମୀକ୍ଷା କରନ୍ତୁ କିମ୍ବା ସିଧାସଳଖ କୁହନ୍ତୁ।",
    },
    "section_personal": {
        "English": "👤 Personal Information", "Hindi": "👤 व्यक्तिगत जानकारी", "Odia": "👤 ବ୍ୟକ୍ତିଗତ ସୂଚନା",
    },
    "section_address": {
        "English": "📍 Address & Domicile Details", "Hindi": "📍 पता एवं मूल निवास विवरण", "Odia": "📍 ଠିକଣା ଏବଂ ନିବାସ ବିବରଣୀ",
    },
    "section_academic": {
        "English": "🎓 Academic Details", "Hindi": "🎓 शैक्षणिक विवरण", "Odia": "🎓 ଶିକ୍ଷାଗତ ବିବରଣୀ",
    },
    "section_financial": {
        "English": "💰 Financial & Contact Details", "Hindi": "💰 वित्तीय एवं संपर्क विवरण", "Odia": "💰 ଆର୍ଥିକ ଏବଂ ଯୋଗାଯୋଗ ବିବରଣୀ",
    },
    "btn_re_record": {
        "English": "🎙️ Re-record Voice", "Hindi": "🎙️ पुनः वॉइस रिकॉर्ड करें", "Odia": "🎙️ ପୁନଃ ରେକର୍ଡ କରନ୍ତୁ",
    },
    "btn_clear": {
        "English": "🗑️ Clear Form", "Hindi": "🗑️ फॉर्म साफ़ करें", "Odia": "🗑️ ଫର୍ମ ସଫା କରନ୍ତୁ",
    },
    "btn_preview": {
        "English": "👁️ Final Preview →", "Hindi": "👁️ अंतिम पूर्वावलोकन →", "Odia": "👁️ ଅନ୍ତିମ ପୂର୍ବାବଲୋକନ →",
    },

    # ── Application Preview View ───────────────────────────────────
    "preview_title": {
        "English": "👁️ Application Preview & PDF Generation",
        "Hindi": "👁️ आवेदन पूर्वावलोकन एवं पीडीएफ जनरेशन",
        "Odia": "👁️ ଆବେଦନ ପୂର୍ବାବଲୋକନ ଏବଂ PDF ଜନରେସନ୍",
    },
    "preview_sub": {
        "English": "Verify your application details before official submission.",
        "Hindi": "आधिकारिक जमा करने से पहले अपने आवेदन विवरण की पुष्टि करें।",
        "Odia": "ସରକାରୀ ଦାଖଲ ପୂର୍ବରୁ ଆପଣଙ୍କର ଆବେଦନ ଯାଞ୍ଚ କରନ୍ତୁ।",
    },
    "app_number": {
        "English": "APPLICATION REF CODE", "Hindi": "आवेदन संदर्भ कोड", "Odia": "ଆବେଦନ ରେଫରେନ୍ସ କୋଡ୍",
    },
    "declaration_title": {
        "English": "📜 Applicant Self-Declaration", "Hindi": "📜 आवेदक स्व-घोषणा", "Odia": "📜 ଆବେଦନକାରୀ ସ୍ୱ-ଘୋଷଣା",
    },
    "declaration_text": {
        "English": "I hereby declare that all information provided above is true and correct to the best of my knowledge. I understand that any false statement will disqualify my scholarship application.",
        "Hindi": "मैं एतद्द्वारा घोषणा करता हूं कि ऊपर दी गई सभी जानकारी मेरी जानकारी के अनुसार सत्य और सही है।",
        "Odia": "ମୁଁ ଏତଦ୍ଦ୍ୱାରା ଘୋଷଣା କରୁଛି ଯେ ଉପରେ ଦିଆଯାଇଥିବା ସମସ୍ତ ସୂଚନା ସତ୍ୟ ଅଟେ।",
    },
    "declaration_check": {
        "English": "I accept the self-declaration and confirm my details are accurate.",
        "Hindi": "मैं स्व-घोषणा स्वीकार करता हूं और विवरण की पुष्टि करता हूं।",
        "Odia": "ମୁଁ ସ୍ୱ-ଘୋଷଣା ଗ୍ରହଣ କରୁଛି ଏବଂ ବିବରଣୀ ନିଶ୍ଚିତ କରୁଛି।",
    },
    "btn_edit": {
        "English": "✏️ Edit Application", "Hindi": "✏️ आवेदन संपादित करें", "Odia": "✏️ ଆବେଦନ ସମ୍ପାଦନ କରନ୍ତୁ",
    },
    "btn_pdf": {
        "English": "📄 Generate Official PDF", "Hindi": "📄 आधिकारिक पीडीएफ बनाएं", "Odia": "📄 ସରକାରୀ PDF ପ୍ରସ୍ତୁତ କରନ୍ତୁ",
    },
    "btn_submit": {
        "English": "🚀 Submit Application →", "Hindi": "🚀 आवेदन जमा करें →", "Odia": "🚀 ଆବେଦନ ଦାଖଲ କରନ୍ତୁ →",
    },
    "download_pdf": {
        "English": "📥 Download PDF Certificate", "Hindi": "📥 डाउनलोड पीडीएफ प्रमाण पत्र", "Odia": "📥 PDF ଡାଉନଲୋଡ୍ କରନ୍ତୁ",
    },
    "accept_declaration": {
        "English": "Please accept the self-declaration above to enable submission.",
        "Hindi": "जमा करने के लिए कृपया ऊपर स्व-घोषणा स्वीकार करें।",
        "Odia": "ଦାଖଲ କରିବାକୁ ଦୟାକରି ସ୍ୱ-ଘୋଷଣା ଗ୍ରହଣ କରନ୍ତୁ।",
    },

    # ── Form Selection View ─────────────────────────────────────────
    "select_form": {
        "English": "📋 Select Scholarship Scheme", "Hindi": "📋 छात्रवृत्ति योजना चुनें", "Odia": "📋 ଛାତ୍ରବୃତ୍ତି ଯୋଜନା ବାଛନ୍ତୁ",
    },
    "select_form_sub": {
        "English": "Choose your application portal to start voice dictation.",
        "Hindi": "वॉइस डिक्टेशन शुरू करने के लिए अपना आवेदन पोर्टल चुनें।",
        "Odia": "ଭଏସ୍ ଡିକ୍ଟେସନ୍ ଆରମ୍ଭ କରିବାକୁ ଆପଣଙ୍କର ଆବେଦନ ପୋର୍ଟାଲ୍ ବାଛନ୍ତୁ।",
    },
    "select_btn": {
        "English": "Start Voice Application →", "Hindi": "वॉइस आवेदन शुरू करें →", "Odia": "ଭଏସ୍ ଆବେଦନ ଆରମ୍ଭ କରନ୍ତୁ →",
    },
    "coming_soon": {
        "English": "Coming Soon", "Hindi": "शीघ्र आ रहा है", "Odia": "ଶୀଘ୍ର ଆସୁଛି",
    },
    "prototype_info": {
        "English": "💡 Formitra prototype v2.0 supports major central and state scholarship schemes.",
        "Hindi": "💡 फॉर्ममित्र प्रोटोटाइप v2.0 प्रमुख केंद्रीय और राज्य छात्रवृत्ति योजनाओं का समर्थन करता है।",
        "Odia": "💡 ଫର୍ମମିତ୍ର ପ୍ରୋଟୋଟାଇପ୍ v2.0 ସରକାରୀ ଛାତ୍ରବୃତ୍ତି ଯୋଜନାକୁ ସମର୍ଥନ କରେ।",
    },

    # ── UI Language Dropdown Label ─────────────────────────────────
    "ui_language": {
        "English": "🌐 Language / भाषा", "Hindi": "🌐 भाषा / Language", "Odia": "🌐 ଭାଷା / Language",
    },
    "selected_form_lbl": {
        "English": "SELECTED FORM", "Hindi": "चयनित फॉर्म", "Odia": "ଚୟନିତ ଫର୍ମ",
    },
    "language_lbl": {
        "English": "ACTIVE LANGUAGE", "Hindi": "सक्रिय भाषा", "Odia": "ସକ୍ରିୟ ଭାଷା",
    },
    "powered_by": {
        "English": "Powered by Gemma AI & VoiceAssist",
        "Hindi": "Gemma AI एवं VoiceAssist द्वारा संचालित",
        "Odia": "Gemma AI ଏବଂ VoiceAssist ଦ୍ୱାରା ପରିଚାଳିତ",
    },

    # ── Views: Home ────────────────────────────────────────────────
    "hero_title": {
        "English": "Speak in Your Language. Formitra Fills Your Application.",
        "Hindi": "अपनी भाषा में बोलें। फॉर्ममित्र आपका आवेदन भरेगा।",
        "Odia": "ଆପଣଙ୍କ ଭାଷାରେ କୁହନ୍ତୁ। ଫର୍ମମିତ୍ର ଆପଣଙ୍କ ଆବେଦନ ପୂରଣ କରିବ।",
    },
    "hero_sub": {
        "English": "India's first voice-driven scholarship form assistant supporting 9 official languages.",
        "Hindi": "9 आधिकारिक भाषाओं का समर्थन करने वाला भारत का पहला आवाज-संचालित छात्रवृत्ति फॉर्म सहायक।",
        "Odia": "9 ଟି ସରକାରୀ ଭାଷାକୁ ସମର୍ଥନ କରୁଥିବା ଭାରତର ପ୍ରଥମ ଭଏସ୍-ଚାଳିତ ଛାତ୍ରବୃତ୍ତି ଫର୍ମ ସହାୟକ।",
    },
}

_LIST_TRANSLATIONS: dict[str, list[str]] = {
    "gender_opts": ["Male", "Female", "Transgender", "Prefer not to say"],
    "category_opts": ["General", "OBC", "SC", "ST", "EWS / EBC"],
    "year_opts": ["First Year", "Second Year", "Third Year", "Fourth Year", "Fifth Year"],
}


def t(key: str, default: str | None = None) -> str:
    """Retrieve translated string for current language with English fallback."""
    lang = st.session_state.get("selected_language", "Hindi")
    if key in _TRANSLATIONS:
        entry = _TRANSLATIONS[key]
        if lang in entry:
            return entry[lang]
        if "English" in entry:
            return entry["English"]
    return default or key.replace("_", " ").title()


def tlist(key: str) -> list[str]:
    """Retrieve translated list of options."""
    return _LIST_TRANSLATIONS.get(key, ["— Select —"])


def get_available_languages() -> list[str]:
    """Return ordered list of language names."""
    return [lang[1] for lang in LANGUAGES]
