# Session 2: Basic GitHub Concepts

**Duration**: 30 minutes  
**Time**: 09:30 - 10:00

## 🎯 Learning Objectives

By the end of this session, you will understand:
- How commits work and why they matter
- Branching strategies and best practices
- Pull requests and the code review process
- Forking and different collaboration models
- Merging and resolving conflicts

---

## Understanding Commits

### What is a Commit?

A **commit** is a snapshot of your project at a specific point in time. Think of it as a save point in a video game - you can always return to this exact state.

### Anatomy of a Commit

```bash
commit 3907327b003c6b28e96d981a2e6aac38d45be87a
Author: John Smith <john.smith@wales.nhs.uk>
Date:   Mon Oct 9 10:30:45 2024 +0100

    Add repository naming convention documentation
    
    - Created comprehensive naming guidelines
    - Added prefix directory for departments
    - Included examples for BIU and PHN teams
```

### Key Components

| Component | Description | Example |
|-----------|-------------|---------|
| **SHA Hash** | Unique identifier (40 characters) | `3907327b003c6b...` |
| **Author** | Who made the changes | John Smith |
| **Date** | When the commit was created | Mon Oct 9 10:30:45 2024 |
| **Message** | Description of what changed | "Add naming convention docs" |
| **Changes** | The actual file modifications | Lines added/removed |

### Writing Good Commit Messages

#### ✅ Good Examples
```
Add user authentication module

Fix bug in date calculation for reporting
- Corrected timezone handling
- Added unit tests for edge cases

Update dependencies to resolve security vulnerabilities
- Updated lodash to 4.17.21
- Updated axios to 1.6.0
```

#### ❌ Bad Examples
```
fixed stuff
WIP
asdfasdf
Updated files
```

### Best Practices for Commits

1. **Commit Often**: Small, frequent commits are better than large, rare ones
2. **Atomic Commits**: Each commit should represent one logical change
3. **Clear Messages**: Describe what and why, not how
4. **Present Tense**: "Add feature" not "Added feature"
5. **Reference Issues**: Include issue numbers when relevant (e.g., "Fixes #123")

---

## Branching

### What is a Branch?

A **branch** is a parallel version of your repository. It allows you to work on features or fixes without affecting the main codebase.

### The Main Branch

```
main ──●──●──●──●──●──●──●──►
       Initial commits continue here
```

The `main` branch (formerly `master`) is the primary branch where production-ready code lives.

### Creating Feature Branches

```
main ──●──●──●──────────●──●──►
            \          /
feature ─────●──●──●──●
             Work on new feature
```

### Common Branch Types

| Branch Type | Purpose | Example Name | Lifetime |
|-------------|---------|--------------|----------|
| **Main** | Production code | `main` | Permanent |
| **Feature** | New functionality | `feature/user-login` | Temporary |
| **Bugfix** | Fix defects | `bugfix/date-calculation` | Temporary |
| **Hotfix** | Urgent production fixes | `hotfix/security-patch` | Temporary |
| **Release** | Release preparation | `release/v2.1.0` | Temporary |
| **Development** | Integration branch | `develop` | Permanent (optional) |

### Branching Commands

```bash
# Create a new branch
git branch feature/new-dashboard

# Switch to the branch
git checkout feature/new-dashboard

# Create and switch in one command
git checkout -b feature/new-dashboard

# List all branches
git branch -a

# Delete a branch (locally)
git branch -d feature/old-feature

# Push branch to remote
git push origin feature/new-dashboard
```

### Branching Strategies

#### 1. **GitHub Flow** (Simple - Recommended for Most Teams)
```
main ──●──●──────────●──●──────────●──►
            \       /     \       /
             ●──●──●       ●──●──●
           feature-1     feature-2
```

- Only one permanent branch (`main`)
- Create feature branches for work
- Merge back to main frequently
- Deploy from main

#### 2. **Git Flow** (Complex - For Larger Projects)
```
main ──────●───────────────●──────────►
            \             /
develop ─────●──●──●──●──●──●──────────►
              \     /  \    /
               ●───●    ●──●
             feature  bugfix
```

- Two permanent branches: `main` and `develop`
- Feature branches off `develop`
- Release branches for preparation
- Hotfix branches off `main`

#### 3. **Trunk-Based Development** (Fast-Paced Teams)
```
main ──●──●──●──●──●──●──●──●──●──●──►
        \  /  \  /  \  /
         ●●    ●●    ●●
     Short-lived feature branches
```

- Very short-lived branches (hours to 1-2 days)
- Frequent integration to main
- Feature flags for incomplete work
- Requires strong CI/CD pipeline

### ABB Recommended Approach

For ABB projects, we recommend **GitHub Flow**:
- Simple and easy to understand
- Encourages frequent integration
- Works well with GitHub's pull request workflow
- Suitable for most team sizes

---

## Pull Requests (PRs)

