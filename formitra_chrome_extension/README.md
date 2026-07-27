# 🎙️ Formitra Chrome Extension — AI Voice Form Auto-Filler

> **Speak in any of 9 Indian Languages to auto-fill ANY web page form instantly using Web Speech API & Gemma AI intent extraction.**

---

## 🌟 Features
- **🌐 9 Indian Languages Supported**: Hindi, English, Odia, Tamil, Telugu, Bengali, Marathi, Kannada, Malayalam.
- **⚡ Instant Web Form Auto-Fill**: Automatically detects form inputs on any website (National Scholarship Portal, State Portals, College portals, Google Forms, custom web applications) and populates your spoken data.
- **🤖 Gemma AI Extraction**: Parses names, DOB, income, state, city, college, course, aadhaar, mobile, and email automatically.
- **✨ Visual Feedback**: Highlights auto-filled fields on the active webpage with glowing emerald borders and temporary checkmark tooltips.
- **🛡️ Manifest V3 Compliant**: Built strictly with standard Google Chrome Manifest V3 security standards.

---

## 🚀 How to Install in Google Chrome / Edge / Brave

1. **Open Chrome Extensions**:
   - In Google Chrome, navigate to `chrome://extensions/`
   - (Or in Microsoft Edge, go to `edge://extensions/`)

2. **Enable Developer Mode**:
   - Turn **ON** the **"Developer mode"** toggle switch in the top-right corner.

3. **Load Unpacked Extension**:
   - Click the **"Load unpacked"** button in the top-left toolbar.
   - Browse and select the folder:
     `e:\codes\AntiGravity Google\chess\AI_made\formitra_chrome_extension\`

4. **Pin Formitra to Extension Bar**:
   - Click the puzzle icon (🧩) in Chrome's top right toolbar.
   - Click the pin icon next to **Formitra — AI Voice Form Auto-Filler**.

---

## 📖 How to Use

1. Navigate to **ANY web page** containing a form (e.g. NSP Portal, Formitra Streamlit app, or any HTML form).
2. Click the **Formitra extension icon (🎙️)** in your browser toolbar.
3. Select your preferred dictation language (e.g. `Hindi`).
4. Click the **glowing mic button** and speak your details (or click **"📋 Load Demo"**).
5. Click **"✨ Auto-Fill Active Web Page Form"**.
6. Watch your form fields populate instantly with glowing green visual feedback!

---

## 📁 Extension File Structure
```
formitra_chrome_extension/
├── manifest.json      # Chrome Manifest V3 specification
├── popup.html         # Extension popup interface
├── popup.css          # Glassmorphism darkmode styling & animations
├── popup.js           # Speech recognition & Gemma AI parser
├── content.js         # Injected DOM scanner & auto-fill engine
├── background.js      # Service worker & context menus
├── README.md          # Installation guide
└── icons/             # Formitra Multilingual Brand Icons (16x16, 48x48, 128x128)
```
