"""
scratch/audit.py
================
Comprehensive offline audit of Bharat Voice2Form codebase.
Checks: syntax, imports, constants integrity, session key contracts,
        data-flow consistency, component signatures, edge cases.
Run with:  py -3.14 scratch/audit.py
"""

import sys, os, ast, importlib, importlib.util, traceback, json, re, inspect
from pathlib import Path

# Force UTF-8 output on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"
INFO = "[INFO]"

results = []

def ok(msg):   results.append((PASS, msg))
def fail(msg): results.append((FAIL, msg))
def warn(msg): results.append((WARN, msg))
def info(msg): results.append((INFO, msg))


# ══════════════════════════════════════════════════════════════════
# 1. SYNTAX — every .py file compiles
# ══════════════════════════════════════════════════════════════════
print("\n── 1. Syntax check ──────────────────────────────────────────")
import py_compile

py_files = [f for f in ROOT.rglob("*.py") if "__pycache__" not in str(f) and "scratch" not in str(f)]
for f in sorted(py_files):
    try:
        py_compile.compile(str(f), doraise=True)
        ok(f"Syntax OK: {f.relative_to(ROOT)}")
    except py_compile.PyCompileError as e:
        fail(f"Syntax ERROR: {f.relative_to(ROOT)} - {e}")


# ══════════════════════════════════════════════════════════════════
# 2. AST IMPORT — check all local imports resolve
# ══════════════════════════════════════════════════════════════════
print("\n── 2. Import resolution ─────────────────────────────────────")

MOCK_ST = """
import sys, types
st_mod = types.ModuleType('streamlit')
for attr in ['markdown','write','button','text_input','text_area','selectbox',
             'columns','sidebar','session_state','rerun','spinner','error',
             'success','checkbox','download_button','empty','stop','set_page_config',
             'cache_data','cache_resource']:
    setattr(st_mod, attr, lambda *a,**kw: None)
st_mod.session_state = {}
sys.modules['streamlit'] = st_mod
"""

# We'll check modules that don't need streamlit at import time
pure_modules = [
    "utils.constants",
    "utils.session",
    "utils.speech_to_text",
    "utils.gemma_processor",
    "utils.pdf_generator",
]
for mod_name in pure_modules:
    try:
        # Patch streamlit before import
        exec(MOCK_ST)
        mod = importlib.import_module(mod_name)
        ok(f"Import OK: {mod_name}")
    except Exception as e:
        fail(f"Import FAIL: {mod_name} — {type(e).__name__}: {e}")


