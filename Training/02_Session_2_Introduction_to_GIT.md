![BIU Logo](../links%20and%20logos/BIU%20LOGO.png) ![DDAT Logo](../links%20and%20logos/DDAT%20Logo.png)

---

# Session 2: Introduction to GIT

**Duration**: 1 hour  
**Time**: 09:30 - 10:30

## 🎯 Learning Objectives

By the end of this session, you will understand:

- What GIT is as a version control system (distinct from GitHub)
- The fundamental architecture and design of GIT
- Core GIT concepts: commits, trees, blobs, and the GIT object model
- How GIT stores and tracks changes over time
- The distributed nature of GIT and its benefits
- GIT's three-tree architecture: working directory, staging area (index), and repository
- How GIT ensures data integrity and enables collaboration

---

## 📚 What is GIT?

### GIT: The Version Control System

**GIT** is a distributed version control system (DVCS) created by Linus Torvalds in 2005 for managing the Linux kernel development. It is the underlying technology that powers platforms like GitHub, GitLab, and Bitbucket.

#### Key Characteristics

- **Distributed**: Every developer has a complete copy of the entire project history
- **Fast**: Most operations are local and extremely quick
- **Data Integrity**: Everything is checksummed before storage (SHA-1 hash)
- **Non-linear Development**: Powerful branching and merging capabilities
- **Free and Open Source**: Licensed under GPL v2

### GIT vs GitHub: Understanding the Difference

```
┌─────────────────────────────────────────────────────────────┐
│                          GitHub                             │
│  (Cloud Platform - Web Interface, Collaboration Tools)      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                      GIT                            │    │
│  │  (Version Control Engine - Local & Distributed)     │    │
│  │                                                     │    │
│  │  • Tracks changes                                   │    │
│  │  • Manages versions                                 │    │
│  │  • Enables branching                                │    │
│  │  • Stores history                                   │    │ 
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  • Pull Requests                                            │
│  • Issues and Projects                                      │
│  • Team Management                                          │
│  • Cloud Storage                                            │
│  • CI/CD Actions                                            │
└─────────────────────────────────────────────────────────────┘
```

**GIT** = The engine that manages version control
**GitHub** = A platform built on top of GIT that adds collaboration features

---

## GIT's Core Architecture

### The GIT Object Model

GIT stores everything as objects in a content-addressable filesystem. There are four types of objects:

#### 1. Blob (Binary Large Object)
- Stores file content (data)
- No filename, no metadata - just the raw content
- Identified by SHA-1 hash of the content

```
Example: patient_analysis.sql content
SHA-1: a3b5c8d9e1f2...
```

#### 2. Tree
- Represents a directory structure
- Contains pointers to blobs (files) and other trees (subdirectories)
- Stores filenames and permissions

```
Tree Object:
├── blob: patient_analysis.sql
├── blob: demographics.sql
└── tree: reports/
    ├── blob: monthly_report.sql
    └── blob: quarterly_report.sql
```

#### 3. Commit
- Snapshot of your project at a point in time
- Points to a tree object (the project state)
- Contains metadata: author, timestamp, message
- Points to parent commit(s) creating history chain

```
Commit Object:
├── Tree: SHA-1 pointer to project snapshot
├── Parent: SHA-1 pointer to previous commit(s)
├── Author: Dr. Sarah Williams <sarah@nhs.wales>
├── Date: 2024-03-15 10:30:00
└── Message: "Add patient risk calculation methodology"
```

#### 4. Tag
- Human-readable name pointing to a specific commit
- Used for marking releases or important milestones

```
Tag Object:
├── Object: SHA-1 pointer to commit
├── Type: commit
├── Tag: v1.0-patient-risk-model
├── Tagger: John Davies <john@nhs.wales>
└── Message: "First production release of risk model"
```

### Object Storage and Integrity

Every object in GIT is:

1. **Content-addressable**: Retrieved by its SHA-1 hash
2. **Immutable**: Once created, never changes
3. **Compressed**: Stored efficiently using zlib compression
4. **Verified**: SHA-1 checksum ensures data integrity

```
SHA-1 Hash Example:
a3b5c8d9e1f2a4b6c7d8e9f0a1b2c3d4e5f6a7b8

This 40-character hash uniquely identifies the content
Any change to the content produces a completely different hash
```

---

## 🌳 The Three-Tree Architecture

GIT manages your project through three conceptual "trees" or areas:

### 1. Working Directory (Working Tree)

