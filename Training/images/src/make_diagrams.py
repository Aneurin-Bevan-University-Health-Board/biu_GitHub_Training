#!/usr/bin/env python3
"""Generate the training diagrams as PNG files (Training/images/*.png).

    pip install cairosvg
    python Training/images/src/make_diagrams.py

Each diagram is drawn as SVG (also saved in Training/images/src/svg/) and rendered to PNG.
Change the drawing code here, re-run it, then run  python Training/slides/build_deck.py  to refresh the deck.
"""

from pathlib import Path
from xml.sax.saxutils import escape

import cairosvg

HERE = Path(__file__).resolve().parent
PNG_DIR = HERE.parent
SVG_DIR = HERE / "svg"

NAVY, GREY, CYAN = "#002060", "#44546A", "#01B0FF"
LIGHT, MID, WHITE = "#EAF1FB", "#C9D9F0", "#FFFFFF"
GREEN, AMBER, RED = "#2E8B57", "#E07B00", "#C0392B"
FONT = "Arial, Helvetica, 'Liberation Sans', FreeSans, 'DejaVu Sans', sans-serif"


class Canvas:
    def __init__(self, w, h):
        self.w, self.h, self.parts = w, h, []

    # -- primitives -------------------------------------------------------------------
    def text(self, x, y, s, size=26, color=GREY, bold=False, anchor="middle", mono=False):
        fam = "'DejaVu Sans Mono', Menlo, Consolas, monospace" if mono else FONT
        wt = "bold" if bold else "normal"
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{wt}" '
            f'fill="{color}" text-anchor="{anchor}">{escape(s)}</text>'
        )

    def lines(self, x, y, lines, size=26, color=GREY, bold=False, anchor="middle", gap=1.35, mono=False):
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * gap, ln, size, color, bold, anchor, mono)

    def box(self, x, y, w, h, lines=(), fill=LIGHT, stroke=NAVY, color=NAVY, size=26, bold=True, r=14, dash=False, sw=3, mono=False):
        d = ' stroke-dasharray="12 8"' if dash else ""
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )
        if lines:
            n = len(lines)
            top = y + h / 2 - (n - 1) * size * 1.35 / 2 + size * 0.35
            self.lines(x + w / 2, top, lines, size, color, bold, mono=mono)

    def arrow(self, x1, y1, x2, y2, color=NAVY, sw=5, dash=False, head=True):
        d = ' stroke-dasharray="14 9"' if dash else ""
        m = f' marker-end="url(#h{color[1:]})"' if head else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}{m}/>')

    def path(self, d, color=NAVY, sw=5, dash=False, head=True, fill="none"):
        dd = ' stroke-dasharray="14 9"' if dash else ""
        m = f' marker-end="url(#h{color[1:]})"' if head else ""
        self.parts.append(f'<path d="{d}" stroke="{color}" stroke-width="{sw}" fill="{fill}"{dd}{m}/>')

    def circle(self, cx, cy, r, fill=NAVY, stroke=NAVY):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')

    def pill(self, x, y, w, h, s, fill=CYAN, color=WHITE, size=22):
        self.box(x, y, w, h, [s], fill=fill, stroke=fill, color=color, size=size, r=h / 2, sw=0)

    # -- output -----------------------------------------------------------------------
    def svg(self):
        heads = "".join(
            f'<marker id="h{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for c in (NAVY, GREY, CYAN, GREEN, AMBER, RED)
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
            f"<defs>{heads}</defs><rect width=\"100%\" height=\"100%\" fill=\"white\"/>" + "".join(self.parts) + "</svg>"
        )

    def save(self, name):
        SVG_DIR.mkdir(parents=True, exist_ok=True)
        svg = self.svg()
        (SVG_DIR / f"{name}.svg").write_text(svg, encoding="utf-8")
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(PNG_DIR / f"{name}.png"), output_width=self.w)
        print("wrote", name)