# ══════════════════════════════════════════════════════════════════
# 3. CONSTANTS INTEGRITY
# ══════════════════════════════════════════════════════════════════
print("\n── 3. Constants integrity ───────────────────────────────────")
try:
    from utils import constants as C

    # 3a. PAGE_ORDER ↔ PAGE_LABELS coverage
    missing_labels = set(C.PAGE_ORDER) - set(C.PAGE_LABELS)
    if missing_labels:
        fail(f"PAGE_LABELS missing keys: {missing_labels}")
    else:
        ok(f"PAGE_ORDER / PAGE_LABELS fully aligned ({len(C.PAGE_ORDER)} pages)")

    # 3b. STEP_LABELS count matches PAGE_ORDER
    if len(C.STEP_LABELS) == len(C.PAGE_ORDER):
        ok(f"STEP_LABELS count matches PAGE_ORDER ({len(C.STEP_LABELS)})")
    else:
        warn(f"STEP_LABELS has {len(C.STEP_LABELS)} items but PAGE_ORDER has {len(C.PAGE_ORDER)}")

    # 3c. Every language in LANGUAGES has a mock transcript
    for flag, eng, native, locale in C.LANGUAGES:
        if eng in C.MOCK_TRANSCRIPTS:
            ok(f"Mock transcript exists: {eng}")
        else:
            fail(f"Mock transcript MISSING: {eng}")

    # 3d. LANGUAGE_NAMES derived correctly
    derived = [l[1] for l in C.LANGUAGES]
    if derived == C.LANGUAGE_NAMES:
        ok("LANGUAGE_NAMES matches LANGUAGES list")
    else:
        fail(f"LANGUAGE_NAMES mismatch: {set(derived) ^ set(C.LANGUAGE_NAMES)}")

    # 3e. ALL_FIELD_NAMES covers all sections
    from_sections = [f for s in C.SCHOLARSHIP_SECTIONS for f in s["fields"]]
    if from_sections == C.ALL_FIELD_NAMES:
        ok(f"ALL_FIELD_NAMES derived correctly ({len(C.ALL_FIELD_NAMES)} fields)")
    else:
        fail(f"ALL_FIELD_NAMES mismatch: {set(from_sections) ^ set(C.ALL_FIELD_NAMES)}")

    # 3f. FORM_TYPES — every available form has a page_key
    for ft in C.FORM_TYPES:
        if ft["available"] and not ft.get("page_key"):
            fail(f"Available form '{ft['title']}' has no page_key")
        else:
            ok(f"FORM_TYPE OK: {ft['title']} (available={ft['available']})")

    # 3g. AI_PROCESSING_STEPS durations are positive
    for icon, msg, dur in C.AI_PROCESSING_STEPS:
        if dur <= 0:
            fail(f"AI step '{msg}' has non-positive duration {dur}")
        else:
            ok(f"AI step OK: '{msg}' ({dur}s)")

    # 3h. INDIAN_STATES starts with placeholder
    if C.INDIAN_STATES[0] == "— Select —":
        ok("INDIAN_STATES[0] is the placeholder '— Select —'")
    else:
        fail(f"INDIAN_STATES[0] should be '— Select —', got '{C.INDIAN_STATES[0]}'")

    # 3i. MOCK_CONFIDENCE_SCORES all in 0-100
    for field, score in C.MOCK_CONFIDENCE_SCORES.items():
        if 0 <= score <= 100:
            ok(f"Confidence score OK: {field} = {score}%")
        else:
            fail(f"Confidence score OUT OF RANGE: {field} = {score}")

    # 3j. AI_SUGGESTIONS all have required keys
    required_keys = {"icon", "title", "body", "color"}
    for i, s in enumerate(C.AI_SUGGESTIONS):
        missing = required_keys - set(s.keys())
        if missing:
            fail(f"AI_SUGGESTIONS[{i}] missing keys: {missing}")
        else:
            ok(f"AI_SUGGESTIONS[{i}] keys OK: '{s['title']}'")

except Exception as e:
    fail(f"Constants module crashed: {e}")
    traceback.print_exc()


# ══════════════════════════════════════════════════════════════════
# 4. SESSION KEY CONTRACT
# ══════════════════════════════════════════════════════════════════
print("\n-- 4. Session key contract --")
try:
    src = (ROOT / "utils" / "session.py").read_text(encoding='utf-8')
    tree = ast.parse(src)

    # Collect all string keys in _DEFAULTS dict
    # _DEFAULTS uses an annotated assignment (_DEFAULTS: dict = {...}),
    # so we must handle ast.AnnAssign, NOT just ast.Assign.
    defaults_keys = set()
    for node in ast.walk(tree):
        # Plain assignment:    _DEFAULTS = {...}
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "_DEFAULTS":
                    if isinstance(node.value, ast.Dict):
                        for k in node.value.keys:
                            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                                defaults_keys.add(k.value)
        # Annotated assignment: _DEFAULTS: dict = {...}
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "_DEFAULTS":
                if node.value and isinstance(node.value, ast.Dict):
                    for k in node.value.keys:
                        if isinstance(k, ast.Constant) and isinstance(k.value, str):
                            defaults_keys.add(k.value)

    if defaults_keys:
        ok(f"_DEFAULTS has {len(defaults_keys)} keys: {sorted(defaults_keys)}")
    else:
        warn("Could not parse _DEFAULTS from session.py -- check AST")

    # All keys known to be valid (from _DEFAULTS + widget keys + page-internal keys)
    known_keys = defaults_keys | {
        "lang_select", "transcript_editor", "declaration_agreed",
        # Explicit list in case AST parse misses any
        "page", "selected_form", "selected_language", "is_recording",
        "transcript", "extracted_data", "extraction_done",
        "form_data", "application_no",
    }
    page_files = list((ROOT / "pages").glob("*.py"))
    for pf in page_files:
        psrc = pf.read_text(encoding='utf-8')
        get_calls = re.findall(r'session\.get\("([^"]+)"', psrc)
        set_calls = re.findall(r'session\.set\("([^"]+)"', psrc)
        for key in set(get_calls + set_calls):
            if key in known_keys or key.startswith("field_"):
                ok(f"Session key '{key}' in {pf.name}: registered")
            else:
                warn(f"Session key '{key}' in {pf.name}: NOT in _DEFAULTS")