**What it is**: Your actual project files on disk that you can see and edit

**Purpose**: Where you make changes to your code, SQL queries, notebooks, etc.

**Healthcare Example**:
```
Working Directory: /nhs-wales-analytics/
├── sql/
│   ├── patient_metrics.sql        (You're editing this)
│   └── admissions_report.sql      (Modified)
├── python/
│   └── risk_model.py              (Unchanged)
└── README.md                      (Unchanged)
```

**Status**: Files can be:
- **Untracked**: New files GIT doesn't know about yet
- **Modified**: Changed since last commit
- **Unmodified**: Same as last commit

### 2. Staging Area (Index)

**What it is**: An intermediate area between your working directory and repository

**Purpose**: Prepare and review changes before committing them permanently

**Why it matters**: Allows you to:
- Select specific changes to include in a commit
- Create logical, focused commits
- Review changes before making them permanent
- Stage parts of files (interactive staging)

**Healthcare Example**:
```
Working Directory → Staging Area → Repository

patient_metrics.sql (modified)
├── Line 45: Fix date calculation     ← Stage this
└── Line 89: Experimental change      ← Don't stage yet

admissions_report.sql (modified)  
└── All changes ready                 ← Stage everything
```

**Key Concept**: The staging area lets you craft commits thoughtfully, not just dump all changes at once.

### 3. Repository (HEAD)

**What it is**: The GIT database containing the complete project history

**Location**: Hidden `.git` directory in your project root

**Purpose**: Permanent storage of all commits, branches, and project history

**Example**:
```
Repository History:
├── Commit a3b5c8d (HEAD → main)
│   "Add patient risk stratification"
│   Date: 2024-03-15 14:30
│
├── Commit d4e6f7a
│   "Fix emergency admission calculation"  
│   Date: 2024-03-14 10:15
│
└── Commit h8i9j0k
    "Initial patient analytics setup"
    Date: 2024-03-10 09:00
```

### The Flow Between Trees

```
┌──────────────────┐
│     Working      │  ← You edit files here
│    Directory     │
└────────┬─────────┘
         │ git add
         ↓
┌──────────────────┐
│     Staging      │  ← You prepare commits here
│   Area (Index)   │
└────────┬─────────┘
         │ git commit
         ↓
┌──────────────────┐
│    Repository    │  ← Permanent history stored here
│      (HEAD)      │
└──────────────────┘
```

---

## How GIT Tracks Changes

### Snapshot-Based, Not Delta-Based

Unlike some version control systems that store deltas (differences), GIT stores complete snapshots.

#### Other VCS (Delta-Based) Version Control Systems:
```
Version 1: Full file
Version 2: +changes
Version 3: +more changes
```

#### GIT (Snapshot-Based):
```
Commit 1: Complete snapshot of project
Commit 2: Complete snapshot of project (efficient storage via compression)
Commit 3: Complete snapshot of project
```

**Benefits**:
- Fast operations (no need to calculate from deltas)
- Data integrity (complete state at every commit)
- Simple branching and merging
- Reliable history reconstruction

### Analytics Example

```sql
-- Commit 1: patient_metrics.sql
SELECT patient_id, age 
FROM demographics;

-- Commit 2: patient_metrics.sql (complete file stored)
SELECT patient_id, age, gender 
FROM demographics;

-- Commit 3: patient_metrics.sql (complete file stored)
SELECT patient_id, age, gender, diagnosis
FROM demographics
WHERE admission_date >= '2024-01-01';
```

Each commit stores the **entire file content**, but GIT uses:
- **Compression**: Reduces storage overhead
- **Pack files**: Groups objects efficiently
- **Delta compression**: Applied during packing (but conceptually still snapshots)

---

## The Distributed Model

### What "Distributed" Means

In GIT, every developer has a **complete copy** of the entire repository, including full history.

#### Centralized VCS (Old Model):
```
         Central Server
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
Developer A  Dev B    Dev C
(No history) (No history) (No history)
```

**Problems**:
- Single point of failure
- All operations require network
- Limited offline work
- Server performance bottleneck

#### Distributed VCS (GIT Model):
```
    Remote Repository (GitHub)
       (Full History)
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
Developer A  Dev B    Dev C
(Full history) (Full history) (Full history)
```

**Benefits**:
- No single point of failure
- Most operations are local and fast
- Full offline capability
- Multiple backup copies
- Flexible workflows



**Each site can**:
- Work offline during network issues
- Review complete history locally
- Create branches without server
- Commit changes locally
- Sync when ready/able

