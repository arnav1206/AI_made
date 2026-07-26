"""
components/progress.py
======================
Step-progress bar and completion-meter widgets used across pages.
"""

from __future__ import annotations

import streamlit as st
from utils.constants import STEP_LABELS


def step_progress_bar(current_step: int) -> None:
    """
    Render the horizontal step-progress bar.

    Parameters
    ----------
    current_step : int
        0-indexed index of the currently active step.
        Steps before current are marked done (✓, green).
        Current step is highlighted (blue, numbered).
        Future steps are grey and numbered.
    """
    items = []
    for i, label in enumerate(STEP_LABELS):
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

    Parameters
    ----------
    detected : int
        Number of fields that have been auto-filled.
    total : int
        Total number of fields in the form.
    label : str
        Header text above the bar.
    """
    pct = int((detected / total) * 100) if total else 0

    st.markdown(
        f'<div class="card" style="margin-top:0.5rem;">'
        f'<div style="font-weight:700;font-size:0.9rem;margin-bottom:0.75rem;">📊 {label}</div>'
        f'<div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">'
        f'<span style="font-size:0.82rem;color:#6B7280;">'
        f'{detected} / {total} fields detected</span>'
        f'<span style="font-size:0.82rem;font-weight:700;color:#002868;">{pct}%</span>'
        f'</div>'
        f'<div style="background:#E5E7EB;border-radius:6px;height:10px;">'
        f'<div style="width:{pct}%;'
        f'background:linear-gradient(90deg,#FF9933,#002868);'
        f'border-radius:6px;height:10px;transition:width 0.5s ease;"></div>'
        f'</div>'
        f'<div style="font-size:0.78rem;color:#6B7280;margin-top:0.5rem;">'
        f'Fill remaining {total - detected} field(s) manually to complete the form.'
        f'</div></div>',
        unsafe_allow_html=True,
    )


def confidence_bars(scores: dict[str, int]) -> None:
    """
    Render a list of labelled confidence-score bars.

    Parameters
    ----------
    scores : dict[str, int]
        Mapping of field name → confidence percentage (0–100).
    """
    for field, score in scores.items():
        color = (
            "#138808" if score >= 90
            else "#FF9933" if score >= 75
            else "#EF4444"
        )
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.4rem;">'
            f'<div style="width:80px;font-size:0.82rem;font-weight:600;color:#374151;">{field}</div>'
            f'<div style="flex:1;background:#E5E7EB;border-radius:4px;height:8px;">'
            f'<div style="width:{score}%;background:{color};border-radius:4px;height:8px;"></div>'
            f'</div>'
            f'<div style="width:36px;font-size:0.82rem;font-weight:700;color:{color};">{score}%</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
