"""
components/web_speech.py
========================
Live streaming speech dictation component.
Performs real-time HTML5 browser speech-to-text in 8 Indian languages.
Transcribes live as user speaks, and returns the final transcribed text on stop.
"""

from __future__ import annotations

import streamlit as st

_LOCALE_MAP: dict[str, str] = {
    "Hindi":     "hi-IN",
    "Tamil":     "ta-IN",
    "Telugu":    "te-IN",
    "Bengali":   "bn-IN",
    "Marathi":   "mr-IN",
    "Kannada":   "kn-IN",
    "Malayalam": "ml-IN",
    "English":   "en-IN",
}


def render_live_speech_dictation(language: str = "Hindi") -> str | None:
    """
    Render HTML5 live speech transcription component.

    Parameters
    ----------
    language : str
        Target language name (e.g. "Hindi", "Tamil", "English").

    Returns
    -------
    str | None
        Live transcribed speech text.
    """
    locale = _LOCALE_MAP.get(language, "hi-IN")

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Inter', system-ui, sans-serif;
                margin: 0;
                padding: 4px;
                background: transparent;
            }}
            .dictation-card {{
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                border-radius: 20px;
                padding: 1.5rem;
                color: #FFFFFF;
                text-align: center;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            .mic-btn {{
                background: linear-gradient(135deg, #FF7A00 0%, #EA580C 100%);
                color: #FFFFFF;
                border: none;
                border-radius: 50px;
                padding: 0.9rem 2.2rem;
                font-size: 1.05rem;
                font-weight: 800;
                cursor: pointer;
                box-shadow: 0 6px 20px rgba(255, 122, 0, 0.4);
                transition: all 0.25s ease;
                display: inline-flex;
                align-items: center;
                gap: 0.6rem;
            }}
            .mic-btn:hover {{
                transform: translateY(-2px) scale(1.03);
                box-shadow: 0 10px 28px rgba(255, 122, 0, 0.5);
            }}
            .mic-btn.recording {{
                background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
                animation: pulse-recording 1.5s infinite;
                box-shadow: 0 0 20px rgba(220, 38, 38, 0.6);
            }}
            @keyframes pulse-recording {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
            }}
            .status-text {{
                font-size: 0.88rem;
                margin-top: 0.85rem;
                color: #94A3B8;
                font-weight: 600;
            }}
            .live-box {{
                margin-top: 1rem;
                background: rgba(255, 255, 255, 0.06);
                border-radius: 12px;
                padding: 1rem;
                font-size: 1.05rem;
                color: #F8FAFC;
                min-height: 60px;
                text-align: left;
                border: 1.5px solid rgba(255, 255, 255, 0.15);
                line-height: 1.6;
            }}
            .interim {{
                color: #FDE047;
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        <div class="dictation-card">
            <button id="recordBtn" class="mic-btn" onclick="toggleDictation()">
                <span id="micIcon">🎙️</span> <span id="btnText">Start Live Dictation ({language})</span>
            </button>
            <div id="statusText" class="status-text">Tap button to start live voice transcription</div>
            <div id="liveOutput" class="live-box"><em>Live speech text will stream here as you speak...</em></div>
        </div>

        <script>
            let recognition = null;
            let isRecording = false;
            let finalTranscript = '';
            const targetLocale = "{locale}";

            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = targetLocale;

                recognition.onstart = function() {{
                    isRecording = true;
                    finalTranscript = '';
                    document.getElementById('recordBtn').classList.add('recording');
                    document.getElementById('micIcon').innerText = '⏹';
                    document.getElementById('btnText').innerText = 'Stop & Use Live Speech';
                    document.getElementById('statusText').innerText = '🗣️ Live recording in progress... Speak into mic ({language})';
                }};

                recognition.onresult = function(event) {{
                    let interimTranscript = '';
                    for (let i = event.resultIndex; i < event.results.length; ++i) {{
                        if (event.results[i].isFinal) {{
                            finalTranscript += event.results[i][0].transcript + ' ';
                        }} else {{
                            interimTranscript += event.results[i][0].transcript;
                        }}
                    }}
                    const fullDisplay = finalTranscript + '<span class="interim">' + interimTranscript + '</span>';
                    document.getElementById('liveOutput').innerHTML = fullDisplay || '<em>Listening...</em>';

                    const currentFullText = (finalTranscript + ' ' + interimTranscript).trim();
                    if (currentFullText) {{
                        window.parent.postMessage({{
                            type: 'streamlit:setComponentValue',
                            value: currentFullText
                        }}, '*');
                    }}
                }};

                recognition.onerror = function(event) {{
                    document.getElementById('statusText').innerText = '⚠️ Mic Error: ' + event.error;
                    stopRecording();
                }};

                recognition.onend = function() {{
                    stopRecording();
                }};
            }} else {{
                document.getElementById('statusText').innerText = '⚠️ Web Speech API not supported in this browser. Please use Chrome or Edge.';
            }}

            function toggleDictation() {{
                if (!recognition) return;
                if (isRecording) {{
                    recognition.stop();
                }} else {{
                    try {{
                        recognition.lang = targetLocale;
                        recognition.start();
                    }} catch (e) {{
                        console.error(e);
                    }}
                }}
            }}

            function stopRecording() {{
                isRecording = false;
                document.getElementById('recordBtn').classList.remove('recording');
                document.getElementById('micIcon').innerText = '🎙️';
                document.getElementById('btnText').innerText = 'Start Live Dictation ({language})';
                document.getElementById('statusText').innerText = '✅ Recording stopped. Live speech captured!';
            }}
        </script>
    </body>
    </html>
    """

    val = st.components.v1.html(html_code, height=230)
    return val
