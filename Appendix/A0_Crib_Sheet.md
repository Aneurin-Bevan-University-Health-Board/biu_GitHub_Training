# Git &Hub Crib Sheet

A quick reference for essential Git concepts and how to use with GitHub UI, GitHub, and VS Code.

---

## Concepts

- **Repository**: A folder tracked by Git. On Git, it's hosted online and accessible via web UI or desktop tools.
- ****: A saved snapshot of changes In GitHub Desktop/VS Code use the "Commit" button after writing message.
- **Branch**: separate line of development. Create,, and manage branches in GitHub UI Desktop, or VS Code.
-Merge**: Combine changes from one into another. Use Pull Requests (PR) in GitHub UI or merge Desktop/VS Code.
- ****: The online version of your repoe.g., on GitHub).

## Typical Workflow (GitHub UI Desktop / VS Code)

### 1 Clone a Repository

- **Git UI**: Click "Code" "Open with GitHub Desktop" or the URL.
- **GitHub**: "File" > " Repository" > paste URL.
- ** Code**: "Source Control" > "Clone Repository > paste URL.

### 2 Make Changes

- Edit files in your (VS Code).
- Changes appear "Changes" tab (Desktop/ Code).

### 3. Stage &

- **GitHub Desktop** Select files, enter a message, "Commit to main/branch".
-VS Code**: Stage files (), enter message, click "Commit- **GitHub UI**: For edits, use the web editor andCommit changes".

### 4. Changes

- **GitHub Desktop/ Code**: Click "Push origin to upload commits.
- **Git UI**: Changes are saved automatically for edits.

### 5. Branching- **GitHub Desktop**:Branch" menu > "New branch- **VS Code**: " Control" > "Create new branch".
 **GitHub UI**: "" dropdown > "New branch".

 6. Merging & Pull

- **GitHub UI**:Pull Requests" > "New Pull" to merge branches.
- **Hub Desktop/VS Code**: Switch target branch, merge from source branch or use "Create Pull Request".

### 7. Resolvinglicts

- **GitHub UI**: Conflicts shown PR; edit files in web editor- **Desktop/VS Code**:licts highlighted; edit, stage, commit resolved files.

---

## Useful

- **GitHub UI**: repo management, branching, PRs code review.
- **GitHub**: Visual tool for commits,, sync.
- **VS Code** Integrated Git support for editing, staging committing, branching.

---

## Advanced

- **Stash**: available in GitHub UI; use DesktopVS Code for "Stash changes (Desktop: "Repository" > "Stash").
- **Tagging**: UseHub UI "Releases" to create; Desktop/VS Code for advanced.
- **Cherry-pick** Advanced; use Desktop/VS Code "Cherry-pick commit".

---

## Practices

- Commit often with clear.
- Use branches for features/f.
- Open Pull Requests for code and merging.
- Sync (pull) pushing to avoid conflicts.
- Review before merging.

---

## Getting Help- **GitHub UI**: "" menu, documentation links.
-GitHub Desktop**: "Help > "GitHub Desktop Help".
 **VS Code**: "Help" "Git Documentation".

