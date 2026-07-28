"""
components/progress.py
======================
Step-progress bar and completion-meter widgets used across pages.
100% Multilingual translation support via t().
"""

from __future__ import annotations

import streamlit as st
from utils.translations import t

_STEP_KEYS = [
    "nav_form_selection",
    "nav_voice_input",
    "nav_ai_processing",
    "nav_auto_fill",
    "nav_preview",
    "nav_success",
]


def step_progress_bar(current_step: int) -> None:
    """
    Render the horizontal step-progress bar with 100% dynamic translation.
    """
    items = []
    for i, key in enumerate(_STEP_KEYS):
        label = t(key)
        if i < current_step:
            css_cls, num = "done",   "✓"
        elif i == current_step:
            css_cls, num = "active", str(i + 1)
        else:
            css_cls, num = "",       str(i + 1)

        items.append(
            f'<div class="step-item">'
            f'<div class="step-circle {css_cls}">{num}</div>'
            f'<div class="step-label">{label}</div>'
            f'</div>'
        )

    st.markdown(
        f'<div class="step-bar">{"".join(items)}</div>',
        unsafe_allow_html=True,
    )


def completion_meter(
    detected: int,
    total: int,
    label: str = "Form Completion",
) -> None:
    """
    Render a labelled progress-bar showing how many fields have been filled.
    """
    pct = int((detected / total) * 100) if total else 0

    st.markdown(
        f'<div class="card" style="margin-top:0.5rem;">'
        f'<div style="font-weight:700;font-size:0.9rem;margin-bottom:0.75rem;">📊 {label}</div>'
        f'<div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">'
        f'<span style="font-size:0.82rem;opacity:0.8;">'
        f'{detected} / {total} fields detected</span>'
        f'<span style="font-size:0.82rem;font-weight:700;color:#FF7A00;">{pct}%</span>'
        f'</div>'
        f'<div style="background:rgba(255,255,255,0.1);border-radius:6px;height:10px;">'
        f'<div style="width:{pct}%;'
        f'background:linear-gradient(90deg,#FF7A00,#2563EB);'
        f'border-radius:6px;height:10px;transition:width 0.5s ease;"></div>'
        f'</div>'
        f'<div style="font-size:0.78rem;opacity:0.7;margin-top:0.5rem;">'
        f'Fill remaining {total - detected} field(s) manually to complete the form.'
        f'</div></div>',
        unsafe_allow_html=True,
    )


def confidence_bars(scores: dict[str, int]) -> None:
    """
    Render a list of labelled confidence-score bars.
    """
    for field, score in scores.items():
        color = (
            "#10B981" if score >= 90
            else "#F59E0B" if score >= 75
            else "#EF4444"
        )
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.4rem;">'
            f'<div style="width:80px;font-size:0.82rem;font-weight:600;">{field}</div>'
            f'<div style="flex:1;background:rgba(255,255,255,0.1);border-radius:4px;height:8px;">'
            f'<div style="width:{score}%;background:{color};border-radius:4px;height:8px;"></div>'
            f'</div>'
            f'<div style="width:36px;font-size:0.82rem;font-weight:700;color:{color};">{score}%</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