# ======================================================================================
def three_trees():
    c = Canvas(1200, 780)
    c.text(600, 60, "Where your files live in GIT", 36, NAVY, True)
    xs = [50, 460, 870]
    heads = ["Working directory", "Staging area", "Repository"]
    subs = ["(your files)", "(the index)", "(committed history)"]
    for x, h, s in zip(xs, heads, subs):
        c.box(x, 130, 280, 210, [h, s], fill=LIGHT, size=28)
    c.arrow(332, 260, 458, 260)
    c.arrow(742, 260, 868, 260)
    c.text(395, 215, "git add", 24, NAVY, True, mono=True)
    c.text(805, 215, "git commit", 24, NAVY, True, mono=True)
    c.path("M 1010 345 C 1010 470, 190 470, 190 348", color=GREY, dash=True)
    c.text(600, 505, "git restore / git checkout", 26, GREY, True, mono=True)
    for x, st, col in zip(xs, ["Modified", "Staged", "Committed"], [AMBER, CYAN, GREEN]):
        c.pill(x + 40, 570, 200, 56, st, fill=col, size=28)
    c.text(600, 690, "A file moves left to right as you work:", 28, GREY, False)
    c.text(600, 735, "edit it  \u2192  choose what to include  \u2192  save a snapshot", 28, NAVY, True)
    c.save("three_trees")


def sync_flow():
    c = Canvas(1200, 900)
    c.box(30, 80, 560, 700, fill=WHITE, stroke=GREY, dash=True, r=22)
    c.text(310, 130, "Your computer", 32, GREY, True)
    c.box(110, 175, 400, 120, ["Working directory"], size=30)
    c.box(110, 365, 400, 120, ["Staging area"], size=30)
    c.box(110, 555, 400, 120, ["Local repository"], size=30)
    c.arrow(310, 297, 310, 363)
    c.arrow(310, 487, 310, 553)
    c.text(335, 340, "git add", 24, NAVY, True, "start", mono=True)
    c.text(335, 530, "git commit", 24, NAVY, True, "start", mono=True)
    c.box(780, 175, 390, 500, ["GitHub", "(origin)"], fill=NAVY, stroke=NAVY, color=WHITE, size=40)
    c.arrow(776, 235, 514, 235, color=AMBER)
    c.text(645, 205, "git pull", 26, AMBER, True, mono=True)
    c.text(645, 270, "(fetch + merge)", 22, AMBER)
    c.arrow(776, 590, 514, 590, color=GREEN)
    c.text(645, 565, "git fetch", 26, GREEN, True, mono=True)
    c.arrow(514, 650, 776, 650, color=CYAN)
    c.text(645, 700, "git push", 26, CYAN, True, mono=True)
    c.text(975, 730, "git clone = first-time copy", 24, NAVY, True)
    c.text(600, 840, "Push shares your work. Pull and fetch bring in your colleagues' work.", 26, NAVY, True)
    c.save("sync_flow")


def branch_merge():
    c = Canvas(1200, 800)
    c.text(600, 55, "Branch, review, merge", 36, NAVY, True)
    y_main, y_feat = 260, 520
    c.text(60, y_main - 40, "main (protected)", 28, NAVY, True, "start")
    c.arrow(60, y_main, 1150, y_main, color=NAVY, sw=7)
    for x in (140, 300, 460, 840, 1000):
        c.circle(x, y_main, 18)
    c.text(300, y_main + 60, "stable, reviewed code", 22, GREY)
    c.path(f"M 460 {y_main} C 520 {y_main}, 540 {y_feat}, 600 {y_feat}", color=CYAN, sw=6, head=False)
    c.text(520, y_feat + 90, "feature/your-name-area", 28, CYAN, True, "start")
    c.arrow(600, y_feat, 760, y_feat, color=CYAN, sw=6, head=False)
    for x in (600, 680, 760):
        c.circle(x, y_feat, 16, fill=CYAN, stroke=CYAN)
    c.text(680, y_feat - 36, "your commits", 22, GREY)
    c.path(f"M 760 {y_feat} C 820 {y_feat}, 790 {y_main + 40}, 840 {y_main}", color=CYAN, sw=6)
    c.box(800, 380, 330, 95, ["Pull request", "review + checks"], fill=WHITE, stroke=GREEN, color=GREEN, size=26)
    c.circle(840, y_main, 20, fill=GREEN, stroke=GREEN)
    c.text(840, y_main - 40, "merge", 24, GREEN, True)
    c.text(600, 720, "Your changes affect no one until the pull request is merged.", 28, NAVY, True)
    c.save("branch_merge")