For more details visit [GitHub Docs](httpsdocs.github.com/) or [Git](https://git-scm.com/doc-+-+-+-+-+
---

## Common Git Commands

| Command                | Description                                                                 | Example Usage                       |
|------------------------|-----------------------------------------------------------------------------|-------------------------------------|
| `git init`             | Initialize a new Git repository                                             | `git init`                          |
| `git clone <url>`      | Clone a repository from a remote URL                                        | `git clone https://github.com/user/repo.git` |
| `git status`           | Show the working directory status                                           | `git status`                        |
| `git add <file>`       | Stage changes for commit                                                    | `git add README.md`                 |
| `git add .`            | Stage all changes in the directory                                          | `git add .`                         |
| `git commit -m "<msg>"`| Commit staged changes with a message                                        | `git commit -m "Initial commit"`    |
| `git log`              | View commit history                                                         | `git log`                           |
| `git diff`             | Show changes between commits, branches, or files                            | `git diff HEAD~1 HEAD`              |
| `git branch`           | List branches                                                               | `git branch`                        |
| `git branch <name>`    | Create a new branch                                                         | `git branch feature-xyz`            |
| `git checkout <name>`  | Switch to a branch                                                          | `git checkout main`                 |
| `git merge <branch>`   | Merge another branch into current                                           | `git merge feature-xyz`             |
| `git pull`             | Fetch and merge changes from remote                                         | `git pull`                          |
| `git push`             | Push local commits to remote                                                | `git push origin main`              |
| `git remote -v`        | List remote repositories                                                    | `git remote -v`                     |
| `git stash`            | Temporarily save changes                                                    | `git stash`                         |
| `git stash pop`        | Reapply stashed changes                                                     | `git stash pop`                     |
| `git tag <name>`       | Create a tag                                                                | `git tag v1.0.0`                    |
| `git cherry-pick <sha>`| Apply changes from a specific commit                                        | `git cherry-pick a1b2c3d`           |
| `git reset --hard <sha>`| Reset to a specific commit, discarding changes                             | `git reset --hard HEAD~1`           |
| `git rm <file>`        | Remove a file from the repository                                           | `git rm old.txt`                    |
| `git fetch`            | Download objects and refs from another repository                           | `git fetch origin`                  |
| `git rebase <branch>`  | Reapply commits on top of another base tip                                  | `git rebase main`                   |
| `git revert <sha>`     | Create a new commit that undoes changes from a previous commit              | `git revert a1b2c3d`                |

---

## GitHub UI & Desktop Actions

| Action                        | GitHub UI                           | GitHub Desktop                | VS Code                        |
|-------------------------------|-------------------------------------|-------------------------------|-------------------------------|
| Clone Repository              | "Code" > "Open with GitHub Desktop" | "File" > "Clone repository"   | "Source Control" > "Clone"    |
| Create Branch                 | "Branch" dropdown > "New branch"    | "Branch" > "New branch"       | "Source Control" > "Branch"   |
| Commit Changes                | Web editor > "Commit changes"       | Stage files, "Commit to..."   | Stage, enter message, "Commit"|
| Push Changes                  | N/A (auto for web edits)            | "Push origin"                 | "Push"                        |
| Pull Changes                  | N/A                                 | "Fetch origin"                | "Pull"                        |
| Open Pull Request             | "Pull Requests" > "New Pull Request"| "Create Pull Request"         | "Create Pull Request"         |
| Resolve Conflicts             | Edit in web editor                  | Edit, stage, commit           | Edit, stage, commit           |
| Stash Changes                 | N/A                                 | "Repository" > "Stash"        | "Stash" via command palette   |
| Tag/Release                   | "Releases" tab                      | "Repository" > "Tag"          | Git commands                  |
| Cherry-pick                   | N/A                                 | "Branch" > "Cherry-pick"      | Git commands                  |

---

## Example Git Workflow

1. **Clone**: `git clone <repo-url>`
2. **Create Branch**: `git checkout -b feature-branch`
3. **Edit Files**: Make changes in your editor.
4. **Stage Changes**: `git add .`
5. **Commit**: `git commit -m "Describe changes"`
6. **Push**: `git push origin feature-branch`
7. **Open Pull Request**: Use GitHub UI to merge changes.
8. **Resolve Conflicts**: Edit files, stage, commit, and push.
9. **Merge**: Complete PR to merge into main branch.

---

## Troubleshooting & Help

| Issue                | Solution/Command                      |
|----------------------|---------------------------------------|
| Untracked files      | `git add <file>`                      |
| Merge conflicts      | Edit files, `git add`, `git commit`   |
| Undo last commit     | `git reset --soft HEAD~1`             |
| Discard changes      | `git checkout -- <file>`              |
| Stash changes        | `git stash`                           |
| Restore stash        | `git stash pop`                       |
| View help            | `git help <command>`                  |

---

## Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [VS Code Git Guide](https://code.visualstudio.com/docs/sourcecontrol/git)

---