---

## 🔐 Data Integrity and Security

### SHA-1 Checksums

Every object in GIT is identified by a 40-character SHA-1 hash:

```
a3b5c8d9e1f2a4b6c7d8e9f0a1b2c3d4e5f6a7b8
```

**How it works**:
1. GIT computes SHA-1 hash of content
2. Uses hash as unique identifier
3. Stores object using hash as key
4. Any corruption or tampering detected immediately

**Example**:
```sql
-- Original content: patient_metrics.sql
SELECT patient_id, age FROM demographics;

SHA-1: a3b5c8d9e1f2a4b6c7d8e9f0a1b2c3d4e5f6a7b8

-- If even one character changes:
SELECT patient_id, age FROM demographics WHERE age > 0;

SHA-1: completely different hash!
```

### Benefits for Data Integrity

1. **Tamper Detection**: Any unauthorised change detected immediately
2. **Audit Trail**: Complete verifiable history of all changes
3. **Data Recovery**: Lost or corrupted data can be recovered from other copies
4. **Compliance**: Meets regulatory requirements for data integrity and traceability

---

## 📁 Inside the .git Directory

When you initialize a GIT repository, a `.git` directory is created:

```
.git/
├── objects/          # All content (blobs, trees, commits, tags)
│   ├── pack/        # Compressed object packs
│   └── info/        # Pack metadata
├── refs/            # Pointers to commits (branches, tags)
│   ├── heads/       # Local branches
│   ├── remotes/     # Remote branches
│   └── tags/        # Tags
├── HEAD             # Points to current branch/commit
├── config           # Repository configuration
├── description      # Repository description
├── hooks/           # Automation scripts
├── index            # Staging area content
└── logs/            # Reference logs (reflog)
```

**Important**: Never manually edit `.git` directory contents unless you know exactly what you're doing!

### What Each Component Does

#### objects/
- Stores all GIT objects (blobs, trees, commits)
- Content-addressable storage using SHA-1 hashes
- Compressed and packed for efficiency

#### refs/
- Stores branch and tag pointers
- Simple text files containing SHA-1 hashes
- Example: `refs/heads/main` contains the commit hash that `main` points to

#### HEAD
- Points to your current branch or commit
- Usually contains: `ref: refs/heads/main`
- Determines what you're currently working on

#### index
- The staging area content
- Binary file tracking staged changes
- Updated by `git add` command

---

## Core GIT Concepts

### Commits: The Building Blocks

A commit is a snapshot of your project at a specific point in time.

**What a commit contains**:
```
Commit: a3b5c8d9e1f2a4b6c7d8e9f0a1b2c3d4e5f6a7b8
├── Tree: pointer to project snapshot
├── Parent: pointer to previous commit
├── Author: Dr. Sarah Williams <sarah@nhs.wales>
├── Committer: Dr. Sarah Williams <sarah@nhs.wales>
├── Date: Thu Mar 15 10:30:00 2024 +0000
└── Message:
    Add patient risk calculation methodology
    
    - Implement comorbidity scoring algorithm
    - Add age stratification factors
    - Include validation against clinical guidelines
    
    Closes #156
```

**Commit Chain (History)**:
```
A ← B ← C ← D ← E (main)
            ↑
          HEAD
```

Each commit points to its parent(s), creating an immutable history chain.

### Branches: Lightweight Pointers

In GIT, a branch is simply a **movable pointer** to a commit.

```
Commit History:
A ← B ← C ← D ← E
            ↑   ↑
         feature main
```

**Key insights**:
- Branches are extremely cheap (just a 41-byte file)
- Creating/deleting branches is instant
- Switching branches is fast (just updates working directory)
- Enables parallel development without copying files

**Healthcare Example**:
```
main:               A ← B ← C
                              ↓
feature/covid:                D ← E
feature/bed-metrics:          F ← G
```

Multiple teams work independently on different branches.

### HEAD: Your Current Position

`HEAD` is a special pointer indicating where you currently are in the repository.

**Typical state** (attached HEAD):
```
HEAD → main → commit E
```
You're on the `main` branch, currently at commit E.

**Detached HEAD**:
```
HEAD → commit C (not on any branch)
```
You've checked out a specific commit directly.

---

## Basic GIT Operations (Conceptual)

### Initializing a Repository

```bash
git init
```

**What happens**:
1. Creates `.git` directory
2. Initializes objects database
3. Creates refs structure
4. Sets up HEAD pointing to (non-existent) main branch

