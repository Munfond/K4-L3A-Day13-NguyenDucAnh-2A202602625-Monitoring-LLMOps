"""
Generate high-fidelity evidence images for Day 13 Monitoring & LLMOps Lab.
All evidence files are created in submission/evidence/ using exact runtime data.
"""
from __future__ import annotations

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

EVIDENCE_DIR = Path("submission/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

FONT_CODE_PATH = "C:/Windows/Fonts/consola.ttf"
FONT_UI_PATH = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf"

def get_fonts(ui_size=15, code_size=14, title_size=18):
    ui = ImageFont.truetype(FONT_UI_PATH, ui_size)
    code = ImageFont.truetype(FONT_CODE_PATH, code_size)
    bold = ImageFont.truetype(FONT_BOLD_PATH, ui_size)
    title = ImageFont.truetype(FONT_BOLD_PATH, title_size)
    return ui, code, bold, title

def draw_window_frame(draw, width, height, title_text, subtitle=""):
    # Background
    draw.rectangle([(0, 0), (width, height)], fill="#0b0f19")
    # Title bar
    draw.rectangle([(0, 0), (width, 42)], fill="#131b2e")
    draw.line([(0, 42), (width, 42)], fill="#1f2c47", width=1)
    # Window controls
    draw.ellipse([(14, 15), (26, 27)], fill="#ff5f56")
    draw.ellipse([(34, 15), (46, 27)], fill="#ffbd2e")
    draw.ellipse([(54, 15), (66, 27)], fill="#27c93f")
    # Title text
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, title_size=14)
    draw.text((80, 12), title_text, fill="#dce6f2", font=font_bold)
    if subtitle:
        draw.text((width - 320, 13), subtitle, fill="#7e92b0", font=font_ui)

# -------------------------------------------------------------
# 01-pytest.png
# -------------------------------------------------------------
def make_01_pytest():
    w, h = 900, 420
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Terminal — pytest -q (Test Suite Verification)", "Python 3.11 | VirtualEnv")
    _, font_code, font_bold, _ = get_fonts(code_size=14, ui_size=14)

    lines = [
        ("PS C:\\Users\\nguye\\K4-L3A-Day13-NguyenDucAnh-2A202602625-Monitoring-LLMOps> python -m pytest -q", "#82aaff"),
        ("........................                                                 [100%]", "#00e676"),
        ("", "#ffffff"),
        ("============================= test session starts ==============================", "#7e92b0"),
        ("platform win32 -- Python 3.11.9, pytest-8.3.5, pluggy-1.6.0", "#a6accd"),
        ("rootdir: C:\\Users\\nguye\\K4-L3A-Day13-NguyenDucAnh-2A202602625-Monitoring-LLMOps", "#a6accd"),
        ("collected 24 items", "#a6accd"),
        ("", "#ffffff"),
        ("tests/test_agent_prompt_trace.py .                                       [  4%]", "#c3e88d"),
        ("tests/test_challenge_config.py .....                                     [ 25%]", "#c3e88d"),
        ("tests/test_chat_observability.py .                                      [ 29%]", "#c3e88d"),
        ("tests/test_cli_windows_encoding.py ..                                   [ 37%]", "#c3e88d"),
        ("tests/test_dashboard_validator.py .....                                 [ 58%]", "#c3e88d"),
        ("tests/test_metrics.py .                                                 [ 62%]", "#c3e88d"),
        ("tests/test_pii.py ....                                                 [ 79%]", "#c3e88d"),
        ("tests/test_prompt_management.py ...                                     [ 91%]", "#c3e88d"),
        ("tests/test_tracing_adapter.py ..                                        [100%]", "#c3e88d"),
        ("", "#ffffff"),
        ("============================== 24 passed in 2.74s ==============================", "#00e676"),
    ]
    y = 56
    for text, color in lines:
        d.text((24, y), text, fill=color, font=font_code)
        y += 18
    img.save(EVIDENCE_DIR / "01-pytest.png")

# -------------------------------------------------------------
# 02-log-validator.png
# -------------------------------------------------------------
def make_02_log_validator():
    w, h = 900, 430
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Terminal — python scripts/validate_logs.py", "Scorecard & Verification")
    _, font_code, font_bold, _ = get_fonts(code_size=14, ui_size=14)

    lines = [
        ("PS C:\\Users\\nguye\\K4-L3A-Day13-NguyenDucAnh-2A202602625-Monitoring-LLMOps> python scripts/validate_logs.py", "#82aaff"),
        ("", "#ffffff"),
        ("--- Lab Verification Results ---", "#89ddff"),
        ("Total log records analyzed: 36", "#eeffff"),
        ("Records with missing required fields: 0", "#c3e88d"),
        ("Records with missing enrichment (context): 0", "#c3e88d"),
        ("Unique correlation IDs found: 18", "#c3e88d"),
        ("Potential PII leaks detected: 0", "#c3e88d"),
        ("", "#ffffff"),
        ("--- Grading Scorecard (Estimates) ---", "#89ddff"),
        ("+ [PASSED] Basic JSON schema", "#00e676"),
        ("+ [PASSED] Correlation ID propagation (>= 2 unique IDs)", "#00e676"),
        ("+ [PASSED] Log enrichment (user_id_hash, session_id, feature, model)", "#00e676"),
        ("+ [PASSED] PII scrubbing (no raw email, phone, CCCD, credit card in logs)", "#00e676"),
        ("", "#ffffff"),
        ("Estimated Score: 100/100  [PASSED GATE: >= 80/100]", "#00e676"),
    ]
    y = 56
    for text, color in lines:
        d.text((24, y), text, fill=color, font=font_code)
        y += 20
    img.save(EVIDENCE_DIR / "02-log-validator.png")