### What is a Pull Request?

A **pull request** is a proposal to merge changes from one branch into another. It's GitHub's mechanism for code review and collaboration.

### The Pull Request Process

```
1. Developer                2. Create PR          3. Review
   creates branch              on GitHub             process
        │                          │                    │
        ▼                          ▼                    ▼
   ●──●──●                   ╔══════════╗         👤 Reviewer 1: ✅
feature branch               ║   Pull   ║         👤 Reviewer 2: 💬
                             ║  Request ║         👤 Reviewer 3: ✅
                             ╚══════════╝              │
                                  │                    ▼
                                  └────────►  4. Merge to main
                                                      ●
```

### Anatomy of a Pull Request

#### 1. **Title**
```
Add patient appointment scheduling feature
```
Clear, concise description of the change

#### 2. **Description**
```markdown
## Description
This PR adds a new scheduling system for patient appointments.

## Changes
- Added appointment booking API endpoints
- Created scheduling UI components
- Implemented calendar integration

## Testing
- Unit tests for API endpoints
- Manual testing of UI workflows
- Tested with 100+ sample appointments

## Related Issues
Closes #234
Related to #189
```

#### 3. **Files Changed**
Shows all modified files with line-by-line differences

#### 4. **Conversation**
Comments, questions, and discussions about the changes

#### 5. **Checks**
Automated tests, builds, and quality checks that must pass

### Creating a Pull Request

```bash
# 1. Push your branch
git push origin feature/appointment-scheduling

# 2. On GitHub, click "Compare & pull request"

# 3. Fill in the template:
#    - Title
#    - Description
#    - Reviewers
#    - Labels
#    - Project
#    - Milestone

# 4. Click "Create pull request"
```

### Code Review Best Practices

#### As a Reviewer

✅ **Do:**
- Review promptly (within 24 hours)
- Be constructive and specific
- Ask questions to understand
- Praise good code
- Focus on important issues
- Test the changes if possible

```markdown
Good comment:
"This function could be more efficient using a Set instead of an Array for 
lookups. With large datasets, this would improve performance from O(n) to 
O(1). What do you think?"

Bad comment:
"This is wrong."
```

❌ **Don't:**
- Be vague or dismissive
- Make it personal
- Nitpick minor style issues (use linters instead)
- Block PRs unnecessarily
- Review your own code

#### As an Author

✅ **Do:**
- Keep PRs small and focused (< 400 lines changed)
- Respond to all comments
- Be open to feedback
- Update based on reviews
- Thank reviewers

❌ **Don't:**
- Get defensive
- Ignore feedback
- Create massive PRs
- Mix unrelated changes
- Force-push to reviewed branches (unless necessary)

### PR States

| State | Icon | Meaning |
|-------|------|---------|
| **Open** | 🟢 | Active, awaiting review or changes |
| **Draft** | ⚪ | Work in progress, not ready for review |
| **Changes Requested** | 🔴 | Reviewer requested modifications |
| **Approved** | ✅ | Approved and ready to merge |
| **Merged** | 🟣 | Changes integrated into target branch |
| **Closed** | ⚫ | Closed without merging |

---

## Forks

### What is a Fork?

A **fork** is a complete copy of a repository under your account. It's used for contributing to projects you don't have write access to.

### Fork vs Branch

```
Branches (Same Repository)
──────────────────────────
Org Repository
├── main
├── feature/branch-1
└── feature/branch-2
    ↑
    All in same repo, shared access


Forks (Different Repositories)
──────────────────────────────
Org Repository (Original)         Your Fork (Copy)
    └── main                          └── main
                                      └── your-feature
         ↑                                  ↓
    Pull Request submitted back to original
```

### When to Use Forks vs Branches

| Scenario | Use Fork | Use Branch |
|----------|----------|------------|
| Internal team project | ❌ | ✅ |
| Contributing to external project | ✅ | ❌ |
| Experimental changes | ✅ | ✅ |
| No write access to repo | ✅ | ❌ |
| ABB organization work | ❌ | ✅ |

### Working with Forks

```bash
# 1. Fork the repository on GitHub (click Fork button)

# 2. Clone your fork
git clone https://github.com/your-username/repository.git

# 3. Add original repo as upstream
git remote add upstream https://github.com/original-org/repository.git

# 4. Keep your fork updated
git fetch upstream
git merge upstream/main

# 5. Create feature branch
git checkout -b your-feature

# 6. Make changes and push to your fork
git push origin your-feature

# 7. Create pull request from your fork to original repo
```

---

## Merging

### What is Merging?

**Merging** combines changes from one branch into another, integrating work from different developers.

### Merge Strategies

#### 1. **Merge Commit** (Default)
```
main ──●──●──●──────────M──●──►
            \          / 
feature ─────●──●──●──●
```
Creates a merge commit showing the integration point. Preserves full history.

