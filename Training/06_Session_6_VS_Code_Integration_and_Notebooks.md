![BIU Logo](../links%20and%20logos/BIU%20LOGO.png) ![DDAT Logo](../links%20and%20logos/DDAT%20Logo.png)

---

# Session 6: Using GitHub with VS Code (30‑Minute Overview)

**Duration:** 30 minutes  
**Time**: 12:45 - 13:15  
**Focus:** Practical essentials (not an exhaustive deep dive)

## Learning Objectives 

By the end you can:

1. Clone, branch, commit, and push using VS Code UI.  
2. Open and review pull requests without leaving VS Code.  
3. Understand when to use GitHub Codespaces vs local machine.  
4. Apply minimal notebook hygiene (clear outputs, avoid secrets).  
5. Follow core NHS Wales compliance & security considerations in tooling.

---

## Why VS Code + GitHub

| Need | Benefit |
|------|---------|
| Rapid context switching | Single window: code, issues, PRs, tasks |
| Consistent environments | Dev Containers / Codespaces reduce “works on my machine” |
| Traceability | Commits + PR reviews captured alongside code |
| Productivity | Integrated terminal, AI assistanc`e, linting |
| Governance | Easier enforcement of standards (templates, extensions) |

---

## 10 Minute Quick Start Workflow

```text
1. Open VS Code → Command Palette (ctr shift p): Git: Clone (paste repo URL)
2. Create feature branch: Source Control → ... → Create Branch (naming: feature/readmission-dashboard)
3. Make changes (code / notebook). Keep commits small (1 logical change).
4. Stage & commit: Source Control panel → + → Commit message: concise & reference issue (#123).
5. Push: Click “Sync Changes” (or “Publish Branch” first time).
6. Open PR: GitHub Pull Requests view → Create Pull Request → add reviewers & labels.
7. Address review comments directly in VS Code; iterate until approved.
8. Merge (or request maintainer) → Delete branch (optional). Pull latest main.
9. Archive local branches no longer needed.
10. Log work in issue / project board.
```

---

## Essential Panels & Commands

| Panel / Command | Purpose | Shortcut / Action |
|-----------------|---------|-------------------|
| Source Control | Stage, commit, diff | Ctrl+Shift+G |
| Pull Requests | Create & review PRs | GitHub view icon |
| Command Palette | All actions | Ctrl+Shift+P |
| Terminal | Run tests / scripts | Ctrl+` |
| Search | Codebase wide search | Ctrl+Shift+F |
| Timeline (GitLens) | Line/file history | Right‑click file → Open Timeline |

---

## Minimal Extension Set

| Extension | Why (30‑min scope) |
|-----------|--------------------|
| GitHub Pull Requests & Issues | PR & issue management inside VS Code |
| Python + Jupyter | Execute scripts & notebooks |
| GitHub Copilot (if licensed) | Accelerated boilerplate & doc strings |
|Github actions (optional) | View CI status in PRs |
|GitHub Codespaces (optional) | Seamless Codespace management |
Skip extra stylistic/productivity extensions for this session; introduce later.

---

## Codespaces vs Local: Decision Cheat Sheet

| Situation | Prefer Codespaces | Prefer Local |
|-----------|------------------|--------------|
| New joiner / onboarding | ✅ Prebuilt dev environment | ❌ Setup friction |
| Need identical tooling for review | ✅ Same container config | ❌ Risk of local drift |
| Heavy compute / large datasets | ❌ Resource cost / quotas | ✅ Local or dedicated VM |
| Intermittent network | ❌ Requires stable connection | ✅ Offline continuity |
| Secret management / least privilege | ✅ Scoped secrets, no local sprawl | ❌ Risk of local storage |

---

## Notebook Essentials (Keep Lightweight)

| Rule | Rationale |
|------|-----------|
| Clear outputs before commit | Avoid giant diffs / sensitive remnants |
| Parameterize paths (env vars) | Prevent hard‑coded local secrets |
| Use .gitignore for temp/output | Keep repo lean |
| Extract reusable logic to .py modules | Improves testability & reuse |
| Never commit real patient data | Compliance & governance |


Optional tooling later: pre-commit hooks (`nbstripout`) once basics are adopted.

---

## SQL in Git: Run the Academy Script

SQL is code, so it belongs in Git. In this session you copy a starter script into your own folder and run it against the **ndr-hb-abuhb-academy** Google Cloud project (dataset `SQL_Basic_Training`, table `referrals`).

- Script and steps: [`exercises/sql-basics/`](exercises/sql-basics/README.md)
- The script covers previewing a table with `LIMIT`, choosing named columns, and `SELECT DISTINCT`.
- BigQuery needs backticks round a table name that contains hyphens.
- Commit the SQL file only. Never commit query results, exports or screenshots of data.

---

## Compliance & Security (Top 8 Quick Checks)

1. No identifiable patient data pushed.  
2. Secrets stored in environment variables / GitHub secrets, not code.  
3. Use branch protection (review required).  
4. Descriptive commit messages referencing work items.  
5. Delete stale feature branches (reduces attack surface).  
6. Keep dependencies updated via scheduled PRs (Dependabot).  
7. Use devcontainer / Codespaces to standardise Python versions.  
8. Enable audit logging (GitHub org level) – verify periodically.

---

## Common Pitfalls & Fixes

| Pitfall | Quick Fix |
|---------|-----------|
| Huge notebook diffs | Clear outputs; modularize code |
| “Works locally only” | Adopt devcontainer / Codespaces |
| Forgotten branch merge | Use PR list & project board daily |
| Mixed environments (py 3.9 vs 3.11) | Pin `python` image & `requirements.txt` |
| Secret accidentally committed | Rotate credential; purge history (contact admin) |
| Slow reviews | Smaller PRs (<300 lines) + clear description |

---

## 14-Step Practical Exercise (Instructor Guided)

```text
1. Clone training repo.
2. Create branch: feature/vs-code-session6.
3. Modify your document added previously
4. Stage & commit (message: feat: add training bullet #ISSUE-ID).
5. Push branch.
6. Open PR in VS Code (assign reviewer).
7. View diff & add one inline comment (self-review).
8. Apply suggestion & commit from PR panel.
9. Mark PR ready for review.
10. Simulate reviewer approval (instructor).
11. Merge PR
12. Pull updated main locally.
13. Open Codespace (demonstrate identical state - Session 8 covers Codespaces hands-on).
14. Open notebook → clear outputs → commit hygiene.
```

---

##  Pointers for Further Depth (Out of Scope Today)

| Topic | Where Later |
|-------|-------------|
| Advanced GitLens analytics | Team deep-dive session |
| Pre-commit automation | Dev workflow workshop |
| CI/CD pipelines (Actions) | Session 7 (overview) & Ops docs |
| Environment reproducibility testing | DevContainers advanced module |
| AI pair programming standards | Session 8 and Appendix A1 |

---

## Recap

```text
You can now:
✅ Perform core Git operations in VS Code
✅ Open/review PRs without browser context switching
✅ Decide when to use Codespaces vs local
✅ Maintain lightweight, compliant notebooks
✅ Apply essential security & governance checks
```


---

## ▶ Next Session (7) Preview

Issues, Projects, Discussions – turning analytics work into traceable, prioritised delivery.

---

<!-- SLIDES:BEGIN - generated by Training/slides/build_deck.py from slides/deck_content.yaml. Do not edit by hand. -->
## 🖥️ Slide Deck Content

These are the slides for this session: **slides 42–48** of [`GitHub_Training_Day.pptx`](GitHub_Training_Day.pptx). They are generated from [`slides/deck_content.yaml`](slides/deck_content.yaml), so the deck and this page always match. The sections above give the full detail behind each slide.

### Slide 42: Section divider

**VS Code Integration and Notebooks** — Session 6 | 30 minutes

### Slide 43: Why VS Code + GitHub

**One window for everything**

- Code, issues and pull requests side by side
- Integrated terminal and linting
- Commits and reviews captured alongside the code
- Easier to enforce team standards

**Essential extensions**

- GitHub Pull Requests and Issues
- Python and Jupyter
- GitHub Copilot, if licensed

### Slide 44: Quick Start Workflow

**From clone to merge**

- Clone the repository and create a feature branch
- Make small changes, then stage and commit with a message referencing the issue
- Sync changes (or publish the branch the first time)
- Open the pull request from the GitHub Pull Requests view
- Address review comments, merge, then pull the latest main

### Slide 45: Notebook Hygiene and Security Checks

**Notebooks**

- Clear outputs before you commit
- Keep paths in environment variables, not code
- Move reusable logic into .py modules

**Top security checks**

- No identifiable patient data pushed
- Secrets in environment variables or GitHub secrets — never in code
- Branch protection with required reviews
- Keep dependencies updated

### Slide 46: Running SQL Against the Academy Dataset

**The ndr-hb-abuhb-academy project**

- A Google Cloud project for training, with a SQL_Basic_Training dataset
- Your SQL lives in Git as a file, so every change is tracked and reviewed

**Three habits from the script**

- Preview with SELECT * and always add LIMIT
- Name only the columns you need
- Use SELECT DISTINCT for a unique list of values

> BigQuery needs backticks round a table name with hyphens. Never commit results or data.

### Slide 47: Codespaces vs Local

**Prefer a Codespace when**

- Onboarding new joiners
- Reviewing with identical tooling
- You want least-privilege, scoped secrets

**Prefer local when**

- Working with heavy compute or large datasets
- The network is unreliable

> We try Codespaces hands-on in Session 8.

### Slide 48: Your Area: Checkpoint 6

**Add a clean notebook and your SQL (7 minutes)**

- Create starter.ipynb with one cell that prints a greeting, run it, then clear all outputs
- Copy Training/exercises/sql-basics/referrals_basics.sql into your folder as referrals.sql
- Run the queries in the BigQuery console, then change one and run it again
- Commit and push both files from the Source Control view

**Your folder now contains**

- starter.ipynb with outputs cleared, and referrals.sql, committed and pushed

<!-- SLIDES:END -->

---

*Session 6 of 9 | GitHub Training Series for Analytics and Data Teams*  
*Developed by ABUHB Business Intelligence Team*
