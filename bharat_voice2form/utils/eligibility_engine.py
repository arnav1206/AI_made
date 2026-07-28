"""
utils/eligibility_engine.py
============================
Formitra Eligibility Engine.
Evaluates user's extracted data against top Indian government scholarship schemes.
100% Multilingual translation support via t().
"""

from __future__ import annotations
from utils.translations import t


def evaluate_eligibility(extracted_data: dict) -> list[dict]:
    """
    Evaluate eligibility of extracted form data.

    Returns a list of scheme evaluation objects:
    {
       "title": str,
       "eligible": bool,
       "score": int (percentage match),
       "reason": str,
       "badge": str,
       "badge_color": str
    }
    """
    raw_income = extracted_data.get("Income", "0")
    try:
        income = float(str(raw_income).replace(",", "").replace("₹", ""))
    except ValueError:
        income = 150000.0

    state = extracted_data.get("State", "General")

    schemes = [
        {
            "id": "post_matric",
            "title": t("scheme_0_title", "Post-Matric Scholarship (SC/ST/OBC/EBC)"),
            "limit": 250000.0,
            "badge": t("badge_central_govt", "Central Government"),
            "badge_color": "#FF7A00",
            "desc": t("scheme_0_desc", "Full fee waiver and maintenance allowance for post-matric students."),
        },
        {
            "id": "central_sector",
            "title": t("scheme_1_title", "Central Sector Scheme for College/University Students"),
            "limit": 450000.0,
            "badge": t("badge_min_edu", "Ministry of Education"),
            "badge_color": "#2563EB",
            "desc": t("scheme_1_desc", "₹12,000 per annum for graduation studies based on academic performance."),
        },
        {
            "id": "pm_yasasvi",
            "title": t("scheme_pm_yasasvi_title", "PM-YASASVI Scholarship Scheme"),
            "limit": 250000.0,
            "badge": t("badge_pm_welfare", "PM Welfare Scheme"),
            "badge_color": "#059669",
            "desc": t("scheme_pm_yasasvi_desc", "Top class education scholarship for OBC, EBC and DNT students."),
        },
        {
            "id": "state_merit",
            "title": t("scheme_3_title", f"{state if state != '— Select —' else 'State'} Merit Scholarship Scheme"),
            "limit": 600000.0,
            "badge": t("badge_state_scholarship", "State Scholarship"),
            "badge_color": "#7C3AED",
            "desc": t("scheme_3_desc", "Merit-cum-means assistance for degree and diploma courses."),
        },
    ]

    results = []
    for s in schemes:
        if income <= s["limit"]:
            eligible = True
            score = 100 if income <= (s["limit"] * 0.6) else 85
            reason = f"{t('lbl_income', 'Annual family income')} ₹{int(income):,} <= ₹{int(s['limit']):,}."
        else:
            eligible = False
            score = 40
            reason = f"{t('lbl_income', 'Annual income')} ₹{int(income):,} > ₹{int(s['limit']):,}."

        results.append({
            "title": s["title"],
            "eligible": eligible,
            "score": score,
            "reason": reason,
            "badge": s["badge"],
            "badge_color": s["badge_color"],
            "desc": s["desc"],
        })

    return results
