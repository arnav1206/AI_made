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
        "Tamil": "☀️ ஒளி முறை", "Telugu": "☀️ లైట్ మోడ్", "Bengali": "☀️ লাইট মোড",
        "Marathi": "☀️ लाईट मोड", "Kannada": "☀️ ಲೈಟ್ ಮೋಡ್", "Malayalam": "☀️ ലൈറ്റ് മോഡ്",
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
    "nav_home": {
        "English": "🏠 Home", "Hindi": "🏠 मुख्य पृष्ठ", "Odia": "🏠 ମୁଖ୍ୟ ପୃଷ୍ଠା",
        "Tamil": "🏠 முகப்பு", "Telugu": "🏠 హోమ్", "Bengali": "🏠 হোম",
        "Marathi": "🏠 मुख्यपृष्ठ", "Kannada": "🏠 ಮುಖಪುಟ", "Malayalam": "🏠 ഹോം",
    },
    "nav_login": {
        "English": "🔑 Login", "Hindi": "🔑 लॉगिन", "Odia": "🔑 ଲଗଇନ୍",
        "Tamil": "🔑 உள்நுழை", "Telugu": "🔑 లాగిన్", "Bengali": "🔑 লগইন",
        "Marathi": "🔑 लॉगिन", "Kannada": "🔑 ಲಾಗಿನ್", "Malayalam": "🔑 ലോഗിൻ",
    },
    "nav_register": {
        "English": "📝 Register", "Hindi": "📝 पंजीकरण", "Odia": "📝 ପଞ୍ଜୀକରଣ",
        "Tamil": "📝 பதிவு", "Telugu": "📝 నమోదు", "Bengali": "📝 নিবন্ধন",
        "Marathi": "📝 नोंदणी", "Kannada": "📝 ನೋಂದಣಿ", "Malayalam": "📝 രജിസ്ട്രേഷൻ",
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
        "Marathi": "✍️ फॉर्म पुनरावलोकन", "Kannada": "✍️ ಫಾರ್ಮ್ ಪರಿಶೀಲನೆ", "Malayalam": "✍️ ഫോം അവലോകനം",
    },
    "nav_preview": {
        "English": "👁️ Preview", "Hindi": "👁️ पूर्वावलोकन", "Odia": "👁️ ପୂର୍ବାବଲୋକନ",
        "Tamil": "👁️ முன்னோட்டம்", "Telugu": "👁️ పూర్వవీక్షణం", "Bengali": "👁️ প্রাকদর্শন",
        "Marathi": "👁️ पूर्वदृश्य", "Kannada": "👁️ ಮುನ್ನೋಟ", "Malayalam": "👁️ ପ୍ରୀവ്യൂ",
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

    # ── Form Selection View ─────────────────────────────────────────
    "select_form": {
        "English": "📋 Select Scholarship Scheme", "Hindi": "📋 छात्रवृत्ति योजना चुनें", "Odia": "📋 ଛାତ୍ରବୃତ୍ତି ଯୋଜନା ବାଛନ୍ତୁ",
        "Tamil": "📋 உதவித்தொகை திட்டத்தைத் தேர்ந்தெடுக்கவும்", "Telugu": "📋 స్కాలర్‌షిప్ పథకాన్ని ఎంచుకోండి", "Bengali": "📋 স্কলারশিপ স্কিম নির্বাচন করুন",
        "Marathi": "📋 शिष्यवृत्ती योजना निवडा", "Kannada": "📋 ಸ್ಕಾಲರ್‌ಶಿಪ್ ಯೋಜನೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ", "Malayalam": "📋 സ്‌കോളർഷിപ്പ് പദ്ധതി തിരഞ്ഞെടുക്കുക",
    },
    "select_form_sub": {
        "English": "Choose your application portal to start voice dictation.",
        "Hindi": "वॉइस डिक्टेशन शुरू करने के लिए अपना आवेदन पोर्टल चुनें।",
        "Odia": "ଭଏସ୍ ଡିକ୍ଟେସନ୍ ଆରମ୍ଭ କରିବାକୁ ଆପଣଙ୍କର ଆବେଦନ ପୋର୍ଟାଲ୍ ବାଛନ୍ତୁ।",
        "Tamil": "குரல் தட்டச்சு தொடங்க உங்கள் விண்ணப்ப போர்ட்டலைத் தேர்ந்தெடுக்கவும்.",
        "Telugu": "వాయిస్ డిక్టేషన్ ప్రారంభించడానికి మీ అప్లికేషన్ పోర్టల్‌ని ఎంచుకోండి.",
        "Bengali": "ভয়েস ডিক্টেশন শুরু করতে আপনার আবেদন পোর্টাল বেছে নিন।",
        "Marathi": "व्हॉइस डिक्टेशन सुरू करण्यासाठी तुमचा अर्ज पोर्टल निवडा.",
        "Kannada": "ಧ್ವನಿ ಡಿಕ್ಟೇಷನ್ ಪ್ರಾರಂಭಿಸಲು ನಿಮ್ಮ ಅರ್ಜಿ ಪೋರ್ಟಲ್ ಆಯ್ಕೆಮಾಡಿ.",
        "Malayalam": "വോയ്‌സ് ഡിക്‌റ്റേഷൻ ആരംഭിക്കാൻ നിങ്ങളുടെ ആപ്ലിക്കേഷൻ പോർട്ടൽ തിരഞ്ഞെടുക്കുക.",
    },
    "select_btn": {
        "English": "Start Voice Application →", "Hindi": "वॉइस आवेदन शुरू करें →", "Odia": "ଭଏସ୍ ଆବେଦନ ଆରମ୍ଭ କରନ୍ତୁ →",
        "Tamil": "குரல் விண்ணப்பத்தைத் தொடங்கு →", "Telugu": "వాయిస్ దరఖాస్తు ప్రారంభించండి →", "Bengali": "ভয়েস আবেদন শুরু করুন →",
        "Marathi": "व्हॉइस अर्ज सुरू करा →", "Kannada": "ಧ್ವನಿ ಅರ್ಜಿ ಪ್ರಾರಂಭಿಸಿ →", "Malayalam": "വോയ്‌സ് അപേക്ഷ ആരംഭിക്കുക →",
    },
    "coming_soon": {
        "English": "Coming Soon", "Hindi": "शीघ्र आ रहा है", "Odia": "ଶୀଘ୍ର ଆସୁଛି",
        "Tamil": "விரைவில்", "Telugu": "త్వరలో వస్తుంది", "Bengali": "শীঘ্রই আসছে",
        "Marathi": "लवकरच येत आहे", "Kannada": "ಶೀಘ್ರದಲ್ಲೇ ಬರಲಿದೆ", "Malayalam": "ഉടൻ വരുന്നു",
    },
    "prototype_info": {
        "English": "💡 Formitra prototype v2.0 supports major central and state scholarship schemes.",
        "Hindi": "💡 फॉर्ममित्र प्रोटोटाइप v2.0 प्रमुख केंद्रीय और राज्य छात्रवृत्ति योजनाओं का समर्थन करता है।",
        "Odia": "💡 ଫର୍ମମିତ୍ର ପ୍ରୋଟୋଟାଇପ୍ v2.0 ସରକାରୀ ଛାତ୍ରବୃତ୍ତି ଯୋଜନାକୁ ସମର୍ଥନ କରେ।",
        "Tamil": "💡 ஃபார்ம்மিত্রா முன்மாதிரி v2.0 முக்கிய உதவித்தொகை திட்டங்களை ஆதரிக்கிறது.",
        "Telugu": "💡 ఫార్మ్‌మిత్ర నమూనా v2.0 ప్రధాన స్కాలర్‌షిప్ పథకాలకు మద్దతు ఇస్తుంది.",
        "Bengali": "💡 ফর্মমিত্র প্রোটোটাইপ v2.0 প্রধান সরকারি স্কলারশিপ স্কিম সমর্থন করে।",
        "Marathi": "💡 फॉर्ममित्र प्रोटोटाइप v2.0 प्रामुख्याने शिष्यवृत्ती योजनांना पाठिंबा देतो.",
        "Kannada": "💡 ಫಾರ್ಮ್‌ಮಿತ್ರ ಪ್ರೊಟೊಟೈಪ್ v2.0 ಪ್ರಮುಖ ಸ್ಕಾಲರ್‌ಶಿಪ್ ಯೋಜನೆಗಳನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ.",
        "Malayalam": "💡 ഫോംമിത്ര പ്രോട്ടോടൈപ്പ് v2.0 പ്രധാന പദ്ധതികളെ പിന്തുണയ്ക്കുന്നു.",
    },

    # ── UI Language Dropdown Label ─────────────────────────────────
    "ui_language": {
        "English": "🌐 Language / भाषा", "Hindi": "🌐 भाषा / Language", "Odia": "🌐 ଭାଷା / Language",
        "Tamil": "🌐 மொழி / Language", "Telugu": "🌐 భాష / Language", "Bengali": "🌐 ভাষা / Language",
        "Marathi": "🌐 भाषा / Language", "Kannada": "🌐 ಭಾಷೆ / Language", "Malayalam": "🌐 ഭാഷ / Language",
    },
    "selected_form_lbl": {
        "English": "SELECTED FORM", "Hindi": "चयनित फॉर्म", "Odia": "ଚୟନିତ ଫର୍ମ",
        "Tamil": "தேர்ந்தெடுக்கப்பட்ட படிவம்", "Telugu": "ఎంచుకున్న ఫారమ్", "Bengali": "নির্বাচিত ফর্ম",
        "Marathi": "निवडलेला फॉर्म", "Kannada": "ಆಯ್ಕೆಮಾಡಿದ ಫಾರ್ಮ್", "Malayalam": "તિരഞ്ഞെടുത്ത ഫോം",
    },
    "language_lbl": {
        "English": "ACTIVE LANGUAGE", "Hindi": "सक्रिय भाषा", "Odia": "ସକ୍ରିୟ ଭାଷା",
        "Tamil": "செயலில் உள்ள மொழி", "Telugu": "సక్రియ భాష", "Bengali": "সক্রিয় ভাষা",
        "Marathi": "सक्रिय भाषा", "Kannada": "ಸಕ್ರಿಯ ಭಾಷೆ", "Malayalam": "സജീവ ഭാഷ",
    },
    "powered_by": {
        "English": "Powered by Gemma AI & VoiceAssist",
        "Hindi": "Gemma AI एवं VoiceAssist द्वारा संचालित",
        "Odia": "Gemma AI ଏବଂ VoiceAssist ଦ୍ୱାରା ପରିଚାଳିତ",
        "Tamil": "Gemma AI மற்றும் VoiceAssist மூலம் இயக்கப்படுகிறது",
        "Telugu": "Gemma AI మరియు VoiceAssist ద్వారా అందించబడింది",
        "Bengali": "Gemma AI এবং VoiceAssist চালিত",
        "Marathi": "Gemma AI आणि VoiceAssist द्वारे संचलित",
        "Kannada": "Gemma AI ಮತ್ತು VoiceAssist ನಿಂದ ಚಾಲಿತವಾಗಿದೆ",
        "Malayalam": "Gemma AI, VoiceAssist എന്നിവയാൽ പ്രവർത്തിക്കുന്നു",
    },

    # ── Views: Home ────────────────────────────────────────────────
    "hero_title": {
        "English": "Speak in Your Language. Formitra Fills Your Application.",
        "Hindi": "अपनी भाषा में बोलें। फॉर्ममित्र आपका आवेदन भरेगा।",
        "Odia": "ଆପଣଙ୍କ ଭାଷାରେ କୁହନ୍ତୁ। ଫର୍ମମିତ୍ର ଆପଣଙ୍କ ଆବେଦନ ପୂରଣ କରିବ।",
        "Tamil": "உங்கள் மொழியில் பேசுங்கள். பார்ம்மিত্রா உங்கள் விண்ணப்பத்தை நிரப்பும்.",
        "Telugu": "మీ భాషలో మాట్లాడండి. ఫార్మ్‌మిత్ర మీ దరఖాస్తును నింపుతుంది.",
        "Bengali": "আপনার ভাষায় কথা বলুন। ফর্মমিত্র আপনার আবেদন পূরণ করবে।",
        "Marathi": "तुमच्या भाषेत बोला. फॉर्ममित्र तुमचा अर्ज भरेल.",
        "Kannada": "ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಮಾತನಾಡಿ. ಫಾರ್ಮ್‌ಮಿತ್ರ ನಿಮ್ಮ ಅರ್ಜಿಯನ್ನು ಭರ್ತಿ ಮಾಡುತ್ತದೆ.",
        "Malayalam": "നിങ്ങളുടെ ഭാഷയിൽ സംസാരിക്കുക. ഫോംമിത്ര നിങ്ങളുടെ അപേക്ഷ പൂരിപ്പിക്കും.",
    },
    "hero_sub": {
        "English": "India's first voice-driven scholarship form assistant supporting 9 official languages.",
        "Hindi": "9 आधिकारिक भाषाओं का समर्थन करने वाला भारत का पहला आवाज-संचालित छात्रवृत्ति फॉर्म सहायक।",
        "Odia": "9 ଟି ସରକାରୀ ଭାଷାକୁ ସମର୍ଥନ କରୁଥିବା ଭାରତର ପ୍ରଥମ ଭଏସ୍-ଚାଳିତ ଛାତ୍ରବୃତ୍ତି ଫର୍ମ ସହାୟକ।",
        "Tamil": "9 அதிகாரிக மொழிகளை ஆதரிக்கும் இந்தியாவின் முதல் குரல்-இயக்கப்படும் உதவித்தொகை படிவ உதவியாளர்.",
        "Telugu": "9 అధికారిక భాషలకు మద్దతు ఇచ్చే భారతదేశపు మొదటి వాయిస్ ఆధారిత స్కాలర్‌షిప్ ఫారమ్ అసిస్టెంట్.",
        "Bengali": "৯টি অফিশিয়াল ভাষা সমর্থিত ভারতের প্রথম ভয়েস-চালিত স্কলারশিপ ফর্ম সহকারী।",
        "Marathi": "९ अधिकृत भाषांना पाठिंबा देणारा भारतातील पहिला व्हॉइस-चालित शिष्यवृत्ती फॉर्म सहाय्यक.",
        "Kannada": "9 ಅಧಿಕೃತ ಭಾಷೆಗಳನ್ನು ಬೆಂಬಲಿಸುವ ಭಾರತದ ಮೊದಲ ಧ್ವನಿ-ಚಾಲಿತ ಸ್ಕಾಲರ್‌ಶಿಪ್ ಫಾರ್ಮ್ ಸಹಾಯಕ.",
        "Malayalam": "9 ഔദ്യോഗിക ഭാഷകളെ പിന്തുണയ്ക്കുന്ന ഇന്ത്യയിലെ ആദ്യത്തെ വോയ്‌സ് നയിക്കുന്ന സ്കോളർഷിപ്പ് ഫോം അസിസ്റ്റന്റ്.",
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