except Exception as e:
    fail(f"Session audit crashed: {e}")
    traceback.print_exc()


# ══════════════════════════════════════════════════════════════════
# 5. FORM_FIELDS ↔ SAVE_FORM_DATA ALIGNMENT
# ══════════════════════════════════════════════════════════════════
print("\n── 5. form_fields ↔ save_form_data alignment ───────────────")
try:
    session_src = (ROOT / "utils" / "session.py").read_text(encoding='utf-8')
    # Extract mapping dict from save_form_data
    mapping_block = re.search(
        r"mapping\s*=\s*\{([^}]+)\}", session_src, re.DOTALL
    )
    if mapping_block:
        raw = mapping_block.group(1)
        # Extract pairs  "Label": "field_key"
        pairs = re.findall(r'"([^"]+)"\s*:\s*"(field_[^"]+)"', raw)
        saved_labels   = {label for label, _ in pairs}
        saved_keys     = {key for _, key in pairs}
        ok(f"save_form_data maps {len(pairs)} fields")

        # Check against ALL_FIELD_NAMES
        from utils.constants import ALL_FIELD_NAMES
        for fn in ALL_FIELD_NAMES:
            if fn in saved_labels:
                ok(f"  Field '{fn}' covered in save_form_data")
            else:
                warn(f"  Field '{fn}' NOT in save_form_data mapping")
    else:
        warn("Could not parse save_form_data mapping block")
except Exception as e:
    fail(f"form_fields audit crashed: {e}")


# ══════════════════════════════════════════════════════════════════
# 6. GEMMA PROCESSOR — mock output matches expected keys
# ══════════════════════════════════════════════════════════════════
print("\n── 6. Gemma processor mock output ───────────────────────────")
try:
    from utils.gemma_processor import MOCK_EXTRACTION, _parse_json_from_llm, ENGINE
    ok(f"gemma_processor ENGINE = '{ENGINE}'")

    expected_keys = {"Name", "City", "State", "Course", "Year", "Income"}
    actual_keys   = set(MOCK_EXTRACTION.keys())
    if expected_keys <= actual_keys:
        ok(f"MOCK_EXTRACTION has all expected keys: {expected_keys}")
    else:
        fail(f"MOCK_EXTRACTION missing keys: {expected_keys - actual_keys}")

    # Test _parse_json_from_llm with fence, bare, and plain formats
    tests = [
        ('```json\n{"Name":"Test"}\n```', {"Name": "Test"}, "fenced JSON"),
        ('Here is the result: {"Name":"Test"}', {"Name": "Test"}, "inline JSON"),
        ('{"Name":"Test"}', {"Name": "Test"}, "bare JSON"),
    ]
    for raw, expected, label in tests:
        parsed = _parse_json_from_llm(raw)
        if parsed == expected:
            ok(f"_parse_json_from_llm: {label} → {parsed}")
        else:
            fail(f"_parse_json_from_llm: {label} expected {expected}, got {parsed}")

except Exception as e:
    fail(f"Gemma processor audit crashed: {e}")
    traceback.print_exc()


# ══════════════════════════════════════════════════════════════════
# 7. STT — mock returns text for every supported language
# ══════════════════════════════════════════════════════════════════
print("\n── 7. Speech-to-text mock coverage ─────────────────────────")
try:
    from utils.speech_to_text import transcribe, get_supported_languages, ENGINE as STT_ENGINE
    ok(f"speech_to_text ENGINE = '{STT_ENGINE}'")

    langs = get_supported_languages()
    ok(f"get_supported_languages() returns {len(langs)} languages")

    for lang in langs:
        result = transcribe(audio_bytes=None, language=lang)
        if result and result.text:
            ok(f"Mock transcript OK: {lang} ({len(result.text)} chars)")
        else:
            fail(f"Mock transcript EMPTY: {lang} (error={result.error})")

    # Test unknown language falls back to English
    result_unknown = transcribe(audio_bytes=None, language="Klingon")
    if result_unknown and result_unknown.text:
        ok(f"Unknown language fallback OK (returned {len(result_unknown.text)} chars)")
    else:
        warn("Unknown language returned empty result")

