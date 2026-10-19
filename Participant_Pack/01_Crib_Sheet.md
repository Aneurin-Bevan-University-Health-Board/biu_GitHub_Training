# Crib Sheet

Keep this open all day. Replace `<your-folder>` with your folder name, for example `jerin-george`.

## The rules

- Synthetic data only. No patient data, no secrets, no tokens, anywhere.
- Work only in `participants/<your-folder>/`, on your branch `training/<your-folder>`.
- Never commit to `main`. Use a pull request.
- Read every Copilot suggestion before you accept it.

## Your workspace: Codespaces

| Task | How |
|------|-----|
| Open | Repository page, **Code → Codespaces → Create codespace on** your branch |
| Terminal | `` Ctrl+` `` |
| Command Palette | `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`) |
| Stop | Command Palette, **Codespaces: Stop Current Codespace** |
| Copilot Chat | Chat icon in the side bar, or `Ctrl+Alt+I` |

## Git commands

| I want to | Command |
|-----------|---------|
| See what changed | `git status` |
| Create and switch to my branch | `git switch -c training/<your-folder>` |
| Switch to an existing branch | `git switch training/<your-folder>` |
| Stage a file or folder | `git add participants/<your-folder>` |
| Commit | `git commit -m "Short, clear message"` |
| Push my branch | `git push` (first time: `git push -u origin HEAD`) |
| Bring in the latest main | `git pull origin main` |
| See history | `git log --oneline` |
| See my edits | `git diff` |
| Undo an unstaged edit to a file | `git restore <file>` |

**Good commit messages** say what and why: `Add DNA rate by speciality`, not `update`.

## Three places your files live

Working directory (you edit) → `git add` → staging area → `git commit` → repository → `git push` → GitHub.

## Pull requests

1. Push your branch. 2. On github.com choose **Compare and pull request**. 3. Write what you did and `Closes #<issue number>`. 4. Ask for a review. 5. Merge when approved.

## Merge conflict

You see `<<<<<<<`, `=======`, `>>>>>>>` in a file. Edit the file so it holds the lines you want, delete the three marker lines, test, then `git add` and `git commit`.

## `.gitignore`

Lists files Git must never track, one pattern per line: `*.csv`, `data/`, `outputs/`, `.env`. Already tracked a file by mistake? Tell the trainer. Do not just delete it, because history keeps it.

## GitHub on the web

Tabs: **Code**, **Issues**, **Pull requests**, **Actions**, **Projects**, **Security**, **Insights**. Press `.` on a repository for the web editor, `t` to find a file, `/` to search.

## Issues

Title says the problem. Body has context, definition of done and acceptance criteria. Link it from a pull request with `Closes #12`.

## Advanced Security (Session 7)

- Push protection blocks a secret before it reaches GitHub.
- Code scanning and dependency review check pull requests.
- **If a secret is ever pushed: revoke it first**, tell the admin team, then clean up. Deleting the line is not enough.

## SQL basics (BigQuery, optional)

| Idea | Example |
|------|---------|
| Preview | `SELECT * FROM `ndr-hb-abuhb-academy.SQL_Basic_Training.referrals` LIMIT 100;` |
| Choose columns | `SELECT division_current, fy FROM ...` |
| Unique values | `SELECT DISTINCT division_current FROM ...` |
| Count by group | `SELECT division_current, COUNT(*) AS referrals FROM ... GROUP BY division_current` |

Always add `LIMIT` while exploring. Backticks are needed round names with hyphens.

## Copilot prompts that work

- "Explain this code line by line."
- "Write a function that loads the CSV with pandas and checks for duplicate IDs and missing values."
- "What assumptions does this code make about the data?"
- "Write a pytest test for this function."
- "Make the chart title and labels clear, in UK English."

Ask for **small steps**. Say what you want, what the columns mean and what the metric definition is.

## Who to ask

Your trainer first. GitHub admin team: `ABB.BIU.GitHub.Admin@nhswales365.onmicrosoft.com`.