### Adding Changes (Staging)

```bash
git add patient_metrics.sql
```

**What happens**:
1. Computes SHA-1 hash of file content
2. Compresses content
3. Stores as blob object in `.git/objects/`
4. Updates index (staging area) with blob hash
5. File is now "staged" for commit

### Creating a Commit

```bash
git commit -m "Add patient risk calculations"
```

**What happens**:
1. Creates tree object from staged content
2. Creates commit object pointing to tree
3. Sets parent to current HEAD commit
4. Adds author, timestamp, message
5. Moves branch pointer to new commit
6. Updates HEAD

**Result**: New snapshot permanently recorded in repository history.

### Viewing History

```bash
git log
```

**What it shows**:
- List of commits in reverse chronological order
- Each commit's hash, author, date, message
- Branch and tag positions
- Relationship between commits (parent/child)

---

## Branching and Merging (Conceptual)

### How Branching Works in GIT

**Creating a branch**:
```bash
git branch feature/patient-safety
```

**What happens**:
- Creates new file: `.git/refs/heads/feature/patient-safety`
- File contains SHA-1 hash of current commit
- Branch now points to same commit as current branch
- No files copied, no duplication—instant operation

**Visual**:
```
Before:
A ← B ← C
        ↑
      main, HEAD

After git branch feature/patient-safety:
A ← B ← C
        ↑
      main, feature/patient-safety, HEAD
```

### Switching Branches

```bash
git checkout feature/patient-safety
```

**What happens**:
1. Updates HEAD to point to `feature/patient-safety`
2. Updates working directory to match that branch's commit
3. Updates staging area to match commit

### How Merging Works

When you merge two branches, GIT finds:

1. **Common ancestor**: The commit where branches diverged
2. **Branch tips**: The latest commits on each branch
3. **Three-way merge**: Combines changes from both branches

**Example**:
```
      C ← D  (feature)
     ↗
A ← B ← E ← F  (main)

After merge:
      C ← D
     ↗     ↘
A ← B ← E ← F ← M  (main)
```

Commit M combines changes from both D and F.

---

## Why GIT's Design Matters for Data Teams

### 1. Data Integrity

**SHA-1 checksums** ensure:
- Any tampering detected immediately
- Complete audit trail for compliance
- Data corruption identified and recovered
- Regulatory requirements met (GDPR, audit trails)

### 2. Distributed Reliability

**Every team has complete copy**:
- No single point of failure
- Work continues during network issues
- Multiple backup copies automatically
- Resilience for critical healthcare systems

### 3. Speed and Efficiency

**Local operations** mean:
- Fast commit and branch operations
- Quick history searches
- No waiting for server responses
- Better developer/analyst productivity

### 4. Branching for Safety

**Cheap branches** enable:
- Safe experimentation without affecting production
- Parallel development of multiple features
- Isolated testing of new methodologies
- Easy rollback if problems detected

### 5. Complete History

**Every change tracked** provides:
- Full audit trail for compliance
- Ability to understand why changes were made
- Rollback to any previous state
- Knowledge transfer when team members change

---

## Key Concepts Summary

### GIT's Core Philosophy

1. **Snapshots, not differences**: Store complete project state
2. **Everything is local**: Most operations don't need network
3. **Data integrity**: SHA-1 ensures nothing corrupts or changes undetected
4. **Distributed**: Every clone is a full backup
5. **Cheap branches**: Branching is fast and encouraged

### The Three States of Files

```
Modified → Staged → Committed
   ↓         ↓         ↓
Working   Staging  Repository
 Tree      Area     Database
```

### The Three Types of GIT References

1. **Branches**: Movable pointers to commits (development)
2. **Tags**: Fixed pointers to commits (releases)
3. **HEAD**: Your current position in the repository

### Core GIT Objects

1. **Blob**: File content
2. **Tree**: Directory structure
3. **Commit**: Snapshot with metadata
4. **Tag**: Named reference to commit

---

## Healthcare Analytics Context



#### Patient Safety Analysis
```
main (production)
├── Validated, approved calculations
└── Audit trail of all methodology changes

feature/new-safety-metric
├── Experimental work isolated
└── Can be reviewed before production
```

#### Multi-Site Collaboration
```
Cardiff: Full repository copy
Swansea: Full repository copy
Newport: Full repository copy

All can work independently
All sync changes when ready
All have complete backup
```

