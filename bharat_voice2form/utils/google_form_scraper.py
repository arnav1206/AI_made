"""
utils/google_form_scraper.py
=============================
Scrapes and extracts dynamic fields, questions, types, and choice options
from Google Forms URLs (e.g. https://docs.google.com/forms/d/e/.../viewform)
and general HTML web forms.
"""

from __future__ import annotations

import json
import logging
import re
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

# Standard User-Agent to avoid bot blocking
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


class FormQuestion:
    def __init__(
        self,
        qid: str,
        title: str,
        qtype: str = "text",
        options: list[str] | None = None,
        required: bool = False,
    ):
        self.qid      = qid
        self.title    = title
        self.qtype    = qtype    # "text", "paragraph", "choice", "checkboxes", "dropdown", "date"
        self.options  = options or []
        self.required = required

    def to_dict(self) -> dict:
        return {
            "id":       self.qid,
            "title":    self.title,
            "type":     self.qtype,
            "options":  self.options,
            "required": self.required,
        }


def extract_google_form_questions(url: str) -> list[dict]:
    """
    Fetch and parse a Google Form or external web form URL, returning a list of question dicts.
    """
    clean_url = url.strip()
    if not clean_url.startswith(("http://", "https://")):
        clean_url = "https://" + clean_url

    # Ensure viewform URL for Google Forms
    if "docs.google.com/forms" in clean_url and not clean_url.endswith("/viewform"):
        if "/edit" in clean_url:
            clean_url = clean_url.split("/edit")[0] + "/viewform"
        elif not clean_url.endswith("/"):
            clean_url += "/viewform"

    try:
        req = urllib.request.Request(
            clean_url,
            headers={"User-Agent": _USER_AGENT}
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode("utf-8", errors="ignore")
    except Exception as exc:
        logger.warning("Failed to fetch form HTML from %s: %s", clean_url, exc)
        return _fallback_generic_questions(clean_url)

    # ── 1. Try parsing FB_PUBLIC_LOAD_DATA_ JavaScript Variable ────
    fb_match = re.search(r"var\s+FB_PUBLIC_LOAD_DATA_\s*=\s*(\[.*?\]);\s*</script>", html, re.DOTALL)
    if fb_match:
        try:
            raw_data = json.loads(fb_match.group(1))
            questions = _parse_fb_public_load_data(raw_data)
            if questions:
                logger.info("Successfully extracted %d questions from FB_PUBLIC_LOAD_DATA_", len(questions))
                return [q.to_dict() for q in questions]
        except Exception as exc:
            logger.warning("Failed to parse FB_PUBLIC_LOAD_DATA_ JSON: %s", exc)

    # ── 2. Try HTML Regex Scraping ─────────────────────────────────
    questions = _parse_html_regex(html)
    if questions:
        logger.info("Successfully extracted %d questions via HTML regex", len(questions))
        return [q.to_dict() for q in questions]

    # ── 3. Fallback to generic form schema ─────────────────────────
    return _fallback_generic_questions(clean_url)


def _parse_fb_public_load_data(raw_data: list) -> list[FormQuestion]:
    """Parse FB_PUBLIC_LOAD_DATA_ nested array structure."""
    questions: list[FormQuestion] = []
    
    try:
        # Items array is usually at index 1, 1
        items = raw_data[1][1]
        if not items or not isinstance(items, list):
            return []

        for idx, item in enumerate(items):
            if not isinstance(item, list) or len(item) < 2:
                continue

            q_title = item[1]
            if not q_title or not isinstance(q_title, str):
                continue

            q_title = q_title.strip()
            
            # Sub-array at item[4] contains field metadata & entry IDs
            sub_params = item[4] if len(item) > 4 and isinstance(item[4], list) and item[4] else []
            first_sub = sub_params[0] if sub_params and isinstance(sub_params[0], list) else []

            q_type_code = item[3] if len(item) > 3 else 0
            q_type = "text"
            options = []

            # Determine type & options
            # 0=short text, 1=paragraph, 2=radio/mcq, 3=dropdown, 4=checkboxes, 9=date
            if q_type_code == 1:
                q_type = "paragraph"
            elif q_type_code in (2, 3, 4):
                q_type = "choice" if q_type_code == 2 else ("dropdown" if q_type_code == 3 else "checkboxes")
                if len(first_sub) > 1 and isinstance(first_sub[1], list):
                    for opt in first_sub[1]:
                        if isinstance(opt, list) and opt and isinstance(opt[0], str):
                            options.append(opt[0].strip())
            elif q_type_code == 9:
                q_type = "date"

            is_req = bool(first_sub[2]) if len(first_sub) > 2 else False

            questions.append(
                FormQuestion(
                    qid=f"gform_q_{idx+1}",
                    title=q_title,
                    qtype=q_type,
                    options=options,
                    required=is_req
                )
            )
    except Exception as exc:
        logger.warning("Error traversing FB_PUBLIC_LOAD_DATA_: %s", exc)

    return questions


def _parse_html_regex(html: str) -> list[FormQuestion]:
    """Fallback HTML regex parser for Google Form elements."""
    questions: list[FormQuestion] = []
    
    # Match spans with class M7eMe or div with role="heading"
    titles = re.findall(r'<span[^>]*class="[^"]*M7eMe[^"]*"[^>]*>(.*?)</span>', html, re.DOTALL | re.IGNORECASE)
    if not titles:
        titles = re.findall(r'<div[^>]*role="heading"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)

    for idx, raw_t in enumerate(titles):
        clean_t = re.sub(r"<[^>]+>", "", raw_t).strip()
        if clean_t and len(clean_t) > 2:
            questions.append(
                FormQuestion(
                    qid=f"html_q_{idx+1}",
                    title=clean_t,
                    qtype="text",
                    options=[],
                    required="*" in raw_t
                )
            )

    return questions


def _fallback_generic_questions(url: str) -> list[dict]:
    """Default fallback schema if URL scraping is unreachable."""
    return [
        {"id": "fq_1", "title": "Full Name", "type": "text", "options": [], "required": True},
        {"id": "fq_2", "title": "City / District", "type": "text", "options": [], "required": True},
        {"id": "fq_3", "title": "State", "type": "text", "options": [], "required": True},
        {"id": "fq_4", "title": "Course Name", "type": "text", "options": [], "required": True},
        {"id": "fq_5", "title": "Current Year", "type": "choice", "options": ["First Year", "Second Year", "Third Year", "Fourth Year"], "required": True},
        {"id": "fq_6", "title": "Annual Family Income", "type": "text", "options": [], "required": True},
        {"id": "fq_7", "title": "Category", "type": "choice", "options": ["General", "OBC", "SC", "ST", "EWS"], "required": True},
        {"id": "fq_8", "title": "Gender", "type": "choice", "options": ["Male", "Female", "Transgender"], "required": True},
    ]