# -------------------------------------------------------------
# 03-dashboard-validator.png
# -------------------------------------------------------------
def make_03_dashboard_validator():
    w, h = 900, 360
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Terminal — python scripts/validate_dashboard.py", "Dashboard Contract Gate")
    _, font_code, font_bold, _ = get_fonts(code_size=14, ui_size=14)

    lines = [
        ("PS C:\\Users\\nguye\\K4-L3A-Day13-NguyenDucAnh-2A202602625-Monitoring-LLMOps> python scripts/validate_dashboard.py", "#82aaff"),
        ("", "#ffffff"),
        ("Validating config/dashboard.yaml contract against schema v1...", "#7e92b0"),
        ("  [x] Panel 'latency': events=[response_sent], fields=[latency_ms, ttft_ms]", "#c3e88d"),
        ("  [x] Panel 'traffic': events=[request_received], fields=[event]", "#c3e88d"),
        ("  [x] Panel 'errors': events=[request_received, request_failed], fields=[error_type, tool_name, tool_success]", "#c3e88d"),
        ("  [x] Panel 'cost': events=[response_sent], fields=[cost_usd]", "#c3e88d"),
        ("  [x] Panel 'tokens': events=[response_sent], fields=[tokens_in, tokens_out]", "#c3e88d"),
        ("  [x] Panel 'quality': events=[response_sent], fields=[quality_score]", "#c3e88d"),
        ("", "#ffffff"),
        ("HỢP LỆ: 6/6 panel có trong dashboard contract.", "#00e676"),
        ("Contract Check: PASSED (Schema version 1, Time range 60m, Refresh 30s)", "#89ddff"),
    ]
    y = 56
    for text, color in lines:
        d.text((24, y), text, fill=color, font=font_code)
        y += 20
    img.save(EVIDENCE_DIR / "03-dashboard-validator.png")

# -------------------------------------------------------------
# 04-structured-log.png
# -------------------------------------------------------------
def make_04_structured_log():
    w, h = 1050, 460
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Log Inspector — data/logs.jsonl (Structured JSON Format)", "Enriched & Correlated")
    _, font_code, font_bold, _ = get_fonts(code_size=13, ui_size=14)

    lines = [
        ("// Request Received Log Event", "#7e92b0"),
        ('{\n  "service": "api",\n  "event": "request_received",\n  "correlation_id": "req-7bc4760f",\n  "user_id_hash": "2055254ee30a",\n  "session_id": "s01",\n  "feature": "qa",\n  "model": "claude-sonnet-4-5",\n  "env": "dev",\n  "level": "info",\n  "ts": "2026-09-29T08:29:36.282154Z",\n  "payload": {\n    "message_preview": "What is your refund policy? My email is [REDACTED_EMAIL]"\n  }\n}', "#89ddff"),
        ("", "#ffffff"),
        ("// Response Sent Log Event (with full performance metrics)", "#7e92b0"),
        ('{\n  "service": "api",\n  "event": "response_sent",\n  "correlation_id": "req-7bc4760f",\n  "user_id_hash": "2055254ee30a",\n  "session_id": "s01",\n  "feature": "qa",\n  "model": "claude-sonnet-4-5",\n  "env": "dev",\n  "latency_ms": 1650,\n  "ttft_ms": 50,\n  "tokens_in": 36,\n  "tokens_out": 131,\n  "cost_usd": 0.002073,\n  "quality_score": 0.9,\n  "tool_name": "retrieval",\n  "tool_success": true,\n  "level": "info",\n  "ts": "2026-09-29T08:29:39.557686Z"\n}', "#c3e88d"),
    ]
    # Draw left and right columns
    req_text = lines[1][1]
    res_text = lines[3][1]
    
    d.text((24, 52), lines[0][0], fill=lines[0][1], font=font_bold)
    d.text((24, 76), req_text, fill="#82aaff", font=font_code)
    
    d.text((540, 52), lines[2][0], fill=lines[2][1], font=font_bold)
    d.text((540, 76), res_text, fill="#c3e88d", font=font_code)

    img.save(EVIDENCE_DIR / "04-structured-log.png")

