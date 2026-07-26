"""
utils/lang_detector.py
=======================
Automatic language detection module for Formitra.
Detects language script from speech transcript or input text.
"""

from __future__ import annotations

import re


def detect_language(text: str) -> str:
    """
    Detect language name from text using Unicode script range matching.
    Default fallback: 'Hindi' if Devanagari, 'English' if Latin, etc.
    """
    if not text or not text.strip():
        return "Hindi"

    # Count character frequency per script
    counts: dict[str, int] = {
        "Odia":      len(re.findall(r"[\u0B00-\u0B7F]", text)),
        "Tamil":     len(re.findall(r"[\u0B80-\u0BFF]", text)),
        "Telugu":    len(re.findall(r"[\u0C00-\u0C7F]", text)),
        "Bengali":   len(re.findall(r"[\u0980-\u09FF]", text)),
        "Kannada":   len(re.findall(r"[\u0C80-\u0CFF]", text)),
        "Malayalam": len(re.findall(r"[\u0D00-\u0D7F]", text)),
        "Devanagari": len(re.findall(r"[\u0900-\u097F]", text)),
        "English":   len(re.findall(r"[a-zA-Z]", text)),
    }

    max_script = max(counts, key=counts.get)
    if counts[max_script] == 0:
        return "Hindi"

    if max_script == "Devanagari":
        # Check specific Marathi words
        if any(w in text.lower() for w in ["माझे", "नाव", "मी", "आहे", "राहतो"]):
            return "Marathi"
        return "Hindi"

    return max_script