#### 2. **Squash and Merge**
```
main ──●──●──●──────────●'──●──►
            \          (Single commit)
feature ─────●──●──●──●
            (All commits combined)
```
Combines all feature branch commits into one. Cleaner history, loses detail.

#### 3. **Rebase and Merge**
```
main ──●──●──●──●──●──●──●──►
                 ↑  ↑  ↑
            Feature commits moved
```
Replays feature commits on top of main. Linear history, no merge commit.

### ABB Merge Policy

For ABB repositories:
- Use **Squash and Merge** for feature branches (cleaner history)
- Use **Merge Commit** for release branches (preserve history)
- Require at least one approval before merging
- Require passing CI checks before merging

---

## Merge Conflicts

### What is a Merge Conflict?

A conflict occurs when Git can't automatically merge changes because the same lines were modified differently.

### Example Conflict

```diff
<<<<<<< HEAD (main branch)
const API_URL = 'https://api.abb.wales.nhs.uk';
=======
const API_URL = 'https://dev-api.abb.wales.nhs.uk';
>>>>>>> feature/update-api (your branch)
```

### Resolving Conflicts

```bash
# 1. Identify conflicts
git status

# 2. Open conflicted files and edit
# Remove conflict markers (<<<, ===, >>>)
# Keep the correct version or combine both

# 3. Mark as resolved
git add resolved-file.js

# 4. Complete the merge
git commit -m "Merge feature/update-api into main"

# 5. Push
git push
```

### Preventing Conflicts

✅ **Best Practices:**
- Pull latest main before creating branches
- Keep feature branches short-lived
- Communicate with team about overlapping work
- Merge main into your branch regularly
- Use feature flags for large changes

---

## Practical Exercise

### Exercise: Branch, Commit, Pull Request

**Scenario**: You need to update documentation

#### Using GitHub Desktop (Recommended)

```
1. Open GitHub Desktop
2. Ensure you're on main branch
3. Click "Fetch origin" to get latest changes

4. Create a feature branch:
   - Click "Current Branch" dropdown
   - Click "New Branch"
   - Name: docs/update-training-readme
   - Click "Create Branch"

5. Make changes:
   - Edit Training/README.md in your editor
   - Save the file

6. Return to GitHub Desktop:
   - Changes appear automatically
   - Review diff in visual view
   - Verify changes are correct

7. Commit your changes:
   - Check the file to include
   - Summary: "Update training README with schedule details"
   - (Optional) Add description
   - Click "Commit to docs/update-training-readme"

8. Push to GitHub:
   - Click "Publish branch" (or "Push origin")
   - Branch is now on GitHub

9. Create Pull Request:
   - Click "Create Pull Request" button in GitHub Desktop
   - Browser opens with PR form
   - Add description
   - Request reviewers
   - Click "Create pull request"

10. After approval:
    - Merge via GitHub web interface
    - Click "Squash and merge"
    - Delete branch when prompted
```

**Why GitHub Desktop is better for this:**
- Visual confirmation of changes
- No risk of command typos
- Easier to review before committing
- One-click PR creation
- Beginner-friendly interface

---

## Summary

### Key Takeaways

✅ **Commits** are snapshots of your project with clear messages  
✅ **Branches** allow parallel development without affecting main code  
✅ **Pull Requests** enable code review and collaborative development  
✅ **Forks** are for external contributions; branches for internal work  
✅ **Merging** integrates changes with various strategies available  
✅ **Conflicts** are resolved manually when automatic merge fails

### Essential Commands Cheat Sheet

**Note:** These commands are for reference only. Use GitHub Desktop for daily work.

```bash
# Only use command line when GitHub Desktop cannot accomplish the task

# Branching (prefer GitHub Desktop)
git branch feature-name          # Create branch
git checkout feature-name        # Switch branch
git checkout -b feature-name     # Create and switch

# Committing (prefer GitHub Desktop)
git add file.txt                 # Stage file
git add .                        # Stage all changes
git commit -m "message"          # Commit with message

# Syncing (prefer GitHub Desktop)
git pull                         # Fetch and merge from remote
git push origin branch-name      # Push to remote

# Status (GitHub Desktop shows this visually)
git status                       # Show working directory status
git log                          # Show commit history
git diff                         # Show unstaged changes
```

**Reminder:** GitHub Desktop provides visual interfaces for all these operations with less risk of errors.

### Next Session Preview

In **Session 3: GitHub On-Prem vs Cloud**, we'll explore:
- Detailed comparison of deployment models
- GitHub Desktop as your primary tool
- GitHub workflows for on-premises scenarios
- When to use command line (as a last resort)
- Integration considerations

---

## Additional Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Git Branching Tutorial](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [Pull Request Best Practices](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)
- [Resolving Merge Conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts)

---

*Session 2 of 7 | GitHub Training Package*  
*Aneurin Bevan University Health Board*