def conflict():
    c = Canvas(1200, 900)
    c.text(600, 55, "A merge conflict, and how to resolve it", 36, NAVY, True)
    c.box(40, 100, 530, 120, ["Analyst A changes line 1:", "SELECT patient_id, age"], fill=LIGHT, size=24, bold=False)
    c.box(630, 100, 530, 120, ["Analyst B changes line 1:", "SELECT patient_id, age, gender"], fill=LIGHT, size=24, bold=False)
    c.arrow(305, 224, 305, 328, color=GREY)
    c.arrow(895, 224, 895, 328, color=GREY)
    c.text(600, 285, "same line, so GIT can't choose", 26, AMBER, True)
    c.box(140, 335, 920, 260, fill="#1E1E2E", stroke="#1E1E2E")
    code = [
        ("<<<<<<< HEAD", AMBER),
        ("SELECT patient_id, age", WHITE),
        ("=======", AMBER),
        ("SELECT patient_id, age, gender", WHITE),
        (">>>>>>> feature/add-gender", AMBER),
    ]
    for i, (ln, col) in enumerate(code):
        c.text(180, 395 + i * 44, ln, 28, col, False, "start", mono=True)
    steps = ["1  Edit the\nmarkers", "2  Test the\nquery", "3  Validate\nresults", "4  Commit the\nresolution"]
    for i, s in enumerate(steps):
        x = 40 + i * 295
        c.box(x, 650, 270, 120, s.split("\n"), fill=WHITE, stroke=GREEN, color=GREEN, size=26)
        if i < 3:
            c.arrow(x + 272, 710, x + 293, 710, color=GREEN)
    c.text(600, 845, "Prevent conflicts: pull often and keep branches short-lived.", 28, NAVY, True)
    c.save("conflict")


def object_model():
    c = Canvas(1200, 860)
    c.text(600, 55, "How GIT stores a snapshot", 36, NAVY, True)
    c.box(430, 100, 340, 150, ["Commit", "a3b5c8d", "author \u00b7 date \u00b7 message"], fill=NAVY, color=WHITE, stroke=NAVY, size=26)
    c.box(430, 320, 340, 110, ["Tree", "(project root)"], size=28)
    c.arrow(600, 252, 600, 318)
    c.box(60, 520, 300, 100, ["Blob", "README.md"], fill=WHITE, size=26)
    c.box(450, 520, 300, 100, ["Tree", "sql/"], size=26)
    c.box(840, 520, 300, 100, ["Blob", "notes.md"], fill=WHITE, size=26)
    c.arrow(540, 432, 210, 518)
    c.arrow(600, 432, 600, 518)
    c.arrow(660, 432, 990, 518)
    c.box(450, 700, 300, 100, ["Blob", "extract.sql"], fill=WHITE, size=26)
    c.arrow(600, 622, 600, 698)
    c.box(880, 120, 280, 110, ["Parent commit", "9f2e1a0"], fill=WHITE, stroke=GREY, color=GREY, size=24)
    c.arrow(772, 175, 878, 175, color=GREY)
    c.text(40, 160, "Each object is named by", 22, GREY, False, "start")
    c.text(40, 190, "a SHA-1 hash of its content.", 22, GREY, False, "start")
    c.text(40, 220, "Change a byte,", 22, NAVY, True, "start")
    c.text(40, 250, "change the hash.", 22, NAVY, True, "start")
    c.save("object_model")