#### Compliance and Audit
```
Every change:
├── Who made it (author)
├── When they made it (timestamp)
├── Why they made it (commit message)
├── What exactly changed (diff)
└── Who reviewed it (via pull request)
```

### GIT Enables

- ✅ **Reproducibility**: Exact recreation of any analysis
- ✅ **Collaboration**: Multiple analysts working safely
- ✅ **Quality**: Review process before production
- ✅ **Compliance**: Complete audit trail
- ✅ **Recovery**: Rollback to any previous state
- ✅ **Knowledge**: Understanding evolution of work

---

## 🎯 Session 2 Recap

### What You Now Understand

#### 1. GIT vs GitHub
- **GIT**: Version control system (the engine)
- **GitHub**: Platform built on GIT (adds collaboration)

#### 2. GIT's Architecture
- **Object model**: Blobs, trees, commits, tags
- **Content-addressable storage**: SHA-1 hashing
- **Three-tree architecture**: Working, staging, repository

#### 3. How GIT Works
- **Snapshot-based**: Complete project state at each commit
- **Distributed**: Full copy in every clone
- **Data integrity**: Checksums ensure safety

#### 4. Core Concepts
- **Commits**: Immutable snapshots of project
- **Branches**: Lightweight pointers to commits
- **HEAD**: Current position indicator

### Why This Matters

Understanding GIT's fundamentals helps you:
- **Make better decisions** about when to commit and branch
- **Understand error messages** and how to fix issues
- **Appreciate the power** of distributed version control
- **Work confidently** with healthcare analytics data
- **Ensure compliance** through proper version control

---

## Next Session Preview

**Session 3: Branching and Sync Operations**

Now that you understand how GIT works internally, we'll explore:
- Practical branching strategies for healthcare analytics
- Remote operations: push, pull, fetch, and sync
- Conflict resolution in multi-analyst environments
- Pull request workflows for code review
- Best practices for NHS Wales collaboration

---

## 🎯 Git Master Commands Reference

### Essential Git Commands Crib Sheet

| Git CLI Command | GitHub UI Command | Description | Simple Use Case |
|----------------|-------------------|-------------|-----------------|
| `git clone <url>` | "Clone" button → Download ZIP or Clone | Download a complete repository to your local machine | Getting the NHS analytics project for the first time |
| `git init` | Create new repository | Initialize a new Git repository in current directory | Starting a new healthcare analytics project |
| `git status` | File change indicators | Show current status of working directory and staging area | Check what files you've modified before committing |
| `git add <file>` | Upload files / Drag & drop | Stage specific files for commit | Prepare your patient metrics SQL file for commit |
| `git add .` | Select multiple files | Stage all modified files in directory | Stage all changes when ready to commit everything |
| `git commit -m "message"` | Commit changes button | Create a permanent snapshot with descriptive message | Save your completed risk calculation methodology |
| `git push` | None (automatic after web commits) | Upload local commits to remote repository | Share your completed analysis with the team |
| `git pull` | Sync fork / Fetch upstream | Download and merge latest changes from remote | Get latest updates from colleagues before starting work |
| `git fetch` | Compare & pull request view | Download remote changes without merging | Check what teammates have done without affecting your work |
| `git merge <branch>` | Create pull request → Merge | Combine changes from one branch into current branch | Integrate completed feature into main analysis |
| `git branch` | Branch dropdown menu | List all local branches | See all parallel workstreams in your project |
| `git branch <name>` | Create branch button | Create a new branch from current commit | Start working on experimental bed capacity model |
| `git checkout <branch>` | Click branch name | Switch to different branch | Move to your patient safety analysis branch |
| `git checkout -b <name>` | Create branch button | Create and switch to new branch in one command | Quick start on urgent mortality analysis |
| `git log` | Commits tab | View commit history with messages and authors | Review all changes made to patient risk algorithms |
| `git log --oneline` | Commits tab (condensed) | View simplified one-line commit history | Quick overview of recent project changes |
| `git diff` | File diff view | Show differences between working directory and staging | See exactly what you changed in admission rates query |
| `git diff --staged` | Staged changes view | Show differences between staging area and last commit | Review changes before committing |
| `git reset <file>` | Unstage changes | Remove file from staging area (keep changes) | Unstage patient data you're not ready to commit |
| `git reset --hard HEAD` | Discard changes button | Discard all uncommitted changes (DANGEROUS) | Abandon experimental changes that didn't work |
| `git revert <commit>` | Revert button on commit | Create new commit that undoes a previous commit | Safely undo problematic mortality calculation |
| `git reset --hard <commit>` | N/A (use revert instead) | Reset to specific commit, losing all subsequent changes | Emergency rollback (use with extreme caution) |
| `git stash` | N/A | Temporarily save uncommitted changes | Quickly switch branches with unsaved work |
| `git stash pop` | N/A | Restore most recent stashed changes | Get back your temporary changes after branch switch |
| `git remote -v` | Settings → Manage access | Show remote repository URLs | Check where your local repo connects to GitHub |
| `git remote add origin <url>` | Link repository | Connect local repo to remote GitHub repository | Link your local analysis to team GitHub project |
| `git tag <name>` | Create release | Mark specific commit with readable name | Tag v1.0 of your patient risk model for production |
| `git tag -a <name> -m "msg"` | Create release with notes | Create annotated tag with description | Mark production release with detailed changelog |
| `git push --tags` | Publish release | Upload local tags to remote repository | Share version milestones with the team |
| `git blame <file>` | Blame view | Show who last modified each line of file | Find out who created specific mortality calculation |
| `git show <commit>` | Click commit hash | Display detailed information about specific commit | Review what changed in Tuesday's bed capacity update |
| `git cherry-pick <commit>` | N/A (manual process) | Apply specific commit from another branch | Copy urgent fix from feature branch to main |
| `git rebase <branch>` | N/A (use merge via PR) | Replay commits from current branch onto another | Clean up branch history before merging |
| `git clean -f` | Discard untracked files | Remove untracked files from working directory | Clean up temporary analysis files |
| `git mv <old> <new>` | Rename file | Rename/move file while maintaining Git history | Rename patient_analysis.sql to patient_risk_v2.sql |
| `git rm <file>` | Delete file | Remove file from both working directory and Git | Delete outdated demographic query safely |

