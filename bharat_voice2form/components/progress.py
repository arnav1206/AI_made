"""
components/progress.py
=======================
Step-progress bar component for top of pages, plus form completion meter.
100% Multilingual translation support via t().
Inline CSS flexbox layout guarantees horizontal rendering across all themes & viewports.
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
    Render horizontal 6-step progress bar with explicit inline CSS flexbox layout.
    """
    is_dark = st.session_state.get("dark_mode", False)

    steps_html = ""
    for i, step_key in enumerate(_STEPS, start=1):
        step_lbl = t(step_key, f"{i}. Step")

        if i < current_step:
            bg_num   = "#10B981"
            txt_num  = "#FFFFFF"
            txt_lbl  = "#34D399" if is_dark else "#059669"
            badge    = "✓"
            border_c = "#10B981"
        elif i == current_step:
            bg_num   = "#FF7A00"
            txt_num  = "#FFFFFF"
            txt_lbl  = "#FDBA74" if is_dark else "#C2410C"
            badge    = str(i)
            border_c = "#FF7A00"
        else:
            bg_num   = "rgba(148, 163, 184, 0.25)" if is_dark else "#E2E8F0"
            txt_num  = "#94A3B8" if is_dark else "#64748B"
            txt_lbl  = "#64748B" if is_dark else "#64748B"
            badge    = str(i)
            border_c = "transparent"

        steps_html += (
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:0.35rem;flex:1;text-align:center;">'
            f'<div style="width:32px;height:32px;border-radius:50%;background:{bg_num};color:{txt_num};'
            f'display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.9rem;'
            f'border:2px solid {border_c};box-shadow:0 2px 6px rgba(0,0,0,0.12);">{badge}</div>'
            f'<div style="font-size:0.8rem;font-weight:700;color:{txt_lbl};white-space:nowrap;">{step_lbl}</div>'
            f'</div>'
        )

    container_bg     = "rgba(30, 41, 59, 0.7)" if is_dark else "#F8FAFC"
    container_border = "1px solid rgba(255, 122, 0, 0.3)" if is_dark else "1px solid #E2E8F0"

    full_html = (
        f'<div style="display:flex;justify-content:space-between;align-items:center;width:100%;'
        f'background:{container_bg};border:{container_border};border-radius:16px;'
        f'padding:0.85rem 1rem;margin-bottom:1.5rem;box-shadow:0 4px 12px rgba(0,0,0,0.05);">'
        f'{steps_html}'
        f'</div>'
    )

    st.markdown(full_html, unsafe_allow_html=True)


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