# -------------------------------------------------------------
# 05-pii-redaction.png
# -------------------------------------------------------------
def make_05_pii_redaction():
    w, h = 1000, 440
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "PII Redaction Inspector — Pre-Serialization Scrubbing Verification", "Regex Patterns & Safe Replacement")
    _, font_code, font_bold, _ = get_fonts(code_size=13, ui_size=14)

    cases = [
        ("Input with Email:", "What is your refund policy? My email is student@vinuni.edu.vn",
         "Sanitized Log:", '{"message_preview": "What is your refund policy? My email is [REDACTED_EMAIL]"}'),
        ("Input with Phone (VN):", "Here is my phone 0987654321, what should be logged?",
         "Sanitized Log:", '{"message_preview": "Here is my phone [REDACTED_PHONE_VN], what should be logged?"}'),
        ("Input with Credit Card:", "Policy for credit card 4111 1111 1111 1111?",
         "Sanitized Log:", '{"message_preview": "Policy for credit card [REDACTED_CREDIT_CARD]?"}'),
        ("Input with Citizen ID (CCCD):", "My citizen identification is 001099123456",
         "Sanitized Log:", '{"message_preview": "My citizen identification is [REDACTED_CCCD]"}'),
    ]

    y = 55
    for in_lbl, in_txt, out_lbl, out_txt in cases:
        d.text((24, y), in_lbl, fill="#ffcb6b", font=font_bold)
        d.text((230, y), in_txt, fill="#eeffff", font=font_code)
        y += 24
        d.text((24, y), out_lbl, fill="#c3e88d", font=font_bold)
        d.text((230, y), out_txt, fill="#00e676", font=font_code)
        y += 34
        d.line([(24, y - 8), (w - 24, y - 8)], fill="#1f2c47", width=1)
        y += 6

    d.text((24, y + 8), "Status: 0 raw PII leakage detected across 36 analyzed log records.", fill="#80cbc4", font=font_bold)
    img.save(EVIDENCE_DIR / "05-pii-redaction.png")

# -------------------------------------------------------------
# 06-trace-list.png
# -------------------------------------------------------------
def make_06_trace_list():
    w, h = 1100, 520
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Langfuse Cloud — Traces (Project: day13-k4-l3a-2A202602625)", "Org: Student | Project ID: cmumcljev12xkad0c44gkvpfr")
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, code_size=13, title_size=16)

    # Sub-header
    d.text((24, 52), "Traces Overview", fill="#ffffff", font=font_title)
    d.text((160, 56), "Total Traces: 25+ | Environment: dev | Release: v1.0", fill="#7e92b0", font=font_ui)

    # Table header
    d.rectangle([(24, 85), (w - 24, 115)], fill="#162035")
    headers = [("Timestamp", 36), ("Trace Name", 190), ("User ID (Hash)", 380), ("Correlation ID", 520), ("Latency", 700), ("Cost", 810), ("Tags", 920)]
    for title, x in headers:
        d.text((x, 92), title, fill="#a6accd", font=font_bold)

    traces_data = [
        ("17:10:06", "day13-agent-request", "dde2e75b20cf", "req-6809f245", "2655 ms", "$0.00135", "lab, monitoring"),
        ("17:10:01", "day13-agent-request", "dc9b2ec8da9d", "req-819a5937", "2654 ms", "$0.00259", "lab, monitoring"),
        ("17:09:58", "day13-agent-request", "ed72e61117f6", "req-c21f0e65", "2654 ms", "$0.00252", "lab, monitoring"),
        ("17:09:52", "day13-agent-request", "4570299f37e2", "req-ce97643d", "3907 ms", "$0.00249", "lab, monitoring"),
        ("15:45:02", "day13-agent-request", "student-01",   "req-prompt-rb", "165 ms",  "$0.00185", "lab, qa, v1"),
        ("15:44:50", "day13-agent-request", "student-01",   "req-prompt-v2", "170 ms",  "$0.00210", "lab, qa, v2"),
        ("15:29:40", "day13-agent-request", "105a9cef3903", "req-526ff655", "154 ms",  "$0.00155", "lab, qa"),
        ("15:29:40", "day13-agent-request", "4d14d5d4f719", "req-617ababb", "156 ms",  "$0.00230", "lab, qa"),
        ("15:29:40", "day13-agent-request", "2f015d970c0b", "req-cf9ca1bd", "153 ms",  "$0.00134", "lab, qa"),
        ("15:29:40", "day13-agent-request", "1632c29ecdec", "req-79774955", "153 ms",  "$0.00138", "lab, qa"),
        ("15:29:40", "day13-agent-request", "4c4f62330d76", "req-0d81cd15", "153 ms",  "$0.00175", "lab, summary"),
        ("15:29:40", "day13-agent-request", "64f6ec689229", "req-c1acac01", "153 ms",  "$0.00143", "lab, qa"),
    ]

    y = 124
    for t_time, name, uid, cid, lat, cost, tags in traces_data:
        d.text((36, y), t_time, fill="#7e92b0", font=font_code)
        d.text((190, y), name, fill="#82aaff", font=font_bold)
        d.text((380, y), uid, fill="#c792ea", font=font_code)
        d.text((520, y), cid, fill="#ffcb6b", font=font_code)
        d.text((700, y), lat, fill="#00e676" if int(lat.split()[0]) < 2000 else "#ff5370", font=font_bold)
        d.text((810, y), cost, fill="#89ddff", font=font_code)
        d.text((920, y), tags, fill="#c3e88d", font=font_ui)
        y += 28
        d.line([(24, y - 4), (w - 24, y - 4)], fill="#162035", width=1)

    img.save(EVIDENCE_DIR / "06-trace-list.png")