### Branch Management Commands

| Git CLI Command | GitHub UI Command | Description | Use Case |
|----------------|-------------------|-------------|---------------------|
| `git branch -d <name>` | Delete branch button | Delete a merged branch | Clean up completed patient safety feature |
| `git branch -D <name>` | Force delete option | Force delete unmerged branch | Remove abandoned experimental analysis |
| `git branch -m <new-name>` | Rename branch | Rename current branch | Change "temp" to "covid-impact-analysis" |
| `git branch -u origin/<branch>` | Set upstream | Set tracking relationship with remote branch | Link local feature to remote collaboration |
| `git push -u origin <branch>` | Publish branch | Push new branch and set upstream tracking | Share new mortality analysis with team |
| `git push --delete origin <branch>` | Delete branch (remote) | Delete branch from remote repository | Remove completed feature from GitHub |

### Emergency Commands (Use with Caution)

| Git CLI Command | GitHub UI Command | Description | When to Use |
|----------------|-------------------|-------------|-------------|
| `git reset --hard HEAD~1` | N/A | Remove last commit entirely (DESTRUCTIVE) | Committed sensitive patient data by mistake |
| `git push --force` | N/A | Overwrite remote history (DANGEROUS) | After authorised history rewrite (rare) |
| `git reflog` | N/A | View all HEAD movements (recovery tool) | Find "lost" commits after reset mishap |
| `git fsck --full` | N/A | Check repository integrity | Verify no corruption after system crash |

### Quick Reference Workflow

#### Daily Development Flow
```bash
git status                    # Check current state
git pull                     # Get latest changes
git checkout -b feature/new  # Create feature branch
# ... do your work ...
git add .                    # Stage changes
git commit -m "Add feature"  # Commit changes
git push -u origin feature/new # Push to GitHub
# ... create pull request in GitHub UI ...
git checkout main            # Switch back to main
git pull                     # Get merged changes
git branch -d feature/new    # Clean up local branch
```

#### Emergency Rollback
```bash
git log --oneline           # Find problematic commit
git revert <commit-hash>    # Create undo commit
git push                    # Share the fix
```

### Notes 

- **Always use `git revert`** instead of `git reset` for shared repositories
- **Create descriptive commit messages** for audit trails
- **Use branches** for all experimental or feature work
- **Pull before pushing** to avoid conflicts
- **Tag releases** for production deployments
- **Never force push** to shared branches without team approval

---

## 📖 Additional Resources

---

*Session 2 of 8 | GitHub Training Series for Analytics and Data Teams*  
*Developed by ABUHB Business Intelligence Team*