def lifecycle():
    c = Canvas(1300, 330)
    steps = ["Issue", "Branch", "Commits", "Pull\nrequest", "Review", "Merge", "Issue\nclosed"]
    w, gap = 156, 26
    for i, s in enumerate(steps):
        x = 26 + i * (w + gap)
        fill = NAVY if i in (0, 6) else LIGHT
        col = WHITE if i in (0, 6) else NAVY
        c.box(x, 60, w, 130, s.split("\n"), fill=fill, color=col, size=28)
        if i < 6:
            c.arrow(x + w + 2, 125, x + w + gap - 2, 125)
    c.text(650, 255, "Every change links back to the reason it was made.", 28, NAVY, True)
    c.text(650, 300, "Tip: write \u201ccloses #12\u201d in your commit message.", 24, GREY)
    c.save("lifecycle")


def repo_mock():
    c = Canvas(1200, 820)
    c.box(20, 20, 1160, 780, fill=WHITE, stroke=GREY, r=18, sw=3)
    c.text(60, 85, "ABUHB / biu-training", 34, NAVY, True, "start")
    c.pill(520, 55, 100, 42, "Private", fill=MID, color=NAVY, size=22)
    tabs = ["Code", "Issues", "Pull requests", "Actions", "Projects", "Security", "Insights"]
    x = 45
    for i, t in enumerate(tabs):
        w = 20 + len(t) * 13
        if i == 0:
            c.box(x - 8, 120, w + 16, 52, [t], fill=LIGHT, stroke=NAVY, color=NAVY, size=22, r=10)
        else:
            c.text(x + w / 2, 154, t, 22, GREY, False)
        x += w + 22
    c.parts.append(f'<line x1="40" y1="180" x2="1160" y2="180" stroke="{MID}" stroke-width="3"/>')
    rows = [("participants", "Your personal areas", True), ("Training", "Session notes and slides", True), ("README.md", "Start here", False), (".gitignore", "Files to keep out", False)]
    c.box(50, 215, 740, 400, fill=WHITE, stroke=MID)
    for i, (n, d, folder) in enumerate(rows):
        y = 270 + i * 90
        c.box(75, y - 20, 28, 22 if folder else 28, fill=NAVY if folder else MID, stroke=NAVY if folder else GREY, r=3, sw=2)
        c.text(125, y, n, 26, NAVY, True, "start")
        c.text(450, y, d, 22, GREY, False, "start")
        if i < 3:
            c.parts.append(f'<line x1="50" y1="{y + 40}" x2="790" y2="{y + 40}" stroke="{MID}" stroke-width="2"/>')
    c.box(820, 215, 330, 400, fill=LIGHT, stroke=MID)
    c.text(985, 265, "About", 28, NAVY, True)
    c.lines(985, 320, ["Training repository", "for the GitHub", "training day"], 22, GREY, False)
    c.pill(850, 470, 270, 44, "Branch: main", fill=NAVY, size=22)
    c.pill(850, 530, 270, 44, "Pull requests: 3", fill=CYAN, size=22)
    c.text(600, 690, "Code \u00b7 Issues \u00b7 Pull requests \u00b7 Actions \u00b7 Projects \u00b7 Security \u00b7 Insights", 24, GREY)
    c.text(600, 740, "Illustration: the live GitHub interface looks similar.", 22, GREY)
    c.save("repo_mock")


def lfs():
    c = Canvas(1200, 820)
    c.text(600, 55, "Git LFS: pointers in Git, big files elsewhere", 34, NAVY, True)
    c.box(40, 120, 520, 520, fill=WHITE, stroke=GREY, dash=True, r=20)
    c.text(300, 170, "Your repository", 30, GREY, True)
    c.box(80, 210, 440, 100, ["analysis.py"], fill=LIGHT, size=26)
    c.box(80, 340, 440, 260, fill=LIGHT, stroke=NAVY)
    c.text(300, 385, "model.pkl  (pointer file)", 24, NAVY, True)
    for i, ln in enumerate(["version git-lfs spec v1", "oid sha256:4d7a21...", "size 52428800"]):
        c.text(110, 445 + i * 48, ln, 22, GREY, False, "start", mono=True)
    c.box(660, 120, 500, 520, fill=NAVY, stroke=NAVY)
    c.text(910, 175, "LFS storage", 32, WHITE, True)
    c.box(700, 230, 420, 110, ["model.pkl", "50 MB"], fill=WHITE, size=26)
    c.box(700, 380, 420, 110, ["reference.parquet", "120 MB"], fill=WHITE, size=26)
    c.arrow(522, 440, 698, 300, color=CYAN)
    c.text(560, 395, "points to", 24, CYAN, True)
    c.text(600, 715, "Small and fast to clone, but only for approved reference data.", 26, NAVY, True)
    c.text(600, 760, "LFS never makes patient data safe to commit.", 26, RED, True)
    c.save("lfs")


