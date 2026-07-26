"""
utils/pdf_generator.py
=======================
Placeholder module for application PDF generation.

Current status: MOCK — returns a dummy bytes object.

─── How to integrate a real PDF engine ──────────────────────────────

Option A — ReportLab (fully programmatic, recommended)
    1. pip install reportlab
    2. Implement _generate_reportlab() below
    3. Set ENGINE = "reportlab"

Option B — WeasyPrint (HTML → PDF, great for styled output)
    1. pip install weasyprint
    2. Implement _generate_weasyprint() below with Jinja2 template
    3. Set ENGINE = "weasyprint"

Option C — fpdf2 (lightweight pure-Python)
    1. pip install fpdf2
    2. Implement _generate_fpdf() below
    3. Set ENGINE = "fpdf2"

The public-facing function `generate()` is the only interface
that pages should call. Swapping the engine is transparent to callers.
──────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

# ─── Config ────────────────────────────────────────────────────────

# "mock" | "reportlab" | "weasyprint" | "fpdf2"
ENGINE: str = "mock"

# Path to the Jinja2 HTML template used by the weasyprint engine
HTML_TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "templates" / "application.html"


# ─── Public interface ──────────────────────────────────────────────

class PDFResult:
    """Structured return value from generate()."""

    def __init__(self, pdf_bytes: bytes, filename: str, engine: str):
        self.pdf_bytes = pdf_bytes   # Raw PDF bytes — use with st.download_button
        self.filename  = filename    # Suggested download filename
        self.engine    = engine
        self.error     = None        # Set to message on failure
        self.size_kb   = len(pdf_bytes) / 1024

    def __bool__(self) -> bool:
        return bool(self.pdf_bytes) and self.error is None

    def __repr__(self) -> str:
        return (
            f"PDFResult(engine={self.engine!r}, "
            f"filename={self.filename!r}, "
            f"size={self.size_kb:.1f}KB)"
        )


def generate(
    form_data: dict,
    application_no: str = "BVF-2026-DEMO",
    form_title: str = "Scholarship Application",
    *,
    engine: str | None = None,
) -> PDFResult:
    """
    Generate a PDF of the filled application form.

    Parameters
    ----------
    form_data : dict
        Field-name → value mapping (as saved by utils/session.save_form_data).
    application_no : str
        Reference number to print on the PDF.
    form_title : str
        Human-readable form type (printed in the header).
    engine : str | None
        Override the module-level ENGINE setting.

    Returns
    -------
    PDFResult
        Always returns an object; check `.error` for failure details.
        Pass `.pdf_bytes` to `st.download_button(data=...)`.
    """
    selected_engine = engine or ENGINE
    filename = _make_filename(application_no)

    try:
        if selected_engine == "mock":
            return _generate_mock(form_data, application_no, form_title, filename)
        elif selected_engine == "reportlab":
            return _generate_reportlab(form_data, application_no, form_title, filename)
        elif selected_engine == "weasyprint":
            return _generate_weasyprint(form_data, application_no, form_title, filename)
        elif selected_engine == "fpdf2":
            return _generate_fpdf(form_data, application_no, form_title, filename)
        else:
            raise ValueError(f"Unknown PDF engine: '{selected_engine}'")
    except Exception as exc:
        logger.exception("PDF generation failed")
        result = PDFResult(b"", filename, selected_engine)
        result.error = str(exc)
        return result


# ─── Engine implementations ────────────────────────────────────────

def _generate_mock(
    form_data: dict, application_no: str, form_title: str, filename: str
) -> PDFResult:
    """
    Return a minimal valid PDF as placeholder bytes.
    The stub content is plain-text wrapped in a bare PDF structure.
    """
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")
    lines = [
        f"BHARAT VOICE2FORM — {form_title.upper()}",
        f"Application No: {application_no}",
        f"Generated: {now}",
        "",
        "─" * 50,
        "",
    ]
    for field, value in form_data.items():
        lines.append(f"{field:<30}: {value or '—'}")

    lines += [
        "",
        "─" * 50,
        "NOTE: This is a prototype PDF placeholder.",
        "Integrate utils/pdf_generator.py with ReportLab or WeasyPrint",
        "to produce a properly styled application document.",
    ]

    body = "\n".join(lines).encode("utf-8")

    # Minimal valid PDF structure
    pdf = _wrap_text_as_pdf(body.decode("utf-8"))
    return PDFResult(pdf.encode("latin-1", errors="replace"), filename, "mock")


def _generate_reportlab(
    form_data: dict, application_no: str, form_title: str, filename: str
) -> PDFResult:
    """
    TODO: Generate a styled PDF with ReportLab.

    Implementation sketch:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
        from reportlab.lib.styles import getSampleStyleSheet
        from io import BytesIO

        buf    = BytesIO()
        doc    = SimpleDocTemplate(buf, pagesize=A4)
        styles = getSampleStyleSheet()
        story  = []

        # Header
        story.append(Paragraph(f"<b>Bharat Voice2Form</b>", styles["Title"]))
        story.append(Paragraph(form_title, styles["Heading2"]))
        story.append(Paragraph(f"Application No: {application_no}", styles["Normal"]))
        story.append(Spacer(1, 12))

        # Table of fields
        table_data = [["Field", "Value"]] + [
            [k, v or "—"] for k, v in form_data.items()
        ]
        table = Table(table_data, colWidths=[200, 280])
        story.append(table)

        doc.build(story)
        pdf_bytes = buf.getvalue()
        return PDFResult(pdf_bytes, filename, "reportlab")
    """
    raise NotImplementedError(
        "ReportLab engine not yet integrated. "
        "See utils/pdf_generator.py for integration instructions."
    )


def _generate_weasyprint(
    form_data: dict, application_no: str, form_title: str, filename: str
) -> PDFResult:
    """
    TODO: Generate a styled PDF from an HTML template using WeasyPrint.

    Implementation sketch:
        from weasyprint import HTML
        from jinja2 import Template

        template_src = HTML_TEMPLATE_PATH.read_text()
        html_str = Template(template_src).render(
            form_data=form_data,
            application_no=application_no,
            form_title=form_title,
            generated_at=datetime.now().strftime("%d %b %Y"),
        )
        pdf_bytes = HTML(string=html_str).write_pdf()
        return PDFResult(pdf_bytes, filename, "weasyprint")
    """
    raise NotImplementedError(
        "WeasyPrint engine not yet integrated. "
        "See utils/pdf_generator.py for integration instructions."
    )


def _generate_fpdf(
    form_data: dict, application_no: str, form_title: str, filename: str
) -> PDFResult:
    """
    TODO: Generate a PDF with fpdf2 (lightweight, pure Python).

    Implementation sketch:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Bharat Voice2Form", ln=True, align="C")
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, form_title, ln=True, align="C")
        pdf.ln(8)
        for field, value in form_data.items():
            pdf.cell(80, 7, field, border=1)
            pdf.cell(110, 7, value or "—", border=1, ln=True)
        return PDFResult(bytes(pdf.output()), filename, "fpdf2")
    """
    raise NotImplementedError(
        "fpdf2 engine not yet integrated. "
        "See utils/pdf_generator.py for integration instructions."
    )


# ─── Private helpers ───────────────────────────────────────────────

def _make_filename(application_no: str) -> str:
    date_str = datetime.now().strftime("%Y%m%d")
    safe_no  = application_no.replace("/", "-").replace(" ", "_")
    return f"BharatVoice2Form_{safe_no}_{date_str}.pdf"


def _wrap_text_as_pdf(text: str) -> str:
    """
    Create an ultra-minimal valid PDF containing plain text.
    This is only used by the mock engine for a plausible byte sequence.
    NOT suitable for production — use ReportLab/WeasyPrint instead.
    """
    lines   = text.split("\n")
    y       = 750
    ops     = []
    for line in lines:
        safe = line.replace("(", r"\(").replace(")", r"\)").replace("\\", r"\\")
        ops.append(f"BT /F1 10 Tf {50} {y} Td ({safe}) Tj ET")
        y -= 14
        if y < 50:
            break

    stream = "\n".join(ops)
    length = len(stream)

    return (
        "%PDF-1.4\n"
        "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        f"4 0 obj\n<< /Length {length} >>\nstream\n{stream}\nendstream\nendobj\n"
        "5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        "xref\n0 6\n0000000000 65535 f \n"
        "trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n9\n%%EOF"
    )