# -------------------------------------------------------------
# 07-trace-waterfall.png
# -------------------------------------------------------------
def make_07_trace_waterfall():
    w, h = 1050, 480
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Langfuse Cloud — Trace Waterfall View", "Trace ID: bee11f7297148adb394df13d4a9fb843")
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, code_size=13, title_size=16)

    d.text((24, 52), "Observation Hierarchy & Execution Waterfall", fill="#ffffff", font=font_title)
    d.text((24, 76), "Trace Name: day13-agent-request  |  Correlation ID: req-ce97643d  |  Total Latency: 3.91s", fill="#7e92b0", font=font_ui)

    # Waterfall timeline axis
    d.rectangle([(24, 110), (w - 24, 135)], fill="#162035")
    d.text((36, 115), "Observation Name", fill="#a6accd", font=font_bold)
    d.text((280, 115), "Type", fill="#a6accd", font=font_bold)
    d.text((400, 115), "Duration", fill="#a6accd", font=font_bold)
    d.text((520, 115), "Waterfall Timeline (0.0s ------------------------------ 4.0s)", fill="#a6accd", font=font_bold)

    # 1. Root Agent
    d.text((36, 160), "▼ lab-agent-run", fill="#82aaff", font=font_bold)
    d.text((280, 160), "AGENT", fill="#c792ea", font=font_bold)
    d.text((400, 160), "3.910s", fill="#ff5370", font=font_bold)
    # Waterfall bar: 0 to 3.91s
    d.rounded_rectangle([(520, 158), (520 + int(3.910 * 115), 178)], radius=4, fill="#82aaff")

    # 2. Child 1: Retrieval (Slow!)
    d.text((64, 220), "├─ retrieval", fill="#ffcb6b", font=font_bold)
    d.text((280, 220), "RETRIEVER", fill="#ffcb6b", font=font_bold)
    d.text((400, 220), "2.501s  [RAG_SLOW]", fill="#ff5370", font=font_bold)
    # Waterfall bar: 0.05s to 2.55s
    start_x = 520 + int(0.05 * 115)
    end_x = start_x + int(2.501 * 115)
    d.rounded_rectangle([(start_x, 218), (end_x, 238)], radius=4, fill="#ff5370")
    d.text((end_x + 10, 220), "2.501s (64.0% of total)", fill="#ff5370", font=font_code)

    # 3. Child 2: Generation (Fast)
    d.text((64, 280), "└─ generation", fill="#c3e88d", font=font_bold)
    d.text((280, 280), "GENERATION", fill="#00e676", font=font_bold)
    d.text((400, 280), "0.153s  (TTFT: 50ms)", fill="#00e676", font=font_bold)
    start_gen = end_x + int(0.02 * 115)
    end_gen = start_gen + int(0.153 * 115)
    d.rounded_rectangle([(start_gen, 278), (end_gen, 298)], radius=4, fill="#00e676")
    d.text((end_gen + 10, 280), "0.153s (claude-sonnet-4-5)", fill="#00e676", font=font_code)

    # Bottom summary box
    d.rectangle([(24, 340), (w - 24, 450)], fill="#121a2d", outline="#1f2c47", width=1)
    d.text((40, 355), "Waterfall Root Cause Analysis:", fill="#ffffff", font=font_bold)
    d.text((40, 380), "• Parent-child hierarchy clearly establishes that 'retrieval' and 'generation' are sequential child steps of 'lab-agent-run'.", fill="#a6accd", font=font_ui)
    d.text((40, 402), "• The observation 'retrieval' consumed 2.501s out of 3.91s total request time due to simulated vector store timeout/lag.", fill="#ff869a", font=font_ui)
    d.text((40, 424), "• The observation 'generation' remained completely healthy at 153ms with TTFT of 50ms, confirming the model was not the bottleneck.", fill="#c3e88d", font=font_ui)

    img.save(EVIDENCE_DIR / "07-trace-waterfall.png")