def kanban():
    c = Canvas(1200, 820)
    c.text(600, 55, "A simple project board", 36, NAVY, True)
    cols = [("Backlog", MID), ("In Progress", CYAN), ("Review", AMBER), ("Blocked", RED), ("Done", GREEN)]
    cards = {
        0: ["Add DNA chart", "Data quality\nchecks"],
        1: ["Update\nREADME"],
        2: ["Refactor SQL"],
        3: ["Waiting for\nextract access"],
        4: ["Fix typo", "Add .gitignore"],
    }
    w = 218
    for i, (name, col) in enumerate(cols):
        x = 20 + i * (w + 22)
        c.box(x, 100, w, 600, fill="#F5F8FC", stroke=MID, r=12, sw=2)
        c.box(x, 100, w, 64, [name], fill=col, stroke=col, color=WHITE if col != MID else NAVY, size=26, r=12)
        for j, cd in enumerate(cards.get(i, [])):
            c.box(x + 14, 190 + j * 130, w - 28, 105, cd.split("\n"), fill=WHITE, stroke=MID, color=NAVY, size=22, bold=False, r=8, sw=2)
    c.text(600, 765, "Each card is an issue. A merged pull request moves its issue to Done.", 26, NAVY, True)
    c.save("kanban")


def codespace_arch():
    c = Canvas(1200, 900)
    c.box(30, 40, 340, 300, ["Your browser", "(VS Code)"], fill=LIGHT, size=32)
    c.text(200, 270, "Any device", 24, GREY)
    c.box(470, 40, 700, 560, fill=WHITE, stroke=GREY, dash=True, r=22)
    c.text(820, 90, "Your Codespace (GitHub cloud)", 30, GREY, True)
    c.box(510, 130, 300, 100, ["Terminal"], size=26)
    c.box(850, 130, 280, 100, ["Editor"], size=26)
    c.box(510, 260, 620, 100, ["Python 3.11 \u00b7 pandas \u00b7 Streamlit"], size=26)
    c.box(510, 390, 620, 100, ["Extensions: Copilot, Pull Requests"], size=26)
    c.box(510, 520, 620, 60, ["Your branch of the repository"], fill=NAVY, color=WHITE, size=24)
    c.arrow(372, 190, 468, 190, color=CYAN)
    c.arrow(468, 230, 372, 230, color=CYAN)
    c.box(30, 650, 440, 180, [".devcontainer/", "devcontainer.json"], fill=WHITE, size=28, mono=True)
    c.text(250, 865, "defines the environment, stored in the repo", 22, GREY)
    c.path("M 472 720 C 600 720, 640 690, 640 604", color=NAVY, dash=True)
    c.text(560, 760, "builds", 26, NAVY, True)
    c.box(760, 680, 410, 150, ["GitHub repository"], fill=NAVY, color=WHITE, stroke=NAVY, size=30)
    c.arrow(1000, 604, 1000, 678, color=CYAN)
    c.text(1020, 650, "commit + push", 24, CYAN, True, "start")
    c.save("codespace_arch")


