"""
components/progress.py
=======================
Step-progress bar component for top of pages, plus form completion meter.
100% Multilingual translation support via t().
"""

from __future__ import annotations
import streamlit as st
from utils.translations import t


_STEPS = [
    "step_1",
    "step_2",
    "step_3",
    "step_4",
    "step_5",
    "step_6",
]


def step_progress_bar(current_step: int = 1) -> None:
    """
    Render horizontal 6-step progress bar.
    """
    steps_html = ""
    for i, step_key in enumerate(_STEPS, start=1):
        step_lbl = t(step_key)
        if i < current_step:
            cls   = "step-item step-done"
            badge = "✓"
        elif i == current_step:
            cls   = "step-item step-active"
            badge = str(i)
        else:
            cls   = "step-item step-todo"
            badge = str(i)

        steps_html += f"""
        <div class="{cls}">
            <div class="step-num">{badge}</div>
            <div class="step-label">{step_lbl}</div>
        </div>
        """

    st.markdown(
        f'<div class="progress-bar-container">{steps_html}</div>',
        unsafe_allow_html=True,
    )


def completion_meter(detected: int, total: int = 15, label: str = "") -> None:
    """
    Render a labelled progress-bar showing how many fields have been filled.
    """
    pct = int((detected / total) * 100) if total else 0
    meter_hdr = label or t("form_completion_hdr", "Form Completion")

    st.markdown(
        f'<div class="card" style="margin-top:0.5rem;">'
        f'<div style="font-weight:700;font-size:0.9rem;margin-bottom:0.75rem;">📊 {meter_hdr}</div>'
        f'<div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">'
        f'<span style="font-size:0.82rem;opacity:0.8;">'
        f'{detected} / {total} {t("fields_detected", "fields detected")}</span>'
        f'<span style="font-size:0.82rem;font-weight:700;color:#FF7A00;">{pct}%</span>'
        f'</div>'
        f'<div style="background:rgba(255,255,255,0.1);border-radius:6px;height:10px;">'
        f'<div style="width:{pct}%;'
        f'background:linear-gradient(90deg,#FF7A00,#2563EB);'
        f'border-radius:6px;height:10px;transition:width 0.5s ease;"></div>'
        f'</div>'
        f'<div style="font-size:0.78rem;opacity:0.7;margin-top:0.5rem;">'
        f'{t("fill_remaining_msg", "Fill remaining")} {total - detected} {t("fields_manually_msg", "field(s) manually to complete the form.")}'
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