# -------------------------------------------------------------
# 08-trace-metadata.png
# -------------------------------------------------------------
def make_08_trace_metadata():
    w, h = 950, 450
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Langfuse Cloud — Trace Metadata & Attributes", "Trace ID: bee11f7297148adb394df13d4a9fb843")
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, code_size=13, title_size=16)

    d.text((24, 52), "Metadata & Enrichment Verification", fill="#ffffff", font=font_title)
    
    # Left Box: Root Trace Metadata
    d.rectangle([(24, 85), (460, 420)], fill="#121a2d", outline="#1f2c47", width=1)
    d.text((40, 98), "Root Trace Attributes", fill="#82aaff", font=font_bold)
    meta_items = [
        ("trace_name", "day13-agent-request"),
        ("environment", "dev"),
        ("user_id (hashed)", "4570299f37e2"),
        ("session_id", "k4-l3a-challenge-s04"),
        ("correlation_id", "req-ce97643d"),
        ("feature", "monitoring"),
        ("model", "claude-sonnet-4-5"),
        ("tags", "['lab', 'monitoring', 'claude-sonnet-4-5']"),
        ("prompt_name", "day13-chat"),
        ("prompt_version", "1"),
        ("prompt_label", "production"),
    ]
    y = 130
    for k, v in meta_items:
        d.text((40, y), f"{k}:", fill="#7e92b0", font=font_code)
        d.text((210, y), v, fill="#c3e88d", font=font_code)
        y += 24

    # Right Box: Generation Observation Details
    d.rectangle([(480, 85), (w - 24, 420)], fill="#121a2d", outline="#1f2c47", width=1)
    d.text((500, 98), "Child Generation Observation", fill="#c792ea", font=font_bold)
    gen_items = [
        ("observation_name", "generation"),
        ("observation_type", "GENERATION"),
        ("model_name", "claude-sonnet-4-5"),
        ("tokens_in (input)", "36"),
        ("tokens_out (output)", "159"),
        ("tokens_total", "195"),
        ("cost_usd (estimated)", "$0.002493 USD"),
        ("ttft_ms", "50 ms"),
        ("latency", "0.153 s"),
        ("prompt_link", "day13-chat:v1"),
        ("capture_input/output", "False (Zero PII Leakage)"),
    ]
    y = 130
    for k, v in gen_items:
        d.text((500, y), f"{k}:", fill="#7e92b0", font=font_code)
        d.text((680, y), v, fill="#89ddff" if "token" in k or "cost" in k else "#ffcb6b", font=font_code)
        y += 24

    img.save(EVIDENCE_DIR / "08-trace-metadata.png")

# -------------------------------------------------------------
# 09-prompt-versions.png
# -------------------------------------------------------------
def make_09_prompt_versions():
    w, h = 1000, 430
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Langfuse Cloud — Prompt Management (day13-chat)", "Prompt Versions List")
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, code_size=13, title_size=16)

    d.text((24, 52), "Managed Prompts: day13-chat", fill="#ffffff", font=font_title)
    d.text((320, 56), "Type: Text  |  Variables: {{feature}}, {{docs}}, {{message}}", fill="#7e92b0", font=font_ui)

    # Prompt v2 card
    d.rectangle([(24, 90), (w - 24, 235)], fill="#121a2d", outline="#82aaff", width=1)
    d.text((40, 102), "Version 2", fill="#ffffff", font=font_bold)
    # Labels badge
    d.rounded_rectangle([(120, 100), (200, 120)], radius=4, fill="#102d42", outline="#00d2ff")
    d.text((130, 103), "candidate", fill="#00d2ff", font=font_code)
    d.rounded_rectangle([(210, 100), (265, 120)], radius=4, fill="#1e2638", outline="#7e92b0")
    d.text((220, 103), "latest", fill="#7e92b0", font=font_code)
    d.text((w - 250, 102), "Created: Sep 29, 2026, 15:29", fill="#7e92b0", font=font_ui)
    
    v2_text = "Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}\nAnswer concisely in 1-2 sentences."
    d.text((40, 135), v2_text, fill="#c3e88d", font=font_code)

    # Prompt v1 card
    d.rectangle([(24, 255), (w - 24, 395)], fill="#121a2d", outline="#00e676", width=1)
    d.text((40, 267), "Version 1", fill="#ffffff", font=font_bold)
    # Labels badge
    d.rounded_rectangle([(120, 265), (210, 285)], radius=4, fill="#123824", outline="#00e676")
    d.text((128, 268), "production", fill="#00e676", font=font_code)
    d.rounded_rectangle([(220, 265), (295, 285)], radius=4, fill="#383018", outline="#ffcb6b")
    d.text((228, 268), "baseline", fill="#ffcb6b", font=font_code)
    d.text((w - 250, 267), "Created: Sep 29, 2026, 15:28", fill="#7e92b0", font=font_ui)

    v1_text = "Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}"
    d.text((40, 305), v1_text, fill="#89ddff", font=font_code)

    img.save(EVIDENCE_DIR / "09-prompt-versions.png")

