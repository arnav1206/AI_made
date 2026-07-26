"""
utils/eligibility_engine.py
============================
Formitra Eligibility Engine.
Evaluates user's extracted data against top Indian government scholarship schemes.
"""

from __future__ import annotations


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
        income = float(raw_income.replace(",", "").replace("₹", ""))
    except ValueError:
        income = 150000.0

    state = extracted_data.get("State", "General")
    course = extracted_data.get("Course", "Degree")

    schemes = [
        {
            "id": "post_matric",
            "title": "Post-Matric Scholarship (SC/ST/OBC/EBC)",
            "limit": 250000.0,
            "badge": "Central Government",
            "badge_color": "#FF7A00",
            "desc": "Full fee waiver and maintenance allowance for post-matric students.",
        },
        {
            "id": "central_sector",
            "title": "Central Sector Scheme for College/University Students",
            "limit": 450000.0,
            "badge": "Ministry of Education",
            "badge_color": "#2563EB",
            "desc": "₹12,000 per annum for graduation studies based on academic performance.",
        },
        {
            "id": "pm_yasasvi",
            "title": "PM-YASASVI Scholarship Scheme",
            "limit": 250000.0,
            "badge": "PM Welfare Scheme",
            "badge_color": "#059669",
            "desc": "Top class education scholarship for OBC, EBC and DNT students.",
        },
        {
            "id": "state_merit",
            "title": f"{state if state != '— Select —' else 'State'} Merit Scholarship Scheme",
            "limit": 600000.0,
            "badge": "State Scholarship",
            "badge_color": "#7C3AED",
            "desc": "Merit-cum-means assistance for degree and diploma courses.",
        },
    ]

    results = []
    for s in schemes:
        if income <= s["limit"]:
            eligible = True
            score = 100 if income <= (s["limit"] * 0.6) else 85
            reason = f"Annual family income ₹{int(income):,} is below the ₹{int(s['limit']):,} threshold."
        else:
            eligible = False
            score = 40
            reason = f"Annual income ₹{int(income):,} exceeds the maximum limit of ₹{int(s['limit']):,}."

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
