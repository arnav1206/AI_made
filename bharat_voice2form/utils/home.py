"""
views/home.py
=============
Home / landing page for Bharat Voice2Form.
"""

import streamlit as st
from typing import NamedTuple

from components.layout import tricolour_bar, hero_section, section_heading, spacer
from components.cards  import (
    stat_card, how_it_works_card, language_card, feature_card
)
from components.progress import step_progress_bar
from utils.translations import t
from utils.constants import LANGUAGES, HOME_FEATURES
import utils.session as session

class HowItWorksStep(NamedTuple):
    icon: str
    color: str
    title: str
    description: str

class Stat(NamedTuple):
    value: str
    label: str
    color: str

def _get_how_it_works_steps() -> list[HowItWorksStep]:
    return [
        HowItWorksStep("🎤", "#FF9933", t("step1_title"), t("step1_desc")),
        HowItWorksStep("🤖", "#002868", t("step2_title"), t("step2_desc")),
        HowItWorksStep("📄", "#138808", t("step3_title"), t("step3_desc")),
    ]

def _get_stats() -> list[Stat]:
    return [
        Stat(t("stat_value_languages"), t("stat_languages"), "#002868"),
        Stat(t("stat_value_form_types"), t("stat_form_types"), "#FF9933"),
        Stat(t("stat_value_powered_by"), t("stat_powered_by"), "#138808"),
        Stat(t("stat_value_privacy"), t("stat_privacy"), "#7C3AED"),
    ]


def render() -> None:
    tricolour_bar()

    hero_section(
        title_prefix=t("hero_prefix"),
        title_accent=t("hero_accent"),
        subtitle=t("hero_subtitle"),
    )

    # ── Stats ──────────────────────────────────────────────────────
    cols = st.columns(4)
    for col, stat in zip(cols, _get_stats()):
        with col:
            stat_card(stat.value, stat.label, stat.color)

    spacer(1.5)

    # ── How it works + Language list ───────────────────────────────
    left, right = st.columns([3, 2], gap="large")

    with left:
        section_heading(
            t("how_it_works"),
            t("how_it_works_sub"),
        )
        for step in _get_how_it_works_steps():
            how_it_works_card(step.icon, step.color, step.title, step.description)

    with right:
        section_heading(
            t("supported_langs"),
            t("supported_langs_sub"),
        )
        for flag, eng, native, _ in LANGUAGES:
            language_card(flag, eng, native)

    spacer(1.5)

    # ── CTA ────────────────────────────────────────────────────────
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown(
            f'<div style="text-align:center;margin-bottom:0.75rem;">'
            f'<div style="font-weight:700;font-size:1.1rem;color:#374151;">'
            f'{t("cta_text")}</div></div>',
            unsafe_allow_html=True,
        )
        if st.button(
            t("get_started"),
            use_container_width=True,
            type="primary",
        ):
            session.navigate("form_selection")

    spacer(1.5)

    # ── Feature cards ──────────────────────────────────────────────
    section_heading(
        t("why_title"),
        t("why_sub"),
    )
    cols = st.columns(3)
    for col, feature in zip(cols, HOME_FEATURES):
        with col:
            feature_card(feature[0], feature[1], feature[2], feature[3])
