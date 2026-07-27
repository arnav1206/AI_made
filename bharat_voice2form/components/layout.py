"""
components/layout.py
====================
Reusable layout / structural HTML snippets used across all pages.
Dynamic Light/Dark mode contrast support for alerts and headings.
"""

from __future__ import annotations
import streamlit as st


# ─── Tricolour accent bar ──────────────────────────────────────────

def tricolour_bar() -> None:
    """Render the India-tricolour horizontal accent bar at the top of a page."""
    st.markdown(
        '<div class="tricolour-bar"></div>',
        unsafe_allow_html=True,
    )


def tricolour_divider_inline(height: int = 4) -> str:
    """Return an inline tricolour divider as an HTML string."""
    return (
        f'<div style="display:flex;height:{height}px;border-radius:2px;'
        f'overflow:hidden;margin-bottom:1.5rem;">'
        f'<div style="flex:1;background:#FF9933;"></div>'
        f'<div style="flex:1;background:rgba(255,255,255,0.5);"></div>'
        f'<div style="flex:1;background:#138808;"></div>'
        f'</div>'
    )


# ─── Hero / header ─────────────────────────────────────────────────

def hero_section(title_prefix: str, title_accent: str, subtitle: str) -> None:
    """Render the main hero banner with India-navy gradient background."""
    st.markdown(
        f'<div class="hero-section">'
        f'<div class="hero-title">{title_prefix}<span>{title_accent}</span></div>'
        f'<div class="hero-subtitle">{subtitle}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def section_heading(title: str, sub: str = "") -> None:
    """Render a section title with an optional subtitle line."""
    sub_html = f'<div class="section-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="section-heading">{title}</div>{sub_html}',
        unsafe_allow_html=True,
    )


# ─── Info / alert boxes ────────────────────────────────────────────

def info_box(message: str) -> None:
    """Render a blue informational callout box."""
    st.markdown(
        f'<div class="info-box">{message}</div>',
        unsafe_allow_html=True,
    )


def warning_inline(message: str) -> None:
    """Render a high-contrast amber warning note (for missing field hints)."""
    is_dark = st.session_state.get("dark_mode", False)
    color   = "#FBBF24" if is_dark else "#D97706"
    st.markdown(
        f'<div style="color:{color};font-size:0.8rem;font-weight:700;padding:0.2rem 0;margin-top:0.25rem;margin-bottom:0.4rem;display:block;">'
        f'⚠️ {message}</div>',
        unsafe_allow_html=True,
    )


def success_inline(message: str) -> None:
    """Render a small green success note."""
    is_dark = st.session_state.get("dark_mode", False)
    bg  = "rgba(5, 150, 105, 0.25)" if is_dark else "#D1FAE5"
    txt = "#34D399" if is_dark else "#065F46"
    st.markdown(
        f'<div style="background:{bg};color:{txt};border-radius:8px;'
        f'padding:0.5rem 0.9rem;font-size:0.85rem;font-weight:600;margin-top:0.3rem;">'
        f'{message}</div>',
        unsafe_allow_html=True,
    )


# ─── Generic card wrapper ──────────────────────────────────────────

def card_html(body: str, extra_style: str = "") -> str:
    """Return a card-styled div wrapping `body` HTML."""
    return f'<div class="card" style="{extra_style}">{body}</div>'


def form_card_open(icon: str, title: str) -> None:
    """Open a form-section card (must call form_card_close() after fields)."""
    st.markdown(
        f'<div class="form-card">'
        f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:1.25rem;">'
        f'<span style="font-size:1.3rem;">{icon}</span>'
        f'<span style="font-size:1rem;font-weight:700;">{title}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def form_card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


# ─── Spacer ────────────────────────────────────────────────────────

def spacer(rem: float = 1.0) -> None:
    """Inject a vertical blank space."""
    st.markdown(f'<div style="height:{rem}rem;"></div>', unsafe_allow_html=True)
