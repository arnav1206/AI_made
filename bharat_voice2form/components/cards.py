"""
components/cards.py
===================
Reusable card-style HTML widgets used across Home, Form Selection,
AI Processing, and Success pages.
"""

from __future__ import annotations

import streamlit as st


# ─── Stat card (Home page) ─────────────────────────────────────────

def stat_card(value: str, label: str, color: str) -> None:
    """Render a single KPI/stat card."""
    st.markdown(
        f'<div style="background:white;border-radius:12px;padding:1.2rem;'
        f'text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.06);'
        f'border:1px solid #E5E7EB;">'
        f'<div style="font-size:1.9rem;font-weight:800;color:{color};">{value}</div>'
        f'<div style="font-size:0.78rem;color:#6B7280;font-weight:500;">{label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─── How-it-works step card ────────────────────────────────────────

def how_it_works_card(icon: str, color: str, title: str, desc: str) -> None:
    """Render a single step in the 'How It Works' list."""
    st.markdown(
        f'<div class="card" style="display:flex;align-items:flex-start;gap:1rem;">'
        f'<div style="font-size:2rem;background:{color}22;border-radius:10px;'
        f'padding:0.5rem 0.65rem;flex-shrink:0;">{icon}</div>'
        f'<div>'
        f'<div style="font-weight:700;font-size:0.97rem;">{title}</div>'
        f'<div style="font-size:0.86rem;opacity:0.8;margin-top:0.2rem;">{desc}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )


def step_card(step_num: int, title: str, desc: str, icon: str) -> None:
    """Step card alias for home page."""
    how_it_works_card(icon=icon, color="#FF7A00", title=f"{step_num}. {title}", desc=desc)


def feature_badge(label: str, icon: str = "✨") -> None:
    """Feature badge badge renderer."""
    st.markdown(
        f'<span style="background:rgba(255,122,0,0.15);color:#FF7A00;padding:0.3rem 0.75rem;'
        f'border-radius:50px;font-size:0.8rem;font-weight:700;">{icon} {label}</span>',
        unsafe_allow_html=True,
    )


# ─── Language list card ────────────────────────────────────────────

def language_card(flag: str, english_name: str, native_name: str) -> None:
    """Render one language row on the Home page."""
    st.markdown(
        f'<div class="card" style="padding:0.9rem 1.1rem;display:flex;'
        f'align-items:center;justify-content:space-between;">'
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<span style="font-size:1.4rem;">{flag}</span>'
        f'<span style="font-weight:600;font-size:0.93rem;">{english_name}</span>'
        f'</div>'
        f'<span style="color:#6B7280;font-size:0.88rem;">{native_name}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─── Feature card ──────────────────────────────────────────────────

def feature_card(icon: str, color: str, title: str, desc: str) -> None:
    """Render a centred feature/benefit card (Home page bottom row)."""
    st.markdown(
        f'<div class="card" style="text-align:center;padding:2rem 1.5rem;">'
        f'<div style="font-size:2.5rem;background:{color}18;border-radius:14px;'
        f'padding:0.7rem;display:inline-block;margin-bottom:0.75rem;">{icon}</div>'
        f'<div style="font-weight:700;font-size:1rem;margin-bottom:0.4rem;">{title}</div>'
        f'<div style="font-size:0.85rem;opacity:0.8;">{desc}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─── Form-type selection card ──────────────────────────────────────

def form_type_card(icon: str, title: str, desc: str, badge: str, available: bool) -> None:
    """Render a form-type card with availability badge."""
    badge_cls = "form-badge" if available else "form-badge-coming"
    active_cls = "active" if available else ""
    st.markdown(
        f'<div class="form-selection-card {active_cls}">'
        f'<div class="form-icon">{icon}</div>'
        f'<div class="form-title">{title}</div>'
        f'<div style="font-size:0.8rem;opacity:0.8;margin:0.35rem 0 0.5rem;">{desc}</div>'
        f'<div class="{badge_cls}">{badge}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─── Suggestion card ───────────────────────────────────────────────

def suggestion_card(icon: str, title: str, body: str, color: str = "#6366F1") -> None:
    """Render one AI suggestion card in the suggestions panel."""
    st.markdown(
        f'<div class="suggestion-card" style="--color:{color}">'
        f'<div class="suggestion-icon">{icon}</div>'
        f'<div>'
        f'<div class="suggestion-title">{title}</div>'
        f'<div class="suggestion-body">{body}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─── JSON extraction display ───────────────────────────────────────

def json_block(data: dict) -> None:
    """Render a syntax-highlighted JSON object block."""
    items = list(data.items())
    lines = ['<div class="json-block">',
             '<span class="json-brace">{</span><br>']
    for i, (k, v) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines.append(
            f'&nbsp;&nbsp;<span class="json-key">"{k}"</span>: '
            f'<span class="json-val">"{v}"</span>{comma}<br>'
        )
    lines += ['<span class="json-brace">}</span>', "</div>"]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


# ─── Field-mapping row ─────────────────────────────────────────────

def field_mapping_row(label: str, value: str, found: bool) -> None:
    """Render one row in the AI field-mapping preview."""
    bg = "#ECFDF5" if found else "#FEF9C3"
    ic = "✅" if found else "⚠️"
    st.markdown(
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'background:{bg};border-radius:8px;padding:0.55rem 0.85rem;margin-bottom:0.35rem;">'
        f'<div style="font-size:0.85rem;font-weight:600;color:#111827;">{ic} {label}</div>'
        f'<div style="font-size:0.83rem;color:#374151;">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─── AI loader ─────────────────────────────────────────────────────

def ai_loader(step_icon: str, step_message: str) -> str:
    """
    Return the HTML string for the AI processing loader card.
    Used inside a `st.empty()` placeholder that gets overwritten each step.
    """
    return (
        f'<div class="ai-loader">'
        f'<div class="ai-spinner">⚙️</div>'
        f'<div style="font-size:1.1rem;font-weight:700;color:#4C1D95;margin-bottom:0.4rem;">'
        f'Gemma is understanding your speech…</div>'
        f'<div style="font-size:0.9rem;color:#6D28D9;">{step_icon} {step_message}</div>'
        f'</div>'
    )


# ─── Preview table ─────────────────────────────────────────────────

def preview_table(section_title: str, fields: list[str], form_data: dict) -> None:
    rows = ""
    for field in fields:
        val = form_data.get(field, "")
        if val and val not in ("— Select —",):
            if field == "Annual Family Income" and val.isdigit():
                val = f"₹ {int(val):,}"
            tag  = '<span class="tag-filled">✓ Filled</span>'
        else:
            tag  = '<span class="tag-empty">⚠ Missing</span>'
            val  = "—"

        rows += (
            f"<tr>"
            f"<td>{field}</td>"
            f"<td>{val}</td>"
            f"<td>{tag}</td>"
            f"</tr>"
        )

    st.markdown(
        f'<div class="form-card">'
        f'<div style="font-weight:700;font-size:1rem;margin-bottom:1rem;">{section_title}</div>'
        f'<table class="preview-table">'
        f'<thead><tr><th>Field</th><th>Value</th><th>Status</th></tr></thead>'
        f'<tbody>{rows}</tbody>'
        f'</table></div>',
        unsafe_allow_html=True,
    )


# ─── Next-step card (Success page) ────────────────────────────────

def next_step_card(number: str, color: str, title: str, desc: str) -> None:
    """Render one numbered next-step card on the Success page."""
    st.markdown(
        f'<div class="card" style="display:flex;gap:1rem;align-items:flex-start;">'
        f'<div style="min-width:36px;height:36px;border-radius:50%;'
        f'background:{color};color:white;display:flex;align-items:center;'
        f'justify-content:center;font-weight:800;font-size:1rem;flex-shrink:0;">{number}</div>'
        f'<div>'
        f'<div style="font-weight:700;font-size:0.95rem;">{title}</div>'
        f'<div style="font-size:0.85rem;opacity:0.8;margin-top:0.2rem;">{desc}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )
