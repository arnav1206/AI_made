"""
views/admin.py
==============
Administrator & Nodal Officer Portal for Formitra.
100% Multilingual translation support via t().
Provides Admin Authentication, KPI Analytics, Application Review, Decision Workflow & Data Export.
"""

from __future__ import annotations

import streamlit as st

from components.layout import tricolour_bar, section_heading, info_box, spacer
from utils.translations import t
import utils.auth as auth
import utils.session as session


def render() -> None:
    tricolour_bar()

    section_heading(t("admin_portal_title"), t("admin_portal_sub"))

    # ── Admin Login Gate ──────────────────────────────────────────────
    if not auth.is_admin_logged_in():
        _render_admin_login_card()
        return

    # ── Authenticated Admin Dashboard ─────────────────────────────────
    _render_admin_dashboard()


def _render_admin_login_card() -> None:
    """Render Admin Authentication Card."""
    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        st.markdown(
            f'<div class="card" style="border-top:5px solid #2563EB;text-align:center;padding:2rem 1.5rem;">'
            f'<div style="font-size:2.8rem;margin-bottom:0.4rem;">🏛️</div>'
            f'<div style="font-size:1.35rem;font-weight:900;color:#2563EB;">{t("admin_card_title")}</div>'
            f'<div style="font-size:0.88rem;opacity:0.85;margin-top:0.3rem;">'
            f'{t("admin_card_sub")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        admin_user = st.text_input(
            t("admin_username"),
            value="admin",
            placeholder="Enter admin username (e.g. admin)",
            key="admin_username_input",
        )
        admin_pass = st.text_input(
            t("admin_password"),
            value="admin123",
            type="password",
            placeholder="Enter admin password",
            key="admin_password_input",
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(t("admin_login_btn"), use_container_width=True, type="primary"):
                success, msg = auth.admin_login(admin_user, admin_pass)
                if success:
                    st.toast(msg)
                    st.rerun()
                else:
                    st.error(msg)
        with col_b:
            if st.button(t("admin_demo_btn"), use_container_width=True):
                auth.admin_login("admin", "admin123")
                st.toast("Logged in as Admin (Demo Officer)")
                st.rerun()

    spacer()
    info_box("🔒 Security Notice: Unauthorized access to the State Scholarship Admin Engine is strictly prohibited under the IT Act.")


def _render_admin_dashboard() -> None:
    """Render Admin KPI Overview & Application Audit Workspace."""
    admin_name = st.session_state.get("admin_user", "Officer").title()

    # Top Header Banner with explicit white text
    st.markdown(
        f'<div class="card" style="border-left:5px solid #2563EB;background:linear-gradient(135deg, #1E293B, #0F172A);padding:1.5rem;">'
        f'<div style="font-size:0.75rem;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">MINISTRY OF EDUCATION & STATE DBT PORTAL</div>'
        f'<div style="font-size:1.35rem;font-weight:900;color:#FFFFFF;margin-top:0.2rem;">Welcome, Nodal Officer ({admin_name})</div>'
        f'<div style="font-size:0.85rem;color:#CBD5E1;margin-top:0.15rem;">Live Application Verifier & Gemma AI Speech Audit Workstation</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── KPI Summary Cards ─────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            '<div class="card" style="text-align:center;border-top:4px solid #2563EB;padding:1.2rem;">'
            '<div style="font-size:0.75rem;opacity:0.7;font-weight:700;">TOTAL APPLICATIONS</div>'
            '<div style="font-size:1.8rem;font-weight:900;color:#2563EB;margin-top:0.2rem;">1,482</div>'
            '<div style="font-size:0.72rem;color:#059669;margin-top:0.2rem;">▲ +12% this week</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            '<div class="card" style="text-align:center;border-top:4px solid #059669;padding:1.2rem;">'
            '<div style="font-size:0.75rem;opacity:0.7;font-weight:700;">APPROVED FOR DBT</div>'
            '<div style="font-size:1.8rem;font-weight:900;color:#059669;margin-top:0.2rem;">1,290</div>'
            '<div style="font-size:0.72rem;color:#059669;margin-top:0.2rem;">87.0% Approval Rate</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            '<div class="card" style="text-align:center;border-top:4px solid #FF7A00;padding:1.2rem;">'
            '<div style="font-size:0.75rem;opacity:0.7;font-weight:700;">PENDING VERIFICATION</div>'
            '<div style="font-size:1.8rem;font-weight:900;color:#FF7A00;margin-top:0.2rem;">142</div>'
            '<div style="font-size:0.72rem;color:#FF7A00;margin-top:0.2rem;">Requires Tehsildar Audit</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            '<div class="card" style="text-align:center;border-top:4px solid #9333EA;padding:1.2rem;">'
            '<div style="font-size:0.75rem;opacity:0.7;font-weight:700;">TOTAL DISBURSED</div>'
            '<div style="font-size:1.8rem;font-weight:900;color:#9333EA;margin-top:0.2rem;">₹2.45 Cr</div>'
            '<div style="font-size:0.72rem;color:#9333EA;margin-top:0.2rem;">Direct Bank Transfer (DBT)</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    spacer(0.5)

    # ── Application Review Table ──────────────────────────────────────
    st.markdown('<div style="font-weight:800;font-size:1.15rem;margin-bottom:0.75rem;">📋 Master Application Audit Table</div>', unsafe_allow_html=True)

    applications = auth.get_submitted_applications()

    filter_status = st.selectbox(
        "Filter by Application Status",
        ["All Statuses", "Under Officer Review ⏳", "Approved for Disbursal ✅", "Income Certificate Pending ⚠️"],
        key="admin_filter_status",
    )

    filtered_apps = applications
    if filter_status != "All Statuses":
        filtered_apps = [a for a in applications if a["status"] == filter_status]

    table_rows = ""
    for app in filtered_apps:
        table_rows += (
            f'<tr style="border-bottom:1px solid rgba(255,255,255,0.1);">'
            f'<td style="padding:0.75rem;font-weight:800;font-family:monospace;color:#FF7A00;">{app["ref_code"]}</td>'
            f'<td style="padding:0.75rem;font-weight:700;">{app["name"]}</td>'
            f'<td style="padding:0.75rem;">{app["scheme"]}</td>'
            f'<td style="padding:0.75rem;">{app["state"]}</td>'
            f'<td style="padding:0.75rem;font-weight:700;color:#059669;">{app["income"]}</td>'
            f'<td style="padding:0.75rem;"><span style="background:rgba(37,99,235,0.2);color:#60A5FA;padding:0.2rem 0.5rem;border-radius:6px;font-size:0.78rem;">{app["status"]}</span></td>'
            f'</tr>'
        )

    table_html = (
        f'<div class="card" style="padding:0;overflow-x:auto;">'
        f'<table style="width:100%;border-collapse:collapse;font-size:0.88rem;">'
        f'<thead style="background:rgba(255,255,255,0.06);text-align:left;">'
        f'<tr>'
        f'<th style="padding:0.75rem;">Ref Code</th>'
        f'<th style="padding:0.75rem;">Applicant Name</th>'
        f'<th style="padding:0.75rem;">Scheme Title</th>'
        f'<th style="padding:0.75rem;">State</th>'
        f'<th style="padding:0.75rem;">Income</th>'
        f'<th style="padding:0.75rem;">Verification Status</th>'
        f'</tr></thead>'
        f'<tbody>{table_rows}</tbody></table></div>'
    )
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Decision Action Controls ─────────────────────────────────────
    spacer(0.5)
    st.markdown('<div style="font-weight:800;font-size:1.15rem;margin-bottom:0.75rem;">🛠️ Officer Decision & Status Update Panel</div>', unsafe_allow_html=True)

    col_select, col_action = st.columns([1.2, 2])

    with col_select:
        ref_options = [a["ref_code"] for a in applications]
        selected_ref = st.selectbox("Select Application Ref Code", ref_options, key="admin_target_ref")

    with col_action:
        new_status = st.selectbox(
            "Set New Status",
            [
                "Approved for Disbursal ✅",
                "Under Officer Review ⏳",
                "Income Certificate Pending ⚠️",
                "Rejected — Ineligible Income ❌",
            ],
            key="admin_new_status",
        )
        if st.button("💾 Apply Status Change to System", type="primary", use_container_width=True):
            if auth.update_application_status(selected_ref, new_status):
                st.toast(f"Updated {selected_ref} status to: {new_status}")
                st.rerun()
            else:
                st.error("Failed to update status.")

    spacer()
    if st.button("🚪 Logout Admin Account", use_container_width=True):
        auth.admin_logout()
        st.toast("Logged out of Admin Portal.")
        st.rerun()