def sde_fit():
    c = Canvas(1200, 900)
    c.box(20, 40, 520, 700, fill=LIGHT, stroke=NAVY, r=20)
    c.text(280, 95, "GitHub + Codespaces", 32, NAVY, True)
    c.text(280, 135, "GitHub's cloud", 24, GREY)
    for i, t in enumerate(["Code and reviews", "Documentation", "Synthetic data", "Copilot"]):
        c.box(60, 175 + i * 130, 440, 100, [t], fill=WHITE, size=28)
    c.box(660, 40, 520, 700, fill=NAVY, stroke=NAVY, r=20)
    c.text(920, 95, "Secure Data Environment", 32, WHITE, True)
    c.text(920, 135, "Google Cloud Platform", 24, MID)
    for i, t in enumerate(["BigQuery", "Python notebooks", "Real patient data", "Looker + Data Studio"]):
        c.box(700, 175 + i * 130, 440, 100, [t], fill=WHITE, size=28)
    c.arrow(545, 300, 655, 300, color=GREEN, sw=8)
    c.text(600, 270, "reviewed", 20, GREEN, True)
    c.text(600, 340, "code", 20, GREEN, True)
    c.arrow(655, 520, 545, 520, color=RED, sw=8, dash=True)
    c.text(600, 490, "no real", 20, RED, True)
    c.text(600, 565, "data", 20, RED, True)
    c.text(600, 810, "Code moves to the data. Data never moves to the code.", 32, NAVY, True)
    c.save("sde_fit")


def repo_area():
    c = Canvas(1200, 820)
    c.text(600, 55, "Your area in the training repository", 34, NAVY, True)
    c.box(40, 100, 1120, 660, fill=WHITE, stroke=MID, r=16, sw=2)

    def row(x, y, label, note="", hl=False, folder=True):
        if hl:
            c.box(x - 15, y - 34, 760, 52, fill=LIGHT, stroke=CYAN, r=8, sw=2)
        c.text(x, y, ("▶ " if folder else "■ ") + label, 26, NAVY if not hl else NAVY, True, "start", mono=True)
        if note:
            c.text(x + 520, y, note, 22, GREY, False, "start")

    row(80, 160, "participants/", "everyone's areas", folder=True)
    row(130, 220, "_template/", "copy this to start")
    row(130, 280, "shared-notes.md", "for the conflict drill", folder=False)
    row(130, 350, "firstname-lastname/", "YOUR area", hl=True)
    for i, (n, d) in enumerate([("README.md", "Session 2"), (".gitignore", "Session 3"), ("notes.md", "Session 5"), ("starter.ipynb", "Session 6"), ("requirements.txt", "Session 7"), ("dna-analysis/", "Session 8")]):
        row(190, 405 + i * 48, n, d, folder=n.endswith("/"))
    row(80, 715, "Training/  ·  Appendix/  ·  README.md", "")
    c.save("repo_area")


def security_pipeline():
    c = Canvas(1200, 900)
    c.text(600, 50, "Security checks along the way", 34, NAVY, True)
    stages = [
        ("1  You write code", ["Keep secrets out of code"]),
        ("2  You push", ["Push protection", "blocks secrets"]),
        ("3  Pull request", ["Code scanning (CodeQL)", "Dependency review"]),
        ("4  After merge", ["Secret scanning", "Dependabot alerts"]),
    ]
    for i, (s, chips) in enumerate(stages):
        y = 100 + i * 200
        c.box(30, y, 420, 130, [s], fill=NAVY if i == 0 else LIGHT, color=WHITE if i == 0 else NAVY, size=30)
        if i < 3:
            c.arrow(240, y + 134, 240, y + 196)
        for j, ch in enumerate(chips):
            off = 0 if len(chips) > 1 else 35
            c.box(560, y + 3 + j * 68 + off, 600, 60, [ch], fill=WHITE, stroke=GREEN, color=GREEN, size=26, r=30)
        c.arrow(452, y + 65, 556, y + 65, color=GREEN)
    c.text(600, 880, "Alerts appear in your repository's Security tab.", 26, GREY)
    c.save("security_pipeline")


if __name__ == "__main__":
    for fn in (three_trees, sync_flow, branch_merge, conflict, object_model, lifecycle, repo_mock, lfs, kanban, codespace_arch, sde_fit, repo_area, security_pipeline):
        fn()