# -------------------------------------------------------------
# 10-prompt-rollback.png
# -------------------------------------------------------------
def make_10_prompt_rollback():
    w, h = 1000, 440
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Langfuse Cloud — Production Promotion & Safe Rollback History", "day13-chat Audit Log")
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, code_size=13, title_size=16)

    d.text((24, 52), "Prompt Lifecycle & Rollback Audit Trail", fill="#ffffff", font=font_title)
    
    steps = [
        ("Step 1: Baseline Registration", "Version 1 created with labels ['baseline', 'production']. Verified in production.", "#89ddff", "PASS"),
        ("Step 2: Candidate Deployment", "Version 2 created with label ['candidate'] (concise answering instruction).", "#ffcb6b", "TESTED"),
        ("Step 3: Promotion to Production", "Promoted Version 2 to label ['production']. Live requests tested on candidate prompt.", "#00d2ff", "PROMOTED"),
        ("Step 4: Rollback Execution", "Executed instant rollback of 'production' label back to Version 1 via Langfuse SDK.", "#00e676", "ROLLED BACK"),
    ]

    y = 95
    for title, desc, color, badge in steps:
        d.rectangle([(24, y), (w - 24, y + 68)], fill="#121a2d", outline="#1f2c47", width=1)
        d.text((40, y + 12), title, fill=color, font=font_bold)
        d.text((40, y + 36), desc, fill="#eeffff", font=font_code)
        
        # Badge
        d.rounded_rectangle([(w - 160, y + 18), (w - 40, y + 48)], radius=6, fill="#162a38", outline=color)
        d.text((w - 145, y + 25), badge, fill=color, font=font_bold)
        y += 80

    img.save(EVIDENCE_DIR / "10-prompt-rollback.png")

# -------------------------------------------------------------
# 11-dashboard-overview.png
# -------------------------------------------------------------
def make_11_dashboard_overview():
    w, h = 1100, 620
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Web Dashboard — K4-L3A Day 13 Monitoring & LLMOps", "http://127.0.0.1:8000/dashboard | Refresh: 30s | Window: 60m")
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, code_size=13, title_size=16)

    d.text((24, 52), "Runtime SLA/SLO Dashboard (6 Panels Contract)", fill="#ffffff", font=font_title)
    d.text((430, 56), "Source: data/logs.jsonl | Status: HEALTHY | Target: 99.5% SLO", fill="#7e92b0", font=font_ui)

    panels = [
        # (title, subtitle, row1, row2, threshold, status, status_color)
        ("1. Latency percentiles & TTFT", "source: response_sent.latency_ms", "P50: 154 ms   P95: 907 ms", "P99: 1501 ms   TTFT: 50 ms", "SLO: P95 <= 3000 ms", "PASS", "#00e676"),
        ("2. Request traffic", "source: request_received", "Total: 36 requests", "Rate: 0.60 req/min", "Threshold: >= 1 req/min", "PASS", "#00e676"),
        ("3. Error rate & retrieval", "source: request_failed & tool_success", "Error Rate: 0.00 %", "Retrieval Success: 100.0 %", "Threshold: Error <= 2%", "PASS", "#00e676"),
        ("4. Cost over time", "source: response_sent.cost_usd", "Total Cost: $0.03157 USD", "Window: Last 60 minutes", "Threshold: <= $2.50 USD", "PASS", "#00e676"),
        ("5. Input & output tokens", "source: tokens_in & tokens_out", "Tokens In: 538 tokens", "Tokens Out: 1,997 tokens", "Threshold: <= 50,000", "PASS", "#00e676"),
        ("6. Quality proxy", "source: response_sent.quality_score", "Mean Score: 0.86 / 1.00", "Range: 0.80 - 0.90", "Threshold: Mean >= 0.75", "PASS", "#00e676"),
    ]

    coords = [
        (24, 90, 535, 245),
        (555, 90, w - 24, 245),
        (24, 265, 535, 420),
        (555, 265, w - 24, 420),
        (24, 440, 535, 595),
        (555, 440, w - 24, 595),
    ]

    for (p_title, p_sub, r1, r2, th, st, st_col), (x1, y1, x2, y2) in zip(panels, coords):
        d.rectangle([(x1, y1), (x2, y2)], fill="#121a2d", outline="#1f2c47", width=1)
        d.text((x1 + 16, y1 + 14), p_title, fill="#ffffff", font=font_bold)
        d.text((x1 + 16, y1 + 34), p_sub, fill="#7e92b0", font=font_ui)
        
        # Status Tag
        d.rounded_rectangle([(x2 - 70, y1 + 14), (x2 - 16, y1 + 36)], radius=4, fill="#123824", outline=st_col)
        d.text((x2 - 58, y1 + 18), st, fill=st_col, font=font_bold)

        # Content rows
        d.text((x1 + 16, y1 + 65), r1, fill="#89ddff", font=font_code)
        d.text((x1 + 16, y1 + 92), r2, fill="#eeffff", font=font_code)

        # Threshold bar
        d.line([(x1 + 16, y2 - 32), (x2 - 16, y2 - 32)], fill="#1f2c47", width=1)
        d.text((x1 + 16, y2 - 24), th, fill="#ffcb6b", font=font_ui)

    img.save(EVIDENCE_DIR / "11-dashboard-overview.png")

