# 🎙️ Bharat Voice2Form

> **AI-Powered Form Filling in Indian Languages**  
> Speak in your language. Fill any form instantly.

---

## 📋 Overview

Bharat Voice2Form is a modern Streamlit prototype that demonstrates how AI (Gemma) can
help rural and semi-urban users fill government forms by speaking naturally in their
preferred Indian language.

## 🚀 Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Landing page with stats, how-it-works, and language support |
| 📋 **Form Selection** | Choose from 5 form types (Scholarship is functional) |
| 🎙️ **Voice Input** | Mock recording with waveform animation & multi-language transcripts |
| 🤖 **AI Processing** | Simulated Gemma extraction with confidence scores |
| 📝 **Auto-Fill Form** | Pre-filled editable scholarship form with AI suggestion panel |
| 👁️ **Preview** | Full application preview table with field status |
| ✅ **Success** | Confirmation page with application number and next steps |

## 🛠️ Setup & Run

```bash
# 1. Install dependencies
py -3.14 -m pip install -r requirements.txt

# 2. Run the app
py -3.14 -m streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

## 🗂️ Project Structure

```
bharat_voice2form/
├── app.py                  # Main entry point & routing
├── styles.py               # Global CSS, theme tokens, HTML helpers
├── requirements.txt
├── .streamlit/
│   └── config.toml         # Streamlit theme config
└── pages/
    ├── home.py             # Home page
    ├── form_selection.py   # Form selection grid
    ├── voice_input.py      # Voice recording & transcript
    ├── ai_processing.py    # AI simulation & JSON output
    ├── auto_fill.py        # Editable form + AI suggestions
    ├── preview.py          # Preview table + submission
    └── success.py          # Success / confirmation
```

## 🌐 Supported Languages

Hindi · Tamil · Telugu · Bengali · Marathi · Kannada · Malayalam · English

## 🎨 Design

- India tricolour accents (saffron, white, green)
- Deep navy blue primary (#002868)
- Inter font, glassmorphism cards, smooth animations
- Government-tech professional aesthetic

## 📝 Notes

- **No backend or API** — fully mock/prototype
- Scholarship Application is the only functional form
- PDF generation is simulated (mock)
- All speech recognition is replaced with pre-written mock transcripts

---

*Built with ❤️ for Bharat | Powered by Gemma AI (Google)*