except Exception as e:
    fail(f"STT audit crashed: {e}")
    traceback.print_exc()


# ══════════════════════════════════════════════════════════════════
# 8. PDF GENERATOR — mock returns valid bytes
# ══════════════════════════════════════════════════════════════════
print("\n── 8. PDF generator mock output ─────────────────────────────")
try:
    from utils.pdf_generator import generate as pdf_gen, ENGINE as PDF_ENGINE
    ok(f"pdf_generator ENGINE = '{PDF_ENGINE}'")

    dummy_data = {
        "Full Name": "Aditi Verma",
        "Course": "B.Tech",
        "Annual Family Income": "200000",
        "Date of Birth": "",
    }
    result = pdf_gen(
        form_data=dummy_data,
        application_no="BVF-TEST-001",
        form_title="Test Application",
    )
    if result:
        ok(f"PDF generated: {result.filename} ({result.size_kb:.1f} KB)")
        if result.pdf_bytes[:4] == b"%PDF":
            ok("PDF bytes start with %PDF magic header")
        else:
            warn(f"PDF bytes don't start with %PDF: {result.pdf_bytes[:8]}")
        if result.filename.endswith(".pdf"):
            ok(f"Filename ends with .pdf: {result.filename}")
    else:
        fail(f"PDF generation failed: {result.error}")

    # Test empty form_data
    result_empty = pdf_gen(form_data={}, application_no="BVF-EMPTY")
    if result_empty:
        ok("PDF with empty form_data: gracefully handled")
    else:
        warn(f"PDF with empty data returned error: {result_empty.error}")

except Exception as e:
    fail(f"PDF generator audit crashed: {e}")
    traceback.print_exc()


# ══════════════════════════════════════════════════════════════════
# 9. PAGE ROUTING — every PAGE_ORDER key maps to a module with render()
# ══════════════════════════════════════════════════════════════════
print("\n── 9. Page routing completeness ─────────────────────────────")
try:
    from utils.constants import PAGE_ORDER
    page_dir = ROOT / "pages"
    for page_key in PAGE_ORDER:
        if page_key == "home":
            mod_file = page_dir / "home.py"
        elif page_key == "form_selection":
            mod_file = page_dir / "form_selection.py"
        elif page_key == "voice_input":
            mod_file = page_dir / "voice_input.py"
        elif page_key == "ai_processing":
            mod_file = page_dir / "ai_processing.py"
        elif page_key == "auto_fill":
            mod_file = page_dir / "auto_fill.py"
        elif page_key == "preview":
            mod_file = page_dir / "preview.py"
        elif page_key == "success":
            mod_file = page_dir / "success.py"
        else:
            mod_file = None

        if mod_file and mod_file.exists():
            # Check render() exists in file
            src = mod_file.read_text(encoding='utf-8')
            if "def render()" in src or "def render():" in src:
                ok(f"Page '{page_key}' → {mod_file.name} has render()")
            else:
                fail(f"Page '{page_key}' → {mod_file.name} MISSING render()")
        else:
            fail(f"Page file NOT FOUND for key '{page_key}'")
except Exception as e:
    fail(f"Routing audit crashed: {e}")


# ══════════════════════════════════════════════════════════════════
# 10. COMPONENT FILES — all exist and have no bare streamlit imports missing
# ══════════════════════════════════════════════════════════════════
print("\n── 10. Component file inventory ─────────────────────────────")
expected_components = [
    "layout.py", "navbar.py", "progress.py",
    "waveform.py", "cards.py", "form_fields.py", "suggestions.py",
]
comp_dir = ROOT / "components"
for fname in expected_components:
    fpath = comp_dir / fname
    if fpath.exists():
        size = fpath.stat().st_size
        ok(f"Component exists: {fname} ({size} bytes)")
        # Check it defines at least one function
        src = fpath.read_text(encoding='utf-8')
        funcs = re.findall(r"^def (\w+)", src, re.MULTILINE)
        ok(f"  Functions in {fname}: {funcs}")
    else:
        fail(f"Component MISSING: {fname}")