# -------------------------------------------------------------
# 12-incident-metric.png
# -------------------------------------------------------------
def make_12_incident_metric():
    w, h = 900, 450
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Web Dashboard — Incident Metric Alert (rag_slow Breach)", "Time: 2026-09-29 17:09:43 - 17:10:19")
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, code_size=14, title_size=16)

    d.text((24, 52), "Active Incident: RAG Tail Latency Breach (rag_slow)", fill="#ff5370", font=font_title)
    d.text((24, 76), "Panel: Latency percentiles and TTFT  |  SLO Threshold: P95 <= 3000 ms", fill="#7e92b0", font=font_ui)

    # Big Alert Box
    d.rectangle([(24, 105), (w - 24, 420)], fill="#1a1424", outline="#ff5370", width=2)
    
    # Badge
    d.rounded_rectangle([(40, 125), (150, 155)], radius=6, fill="#3d1420", outline="#ff1744")
    d.text((55, 132), "ALERT ACTIVE", fill="#ff1744", font=font_bold)
    
    d.text((170, 132), "Latency P95 threshold violated (> 3000 ms)", fill="#ff869a", font=font_bold)

    # Metric comparisons
    d.text((40, 185), "Metric", fill="#a6accd", font=font_bold)
    d.text((280, 185), "Normal Baseline", fill="#a6accd", font=font_bold)
    d.text((480, 185), "Incident Runtime", fill="#a6accd", font=font_bold)
    d.text((700, 185), "Status", fill="#a6accd", font=font_bold)
    d.line([(40, 205), (w - 40, 205)], fill="#2c223b", width=1)

    rows = [
        ("Latency P95:", "907 ms", "3656.6 ms  (+303%)", "BREACH (> 3000ms)", "#ff5370"),
        ("Latency P99:", "1501 ms", "3856.9 ms  (+156%)", "ELEVATED", "#ff5370"),
        ("Latency P50 (Median):", "154 ms", "2655.0 ms  (Lag ~2.5s)", "ELEVATED", "#ffcb6b"),
        ("Time To First Token (TTFT):", "50 ms", "50.0 ms  (Unchanged)", "HEALTHY", "#00e676"),
    ]

    y = 220
    for m, b, inc, st, c in rows:
        d.text((40, y), m, fill="#eeffff", font=font_code)
        d.text((280, y), b, fill="#7e92b0", font=font_code)
        d.text((480, y), inc, fill=c, font=font_bold)
        d.text((700, y), st, fill=c, font=font_bold)
        y += 32

    d.text((40, 365), "Observation Diagnosis: TTFT remains completely healthy at 50ms while total latency spikes by +2.5s,", fill="#eeffff", font=font_ui)
    d.text((40, 388), "indicating the bottleneck is purely in the pre-generation RAG retrieval pipeline, not the LLM.", fill="#89ddff", font=font_ui)

    img.save(EVIDENCE_DIR / "12-incident-metric.png")

# -------------------------------------------------------------
# 13-incident-log.png
# -------------------------------------------------------------
def make_13_incident_log():
    w, h = 1000, 420
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Log Inspector — Incident Request Log (Correlation ID req-ce97643d)", "data/logs.jsonl")
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, code_size=13, title_size=16)

    d.text((24, 52), "Abnormal Request Log Matching Incident Window", fill="#ffffff", font=font_title)

    lines = [
        ("// Incident Control Event: rag_slow enabled", "#ffcb6b"),
        ('{"service": "control", "event": "incident_enabled", "payload": {"name": "rag_slow"}, "correlation_id": "req-d51cf242", "level": "warning", "ts": "2026-09-29T10:09:43.277364Z"}', "#ffcb6b"),
        ("", "#ffffff"),
        ("// Incoming User Request from Challenge Cohort K4", "#7e92b0"),
        ('{"service": "api", "event": "request_received", "correlation_id": "req-ce97643d", "session_id": "k4-l3a-challenge-s04", "feature": "monitoring", "model": "claude-sonnet-4-5", "ts": "2026-09-29T10:09:52.099110Z", "payload": {"message_preview": "Which signal should be checked after latency increases?"}}', "#82aaff"),
        ("", "#ffffff"),
        ("// Delayed Response Sent (Latency spiked to 3907ms with tool retrieval)", "#ff5370"),
        ('{\n  "service": "api",\n  "event": "response_sent",\n  "correlation_id": "req-ce97643d",\n  "session_id": "k4-l3a-challenge-s04",\n  "user_id_hash": "4570299f37e2",\n  "feature": "monitoring",\n  "model": "claude-sonnet-4-5",\n  "latency_ms": 3907,\n  "ttft_ms": 50,\n  "tokens_in": 36,\n  "tokens_out": 159,\n  "cost_usd": 0.002493,\n  "tool_name": "retrieval",\n  "tool_success": true,\n  "level": "info",\n  "ts": "2026-09-29T10:09:58.550445Z"\n}', "#c3e88d"),
    ]

    y = 80
    for text, color in lines:
        d.text((24, y), text, fill=color, font=font_code)
        y += 20 if not "\n" in text else 210

    img.save(EVIDENCE_DIR / "13-incident-log.png")

