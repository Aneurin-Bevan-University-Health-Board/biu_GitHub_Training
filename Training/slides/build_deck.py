#!/usr/bin/env python3
"""Build the GitHub training deck and keep it in sync with the markdown.

Single source of truth:  Training/slides/deck_content.yaml

    python Training/slides/build_deck.py            # rebuild the deck + rewrite generated markdown
    python Training/slides/build_deck.py --check    # change nothing; exit 1 if anything has drifted

What it keeps in sync
---------------------
1. Training/GitHub_Training_Day.pptx   - generated from the YAML using template.pptx (the SDE Training Day style)
2. Each session markdown file          - a generated "Slide Deck Content" block, plus the Duration / Time
                                         header lines and the "Session N of M" footer
3. README.md and Training/README.md    - the generated session timetable table

Requirements:  pip install -r Training/slides/requirements.txt
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

import yaml
from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.util import Pt

HERE = Path(__file__).resolve().parent
TRAINING = HERE.parent
REPO = TRAINING.parent
CONTENT_FILE = HERE / "deck_content.yaml"
TEMPLATE_FILE = HERE / "template.pptx"
DECK_FILE = TRAINING / "GitHub_Training_Day.pptx"
DECK_NAME = DECK_FILE.name

# Style taken from the SDE Training Day deck
NAVY = RGBColor(0x00, 0x20, 0x60)
GREY = RGBColor(0x44, 0x54, 0x6A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CYAN = RGBColor(0x01, 0xB0, 0xFF)
FONT = "Arial"
BODY_HEIGHT_PT = 350  # usable height of the body placeholder (about 359pt), with a safety margin
BODY_WIDTH_PT = 800  # usable text width in points
IMG_TEXT_WIDTH_PT = 420  # text width on a slide with the picture on the right
IMG_BOTTOM_TEXT_HEIGHT_PT = 165  # text height on a slide with the picture underneath
IMAGES_DIR = TRAINING / "images"

LAYOUT_TITLE, LAYOUT_CONTENT, LAYOUT_SECTION = 0, 1, 2

BEGIN_MARK = "<!-- SLIDES:BEGIN"
END_MARK = "<!-- SLIDES:END -->"
TABLE_BEGIN = "<!-- SESSIONS-TABLE:BEGIN"
TABLE_END = "<!-- SESSIONS-TABLE:END -->"


# --------------------------------------------------------------------------------------
# 1. Turn the YAML into an ordered plan of slides (used by the deck AND the markdown)
# --------------------------------------------------------------------------------------
def load_spec() -> dict:
    text = CONTENT_FILE.read_text(encoding="utf-8")
    # YAML treats " #" in an unquoted value as the start of a comment and silently drops the rest of the line.
    for n, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("- ") and " #" in stripped and not stripped[2:].lstrip().startswith(('"', "'", "{")):
            raise SystemExit(f"deck_content.yaml line {n}: put quotes around text containing ' #': {stripped}")
    spec = yaml.safe_load(text)
    # An unquoted bullet containing ': ' becomes a dict instead of text: catch it with a clear message.
    for sess in spec["sessions"]:
        slides = list(sess["slides"])
        for sl in slides:
            for sec in sl.get("sections", []):
                for b in sec["bullets"]:
                    if not isinstance(b, str):
                        raise SystemExit(f"Slide '{sl['title']}': a bullet is not text (put quotes round bullets containing ': '): {b}")
        for b in (sess.get("your_area") or {}).get("steps", []):
            if not isinstance(b, str):
                raise SystemExit(f"Session {sess['number']} your_area step is not text: {b}")
    return spec


def agenda_lines(spec: dict) -> list[str]:
    breaks = {b["after_session"]: b for b in spec["deck"].get("breaks", [])}
    lines = []
    for s in spec["sessions"]:
        lines.append(f"{s['time']} | {s['title']} ({s['duration']})")
        if s["number"] in breaks:
            b = breaks[s["number"]]
            lines.append(f"{b['time']} | {b['label']}")
    return lines


def build_plan(spec: dict) -> list[dict]:
    """Return every slide, in order, as a dict with its kind and its text paragraphs."""
    d = spec["deck"]
    plan = [{"kind": "title", "title": d["title"], "subtitle": d["subtitle"], "session": None}]
    plan.append(
        {
            "kind": "agenda",
            "title": "Agenda",
            "heading": "Today's Sessions",
            "bullets": agenda_lines(spec),
            "note": d["agenda_footer"],
            "session": None,
        }
    )
    for s in spec["sessions"]:
        plan.append(
            {
                "kind": "section",
                "title": s["title"],
                "subtitle": f"Session {s['number']} | {s['duration']}",
                "session": s["number"],
            }
        )
        # Slides marked `optional: true` come after the Your Area checkpoint, at the very end of the session.
        ordered = [sl for sl in s["slides"] if not sl.get("optional")]
        optional = [sl for sl in s["slides"] if sl.get("optional")]
        for sl in ordered:
            if sl.get("image"):
                if not (IMAGES_DIR / sl["image"]).exists():
                    raise SystemExit(f"Slide '{sl['title']}': image {sl['image']} not found in Training/images/")
                if not sl.get("image_alt"):
                    raise SystemExit(f"Slide '{sl['title']}': image_alt is required (accessibility)")
                if sl.get("image_position", "right") not in ("right", "bottom"):
                    raise SystemExit(f"Slide '{sl['title']}': image_position must be right or bottom")
            plan.append({"kind": "content", "session": s["number"], **sl})
        if s.get("your_area"):
            plan.append({"kind": "content", "session": s["number"], **your_area_slide(s)})
        for sl in optional:
            plan.append({"kind": "content", "session": s["number"], **sl})
    plan.append({"kind": "title", "title": d["closing_title"], "subtitle": d["closing_subtitle"], "session": None})
    for i, item in enumerate(plan, start=1):
        item["number"] = i
    return plan


def your_area_slide(s: dict) -> dict:
    """The 'Your Area' checkpoint slide of a session, generated from its your_area block."""
    ya = s["your_area"]
    slide = {
        "title": f"Your Area: Checkpoint {s['number']}",
        "sections": [
            {"heading": f"{ya['heading']} ({ya['minutes']} minutes)", "bullets": ya["steps"]},
            {"heading": "Your folder now contains", "bullets": [ya["checkpoint"]]},
        ],
    }
    for k in ("image", "image_alt", "image_position"):
        if ya.get(k):
            slide[k] = ya[k]
    return slide


def plan_texts(item: dict) -> list[str]:
    """The paragraphs of text that must appear on a slide, in order."""
    k = item["kind"]
    if k in ("title", "section"):
        return [item["title"], item["subtitle"]]
    if k == "agenda":
        return [item["title"], item["heading"], *item["bullets"], item["note"]]
    out = [item["title"]]
    for sec in item["sections"]:
        out.append(sec["heading"])
        out.extend(sec["bullets"])
    if item.get("note"):
        out.append(item["note"])
    if item.get("callout"):
        out.append(item["callout"])
    if item.get("image"):
        out.append(f"[image:{item['image']}]")
    return out


# --------------------------------------------------------------------------------------
# 2. PowerPoint
# --------------------------------------------------------------------------------------
def _ppr(p, bullet: bool, space_before: int) -> None:
    """Replace a paragraph's properties with the SDE deck's bullet / spacing settings."""
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    for old in p._p.findall(qn("a:pPr")):
        p._p.remove(old)
    marl, indent = (342900, -342900) if bullet else (0, 0)
    bu = (
        '<a:buClr><a:srgbClr val="44546A"/></a:buClr><a:buSzPts val="1600"/><a:buFont typeface="Arial"/><a:buChar char="&#8226;"/>'
        if bullet
        else "<a:buNone/>"
    )
    xml = (
        f'<a:pPr xmlns:a="{a}" marL="{marl}" indent="{indent}" algn="l">'
        f'<a:lnSpc><a:spcPct val="90000"/></a:lnSpc><a:spcBef><a:spcPts val="{space_before * 100}"/></a:spcBef>'
        f'<a:spcAft><a:spcPts val="0"/></a:spcAft>{bu}</a:pPr>'
    )
    p._p.insert(0, etree.fromstring(xml))


def _add_para(tf, text: str, size: int, bold: bool, color: RGBColor, bullet: bool, space_before: int, first: bool):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    _ppr(p, bullet, space_before)
    run = p.add_run()
    run.text = text
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return p


def _set_plain(shape, text: str, size: int, bold: bool, color: RGBColor) -> None:
    """Single-paragraph placeholder with explicit font settings and no indent."""
    tf = shape.text_frame
    tf.text = ""
    p = tf.paragraphs[0]
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    for old in p._p.findall(qn("a:pPr")):
        p._p.remove(old)
    p._p.insert(0, etree.fromstring(f'<a:pPr xmlns:a="{a}" marL="0" indent="0" algn="l"><a:buNone/></a:pPr>'))
    run = p.add_run()
    run.text = text
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color


def body_box(item: dict) -> tuple[float, float]:
    """(width, height) in points available to the text on a slide; image slides give some room to the picture."""
    pos = item.get("image_position", "right") if item.get("image") else None
    if pos == "right":
        return IMG_TEXT_WIDTH_PT, BODY_HEIGHT_PT
    if pos == "bottom":
        return BODY_WIDTH_PT, IMG_BOTTOM_TEXT_HEIGHT_PT
    return BODY_WIDTH_PT, BODY_HEIGHT_PT


def _lines(text: str, size: int, indent_pt: float = 0, width: float = BODY_WIDTH_PT) -> int:
    chars_per_line = max(10, int((width - indent_pt) / (size * 0.52)))
    return max(1, math.ceil(len(text) / chars_per_line))


def estimate_height(item: dict, bullet_size: int) -> float:
    """Rough height in points of the slide body, so dense slides get a smaller font."""
    paras = []  # (text, size, indent_pt, space_before)
    if item["kind"] == "agenda":
        paras.append((item["heading"], 18, 0, 0))
        paras += [(b, bullet_size, 27, 10) for b in item["bullets"]]
        paras += [("", bullet_size, 0, 10), (item["note"], 14, 0, 10)]
    else:
        for i, sec in enumerate(item["sections"]):
            if i:
                paras.append(("", bullet_size, 0, 10))
            paras.append((sec["heading"], 18, 0, 0 if i == 0 else 10))
            paras += [(b, bullet_size, 27, 10) for b in sec["bullets"]]
        for key in ("note", "callout"):
            if item.get(key):
                paras += [("", bullet_size, 0, 10), (item[key], 14, 0, 10)]
    total = 0.0
    for text, size, indent, before in paras:
        total += before + _lines(text, size, indent, body_box(item)[0]) * size * 1.08
    return total


def choose_bullet_size(item: dict) -> int:
    for size in (16, 15, 14, 13):
        if estimate_height(item, size) <= body_box(item)[1]:
            return size
    raise SystemExit(
        f"Slide '{item['title']}' (session {item['session']}) has too much text even at 13pt. "
        "Split it into two slides in deck_content.yaml."
    )


def _fill_body(body, item: dict) -> None:
    tf = body.text_frame
    first = True
    if item["kind"] == "agenda":
        size = choose_bullet_size(item)
        _add_para(tf, item["heading"], 18, True, NAVY, False, 0, first)
        for b in item["bullets"]:
            _add_para(tf, b, size, False, GREY, True, 10, False)
        _add_para(tf, "", size, False, GREY, False, 10, False)
        _add_para(tf, item["note"], 14, False, GREY, False, 10, False)
        return
    size = choose_bullet_size(item)
    for i, sec in enumerate(item["sections"]):
        if i:
            _add_para(tf, "", size, False, GREY, False, 10, False)
        _add_para(tf, sec["heading"], 18, True, NAVY, False, 0 if first else 10, first)
        first = False
        for b in sec["bullets"]:
            _add_para(tf, b, size, False, GREY, True, 10, False)
    if item.get("note"):
        _add_para(tf, "", size, False, GREY, False, 10, False)
        _add_para(tf, item["note"], 14, False, GREY, False, 10, False)
    if item.get("callout"):
        _add_para(tf, "", size, False, GREY, False, 10, False)
        _add_para(tf, item["callout"], 14, True, NAVY, False, 10, False)


def _place_image(slide, body, item: dict) -> None:
    from PIL import Image

    path = IMAGES_DIR / item["image"]
    iw, ih = Image.open(path).size
    left, top, full_w, full_h = body.left, body.top, body.width, body.height
    if item.get("image_position", "right") == "right":
        text_w = Pt(IMG_TEXT_WIDTH_PT + 10)
        body.left, body.top, body.width, body.height = left, top, text_w, full_h
        box_l, box_t, box_w, box_h = left + text_w + Pt(15), top, full_w - text_w - Pt(15), full_h
    else:
        text_h = Pt(IMG_BOTTOM_TEXT_HEIGHT_PT + 10)
        body.left, body.top, body.width, body.height = left, top, full_w, text_h
        box_l, box_t, box_w, box_h = left, top + text_h + Pt(5), full_w, full_h - text_h - Pt(5)
    scale = min(box_w / iw, box_h / ih)
    w, h = int(iw * scale), int(ih * scale)
    pic = slide.shapes.add_picture(str(path), box_l + (box_w - w) // 2, box_t + (box_h - h) // 2, w, h)
    pic.name = item["image"]
    pic._element.nvPicPr.cNvPr.set("descr", item["image_alt"])


def build_pptx(spec: dict, plan: list[dict], out: Path) -> None:
    prs = Presentation(str(TEMPLATE_FILE))
    files = {s["number"]: s["file"] for s in spec["sessions"]}
    for item in plan:
        k = item["kind"]
        slide = prs.slides.add_slide(prs.slide_layouts[{"title": 0, "section": 2}.get(k, 1)])
        if k in ("title", "section"):
            # Same explicit formatting as the SDE deck: white bold title, white (title slide) or cyan (section) subtitle
            title_size = 40 if k == "title" else 36
            sub_color = WHITE if k == "title" else CYAN
            _set_plain(slide.shapes.title, item["title"], title_size, True, WHITE)
            _set_plain(slide.placeholders[1], item["subtitle"], 18, False, sub_color)
        else:
            t = slide.shapes.title
            t.text_frame.text = item["title"]
            r = t.text_frame.paragraphs[0].runs[0]
            r.font.name, r.font.size, r.font.bold, r.font.color.rgb = FONT, Pt(28), True, NAVY
            body = slide.placeholders[1]
            _fill_body(body, item)
            if item.get("image"):
                _place_image(slide, body, item)
        if item["session"]:
            slide.notes_slide.notes_text_frame.text = f"Detail for this session: {files[item['session']]}"
    prs.core_properties.title = spec["deck"]["title"]
    prs.core_properties.author = "ABUHB Business Intelligence"
    prs.save(str(out))


def extract_pptx_texts(path: Path) -> list[list[str]]:
    prs = Presentation(str(path))
    result = []
    for slide in prs.slides:
        texts = []
        for shape in slide.placeholders:  # title first, then body, in placeholder order
            if shape.has_text_frame:
                texts += [p.text for p in shape.text_frame.paragraphs if p.text.strip()]
        texts += [f"[image:{sh.name}]" for sh in slide.shapes if sh.shape_type == 13]
        result.append(texts)
    return result


# --------------------------------------------------------------------------------------
# 3. Markdown
# --------------------------------------------------------------------------------------
def slide_markdown(item: dict) -> str:
    if item["kind"] == "section":
        return f"### Slide {item['number']}: Section divider\n\n**{item['title']}** — {item['subtitle']}\n"
    lines = [f"### Slide {item['number']}: {item['title']}", ""]
    for sec in item["sections"]:
        lines += [f"**{sec['heading']}**", ""]
        lines += [f"- {b}" for b in sec["bullets"]]
        lines.append("")
    if item.get("note"):
        lines += [f"> {item['note']}", ""]
    if item.get("callout"):
        lines += [f"**{item['callout']}**", ""]
    if item.get("image"):
        lines += [f"![{item['image_alt']}](images/{item['image']})", ""]
    return "\n".join(lines)


def session_block(spec: dict, plan: list[dict], number: int) -> str:
    items = [i for i in plan if i["session"] == number]
    first, last = items[0]["number"], items[-1]["number"]
    session = next(s for s in spec["sessions"] if s["number"] == number)
    head = (
        f"{BEGIN_MARK} - generated by Training/slides/build_deck.py from slides/deck_content.yaml. Do not edit by hand. -->\n"
        "## 🖥️ Slide Deck Content\n\n"
        f"These are the slides for this session: **slides {first}–{last}** of [`{DECK_NAME}`]({DECK_NAME}). "
        "They are generated from [`slides/deck_content.yaml`](slides/deck_content.yaml), so the deck and this page "
        "always match. The sections above give the full detail behind each slide.\n\n"
    )
    body = "\n".join(slide_markdown(i) for i in items)
    return f"{head}{body}\n{END_MARK}"


def _set_header(text: str, label: str, value: str) -> str:
    # Handles both "**Duration**: x" and "**Duration:** x"
    pat = re.compile(rf"^(\*\*{label}(?:\*\*:|:\*\*)\s*)(.*?)(\s*)$", re.M)
    return pat.sub(lambda m: f"{m.group(1)}{value}{m.group(3)}", text, count=1)


def sync_session_file(spec: dict, plan: list[dict], session: dict) -> tuple[Path, str | None]:
    path = REPO / session["file"]
    if not path.exists():
        raise SystemExit(f"Session file not found: {session['file']}")
    old = path.read_text(encoding="utf-8")
    new = _set_header(old, "Duration", session["duration"])
    new = _set_header(new, "Time", session["time"])
    total = len(spec["sessions"])
    new = re.sub(r"\*Session \d+ of \d+", f"*Session {session['number']} of {total}", new)
    block = session_block(spec, plan, session["number"])
    if BEGIN_MARK in new:
        new = re.sub(re.escape(BEGIN_MARK) + r".*?" + re.escape(END_MARK), lambda m: block, new, flags=re.S)
    else:
        m = re.search(r"\n---\s*\n+\*Session \d+ of \d+", new)
        if m:
            new = new[: m.start()] + f"\n---\n\n{block}\n" + new[m.start() :]
        else:
            new = new.rstrip() + f"\n\n---\n\n{block}\n"
    return path, (new if new != old else None)


def sessions_table(spec: dict, link_prefix: str) -> str:
    rows = ["| Session | Topic | Time | Duration | Focus |", "|---------|-------|------|----------|-------|"]
    for s in spec["sessions"]:
        link = s["file"][len(link_prefix) :] if link_prefix and s["file"].startswith(link_prefix) else s["file"]
        link = link.replace(" ", "%20")
        rows.append(f"| **{s['number']}** | [{s['title']}]({link}) | {s['time']} | {s['duration']} | {s['focus']} |")
    return (
        f"{TABLE_BEGIN} - generated by Training/slides/build_deck.py. Do not edit by hand. -->\n"
        + "\n".join(rows)
        + f"\n{TABLE_END}"
    )


def sync_readme(spec: dict, path: Path, link_prefix: str) -> str | None:
    old = path.read_text(encoding="utf-8")
    block = sessions_table(spec, link_prefix)
    if TABLE_BEGIN not in old:
        raise SystemExit(f"{path} is missing the {TABLE_BEGIN} ... {TABLE_END} markers")
    new = re.sub(re.escape(TABLE_BEGIN) + r".*?" + re.escape(TABLE_END), lambda m: block, old, flags=re.S)
    return new if new != old else None


PART_BEGIN = "<!-- CHECKPOINTS:BEGIN"
PART_END = "<!-- CHECKPOINTS:END -->"
PARTICIPANTS_README = REPO / "participants" / "README.md"


def checkpoints_table(spec: dict) -> str:
    rows = []
    for s in spec["sessions"]:
        ya = s.get("your_area")
        if ya:
            rows.append(f"| **{s['number']}** | {s['title']} | {ya['heading']} | {ya['checkpoint']} |")
    return (
        f"{PART_BEGIN} - generated by Training/slides/build_deck.py. Do not edit by hand. -->\n"
        "| Session | Topic | What you do | Your folder now contains |\n|---|---|---|---|\n"
        + "\n".join(rows)
        + f"\n{PART_END}"
    )


def sync_participants(spec: dict) -> str | None:
    old = PARTICIPANTS_README.read_text(encoding="utf-8")
    if PART_BEGIN not in old:
        raise SystemExit(f"{PARTICIPANTS_README} is missing the {PART_BEGIN} ... {PART_END} markers")
    block = checkpoints_table(spec)
    new = re.sub(re.escape(PART_BEGIN) + r".*?" + re.escape(PART_END), lambda m: block, old, flags=re.S)
    return new if new != old else None


# --------------------------------------------------------------------------------------
# 4. Main
# --------------------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="change nothing; exit 1 if the deck or markdown has drifted")
    args = ap.parse_args()

    spec = load_spec()
    plan = build_plan(spec)
    problems: list[str] = []

    # Deck
    expected = [plan_texts(i) for i in plan]
    if args.check:
        if not DECK_FILE.exists():
            problems.append(f"{DECK_NAME} is missing")
        else:
            actual = extract_pptx_texts(DECK_FILE)
            if len(actual) != len(expected):
                problems.append(f"{DECK_NAME} has {len(actual)} slides; the YAML defines {len(expected)}")
            for n, (a, e) in enumerate(zip(actual, expected), start=1):
                if a != e:
                    problems.append(f"{DECK_NAME} slide {n} text differs from the YAML ('{e[0]}')")
    else:
        build_pptx(spec, plan, DECK_FILE)
        print(f"Built {DECK_FILE.relative_to(REPO)} ({len(plan)} slides)")

    # Markdown
    changes: list[tuple[Path, str]] = []
    for s in spec["sessions"]:
        path, new = sync_session_file(spec, plan, s)
        if new is not None:
            changes.append((path, new))
    for path, prefix in ((REPO / "README.md", ""), (TRAINING / "README.md", "Training/")):
        new = sync_readme(spec, path, prefix)
        if new is not None:
            changes.append((path, new))

    new = sync_participants(spec)
    if new is not None:
        changes.append((PARTICIPANTS_README, new))

    # The custom agent is kept in two places (Copilot reads .github/agents/); they must be identical.
    pack_agent = REPO / "Participant_Pack" / "agents" / "senior-python-analyst.agent.md"
    gh_agent = REPO / ".github" / "agents" / "senior-python-analyst.agent.md"
    if pack_agent.exists() and gh_agent.exists() and pack_agent.read_bytes() != gh_agent.read_bytes():
        problems.append("The two copies of senior-python-analyst.agent.md differ (Participant_Pack/agents and .github/agents)")

    for path, new in changes:
        rel = path.relative_to(REPO)
        if args.check:
            problems.append(f"{rel} is out of sync with deck_content.yaml")
        else:
            path.write_text(new, encoding="utf-8")
            print(f"Updated {rel}")

    if args.check:
        if problems:
            print("DECK AND MARKDOWN ARE OUT OF SYNC:")
            for p in problems:
                print(f"  - {p}")
            print("Fix: edit Training/slides/deck_content.yaml, then run: python Training/slides/build_deck.py")
            return 1
        print(f"In sync: {len(plan)} slides, {len(spec['sessions'])} session files, 2 READMEs.")
    else:
        if not changes:
            print("Markdown already up to date.")
        # Re-verify what we just wrote
        if extract_pptx_texts(DECK_FILE) != expected:
            print("ERROR: built deck does not match the YAML", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