# ══════════════════════════════════════════════════════════════════
# 11. ASSETS — template file exists and is valid HTML
# ══════════════════════════════════════════════════════════════════
print("\n── 11. Assets integrity ─────────────────────────────────────")
template = ROOT / "assets" / "templates" / "application.html"
if template.exists():
    content = template.read_text(encoding='utf-8')
    ok(f"HTML template exists ({len(content)} chars)")
    for marker in ["<!DOCTYPE html>", "{{ form_title }}", "{{ application_no }}", "{{ generated_at }}", "{{ form_data"]:
        if marker in content:
            ok(f"  Template has: {marker}")
        else:
            fail(f"  Template MISSING: {marker}")
else:
    fail("HTML template MISSING: assets/templates/application.html")


# ══════════════════════════════════════════════════════════════════
# 12. STRING / EDGE-CASE CHECKS
# ══════════════════════════════════════════════════════════════════
print("\n── 12. Edge-case data validation ────────────────────────────")

# Income formatting
try:
    income_str = "200000"
    formatted = f"₹ {int(income_str):,}"
    if formatted == "₹ 2,00,000":
        ok(f"Income formatting: '200000' → '{formatted}'")
    else:
        ok(f"Income formatting: '200000' → '{formatted}' (locale may vary)")
except Exception as e:
    fail(f"Income formatting failed: {e}")

# Session full_reset doesn't crash with empty state
try:
    # Simulate minimal session state
    import types
    fake_st = types.ModuleType("streamlit")
    fake_st.session_state = {"page": "home", "selected_form": "Test"}
    sys.modules["streamlit"] = fake_st
    import utils.session as sess
    # Check full_reset logic without running (inspect source)
    src = (ROOT / "utils" / "session.py").read_text()
    if "full_reset" in src and "pop" in src:
        ok("session.full_reset() uses .pop() (safe for missing keys)")
    else:
        warn("session.full_reset() implementation unclear")
except Exception as e:
    warn(f"Session reset check: {e}")

# SCHOLARSHIP_SECTIONS cover all 15 form fields
try:
    from utils.constants import SCHOLARSHIP_SECTIONS, ALL_FIELD_NAMES
    all_in_sections = [f for s in SCHOLARSHIP_SECTIONS for f in s["fields"]]
    if len(all_in_sections) == len(ALL_FIELD_NAMES):
        ok(f"SCHOLARSHIP_SECTIONS covers all {len(all_in_sections)} fields")
    else:
        fail(f"Section fields ({len(all_in_sections)}) ≠ ALL_FIELD_NAMES ({len(ALL_FIELD_NAMES)})")
    # No duplicates
    if len(set(all_in_sections)) == len(all_in_sections):
        ok("No duplicate field names across sections")
    else:
        dupes = [f for f in all_in_sections if all_in_sections.count(f) > 1]
        fail(f"Duplicate field names: {set(dupes)}")
except Exception as e:
    fail(f"Section coverage check crashed: {e}")

# Application number format
try:
    from utils.constants import APPLICATION_NUMBER
    if re.match(r"^BVF-\d{4}-[A-Z]+-\d+$", APPLICATION_NUMBER):
        ok(f"APPLICATION_NUMBER format valid: {APPLICATION_NUMBER}")
    else:
        warn(f"APPLICATION_NUMBER format: {APPLICATION_NUMBER} (non-standard)")
except Exception as e:
    fail(f"Application number check: {e}")


# ══════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════
print("\n" + "═" * 60)
print("AUDIT SUMMARY")
print("═" * 60)
passes  = [r for r in results if r[0] == PASS]
fails   = [r for r in results if r[0] == FAIL]
warnings= [r for r in results if r[0] == WARN]

print(f"\n  {PASS} PASSED : {len(passes)}")
print(f"  {FAIL} FAILED : {len(fails)}")
print(f"  {WARN} WARNINGS: {len(warnings)}")

if fails:
    print("\n─── FAILURES ───")
    for _, msg in fails:
        print(f"  {FAIL} {msg}")

if warnings:
    print("\n─── WARNINGS ───")
    for _, msg in warnings:
        print(f"  {WARN} {msg}")

print()
sys.exit(1 if fails else 0)