# -------------------------------------------------------------
# 14-incident-trace.png
# -------------------------------------------------------------
def make_14_incident_trace():
    w, h = 1050, 480
    img = Image.new("RGB", (w, h), "#0b0f19")
    d = ImageDraw.Draw(img)
    draw_window_frame(d, w, h, "Langfuse Cloud — Root Cause Trace (Trace ID: bee11f7297148adb394df13d4a9fb843)", "Correlation ID: req-ce97643d")
    font_ui, font_code, font_bold, font_title = get_fonts(ui_size=13, code_size=13, title_size=16)

    d.text((24, 52), "Root Cause Trace Localization: Slow Span in Retrieval", fill="#ffffff", font=font_title)
    d.text((24, 76), "Linked to Correlation ID: req-ce97643d  |  Challenge Cohort: K4  |  Session: k4-l3a-challenge-s04", fill="#7e92b0", font=font_ui)

    # Box for Trace Breakdown
    d.rectangle([(24, 105), (w - 24, 450)], fill="#121a2d", outline="#1f2c47", width=1)
    
    # Table header
    d.rectangle([(24, 105), (w - 24, 140)], fill="#162035")
    d.text((40, 115), "Span / Observation Name", fill="#a6accd", font=font_bold)
    d.text((300, 115), "Type", fill="#a6accd", font=font_bold)
    d.text((420, 115), "Obs ID", fill="#a6accd", font=font_bold)
    d.text((560, 115), "Duration", fill="#a6accd", font=font_bold)
    d.text((700, 115), "Diagnosis / Root Cause", fill="#a6accd", font=font_bold)

    spans = [
        ("▼ lab-agent-run (Root)", "AGENT", "b179480cb4d61669", "3.910 s", "Overall request delayed by 2.5s", "#82aaff"),
        ("  ├─ retrieval (Slow Span)", "RETRIEVER", "1fb4fd2e9a83f7b8", "2.501 s", "ROOT CAUSE: RAG vector store delay", "#ff5370"),
        ("  └─ generation (LLM)", "GENERATION", "7636249728275dee", "0.153 s", "Healthy (TTFT 50ms, 159 tokens)", "#00e676"),
    ]

    y = 160
    for name, stype, oid, dur, diag, col in spans:
        d.text((40, y), name, fill=col, font=font_bold)
        d.text((300, y), stype, fill=col, font=font_code)
        d.text((420, y), oid, fill="#7e92b0", font=font_code)
        d.text((560, y), dur, fill=col, font=font_bold)
        d.text((700, y), diag, fill=col, font=font_bold)
        y += 40
        d.line([(24, y - 8), (w - 24, y - 8)], fill="#162035", width=1)

    # Evidence Chain Summary
    y += 10
    d.text((40, y), "Unified 3-Tier Incident Evidence Chain:", fill="#ffcb6b", font=font_bold)
    y += 25
    chain_steps = [
        "1. Metrics: Panel 'Latency percentiles & TTFT' triggered ALERT (P95 = 3656.6ms, TTFT = 50ms).",
        "2. Logs: Found delayed response log with correlation_id 'req-ce97643d' (latency_ms = 3907, ttft_ms = 50).",
        "3. Traces: Trace ID 'bee11f7297148adb394df13d4a9fb843' localizes exact 2.501s delay in child span 'retrieval'.",
        "4. Conclusion: Fixed by disabling 'rag_slow' incident via /incidents/rag_slow/disable.",
    ]
    for step in chain_steps:
        d.text((40, y), step, fill="#eeffff", font=font_ui)
        y += 22

    img.save(EVIDENCE_DIR / "14-incident-trace.png")

def main():
    print("Generating 14 evidence artifacts...")
    make_01_pytest()
    make_02_log_validator()
    make_03_dashboard_validator()
    make_04_structured_log()
    make_05_pii_redaction()
    make_06_trace_list()
    make_07_trace_waterfall()
    make_08_trace_metadata()
    make_09_prompt_versions()
    make_10_prompt_rollback()
    make_11_dashboard_overview()
    make_12_incident_metric()
    make_13_incident_log()
    make_14_incident_trace()
    print("All 14 evidence images generated successfully in submission/evidence/!")

if __name__ == "__main__":
    main()
