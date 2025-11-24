# Session 5: GitHub Components

**Duration**: 30 minutes  
**Time**: 12:00 - 12:30

## 🎯 Learning Objectives

By the end of this session, you will understand:
- How to effectively use GitHub repositories
- Managing issues for task tracking and bug reports
- Pull request workflow for code review
- Using Projects for agile planning
- Documentation with Wikis
- Team collaboration with Discussions

---

## GitHub Repositories

### What is a Repository?

A **repository** (repo) is the fundamental unit in GitHub. It contains:
- All project files and folders
- Complete revision history
- Configuration and settings
- Collaboration tools (issues, PRs, etc.)

### Repository Structure

```
biu_analytics_dashboard/
├── .github/                    # GitHub-specific files
│   ├── workflows/              # GitHub Actions workflows
│   │   └── deploy.yml
│   ├── ISSUE_TEMPLATE/         # Issue templates
│   │   ├── bug_report.yml
│   │   └── feature_request.yml
│   └── pull_request_template.md
├── src/                        # Source code
│   ├── components/
│   ├── pages/
│   └── utils/
├── tests/                      # Test files
├── docs/                       # Documentation
├── .gitignore                  # Files to ignore
├── README.md                   # Project overview
├── LICENSE                     # License information
├── CONTRIBUTING.md             # Contribution guidelines
└── package.json                # Dependencies
```

### Repository Settings

#### 1. **General Settings**
- **Repository name**: Follow ABB naming convention (`prefix_project_name`)
- **Description**: Clear, concise project description
- **Visibility**: Private (default for ABB) or Internal
- **Features**: Enable/disable issues, wikis, projects, discussions

#### 2. **Collaborators and Teams**
```
Access Levels:
├── Read: View and clone code
├── Triage: Manage issues and PRs without code access
├── Write: Push to repository
├── Maintain: Manage repository settings
└── Admin: Full control including deletion
```

For ABB:
- **BIU - Data Engineers**: Write access to `biu_*` repositories
- **BIU - Seniors**: Admin access for code review
- **PHN Team**: Write access to `phn_*` repositories

#### 3. **Branch Protection Rules**

Protect the `main` branch:
```yaml
Protection Rules:
├── Require pull request before merging
│   ├── Require 1-2 approvals
│   └── Dismiss stale reviews
├── Require status checks to pass
│   ├── Run CI/CD pipeline
│   └── Pass linting and tests
├── Require conversation resolution
├── Require signed commits
└── Include administrators (optional)
```

#### 4. **Security Settings**
- **Dependabot alerts**: Automatic vulnerability detection
- **Code scanning**: Static analysis with CodeQL
- **Secret scanning**: Detect exposed credentials
- **Security policy**: Define security procedures

### Repository README

A **README.md** is the first thing visitors see. It should include:

```markdown
# Project Name

Brief description of what the project does.

## Purpose
Why this project exists and what problem it solves.

## Features
- Key feature 1
- Key feature 2
- Key feature 3

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- GCP project access

### Installation
```bash
git clone https://github.com/org/repo.git
cd repo
npm install
```

### Usage
```bash
npm run dev
```

## Team Ownership
- **Primary Team**: BIU - Data Engineers
- **Maintainers**: @senior-engineer1, @senior-engineer2

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## License
Internal use only - Aneurin Bevan University Health Board
```

---

## Issues

### What are GitHub Issues?

**Issues** are GitHub's task tracking system. Use them for:
- 🐛 Bug reports
- ✨ Feature requests
- 📝 Documentation tasks
- ❓ Questions and discussions
- 🔧 Technical debt tracking

### Anatomy of an Issue

```
Title: Fix date calculation in reporting module

Labels: bug, priority:high, area:reporting

Assignees: @data-engineer1

Description:
## Description
The weekly reporting module calculates dates incorrectly 
when crossing month boundaries.

## Steps to Reproduce
1. Generate report for dates 28-Jan to 5-Feb
2. Observe incorrect date ranges in output

## Expected Behavior
Dates should span continuously across months

## Actual Behavior
Week splits incorrectly at month boundary

## Environment
- Version: 2.3.1
- Environment: Production
- GCP Region: europe-west2

## Screenshots
[Attach screenshot showing the issue]

## Additional Context
Related to PR #234 which refactored date handling
```

### Issue States

| State | Icon | Description |
|-------|------|-------------|
| **Open** | 🟢 | Active, needs work |
| **In Progress** | 🔵 | Being worked on |
| **Closed** | 🟣 | Completed or resolved |

### Labels

Labels categorize and prioritize issues:

#### ABB Standard Labels

**Type:**
- `bug` - Something isn't working
- `feature` - New functionality
- `documentation` - Documentation improvements
- `technical-debt` - Code quality improvements
- `question` - Further information requested

**Priority:**
- `priority:critical` - Urgent, blocks work
- `priority:high` - Important, should be addressed soon
- `priority:medium` - Normal priority
- `priority:low` - Nice to have

**Area:**
- `area:frontend` - UI/UX related
- `area:backend` - Server/API related
- `area:database` - Database/BigQuery related
- `area:infrastructure` - GCP/deployment related
- `area:testing` - Test coverage

**Status:**
- `status:needs-triage` - Needs review
- `status:blocked` - Waiting on dependency
- `status:wont-fix` - Not going to address
- `status:duplicate` - Already reported

### Issue Templates

Create templates in `.github/ISSUE_TEMPLATE/`:

```yaml
# bug_report.yml
name: Bug Report
description: Report a bug or issue
title: "[BUG]: "
labels: ["bug", "status:needs-triage"]

body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug! Please fill out the information below.
  
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear description of the bug
      placeholder: Tell us what happened
    validations:
      required: true
  
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this issue?
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true
  
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Low
        - Medium
        - High
        - Critical
    validations:
      required: true
```

### Working with Issues

#### Create an Issue
1. Navigate to repository
2. Click **Issues** tab
3. Click **New issue**
4. Select template or start blank
5. Fill in details
6. Assign labels, assignees, milestone
7. Click **Submit new issue**

#### Reference Issues

In commits and PRs:
```
Fixes #123
Closes #234
Related to #345
Resolves #456
```

GitHub automatically links and can close issues when PRs merge.

#### Issue Best Practices

✅ **Do:**
- Use descriptive titles
- Provide complete information
- Add relevant labels
- Assign to appropriate person
- Link related issues and PRs
- Update status as work progresses

❌ **Don't:**
- Create vague or unclear issues
- Duplicate existing issues
- Use issues for general chat (use Discussions)
- Leave issues open indefinitely

---

## Pull Requests (In-Depth)

### Pull Request Lifecycle

```
1. Create Branch        2. Make Changes         3. Open PR
   feature/login    →     Commit code      →    Open on GitHub
                                                      │
                                                      ▼
4. Code Review         5. Address Feedback      6. Approval
   Comments & tests ←  Update code          →   ✅ Approved
                                                      │
                                                      ▼
7. Merge               8. Deploy               9. Close
   Squash & merge  →   CI/CD runs         →    🎉 Complete
```

### Pull Request Template

Create `.github/pull_request_template.md`:

```markdown
## Description
<!-- Brief description of changes -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Infrastructure change

## Changes Made
<!-- List key changes -->
- Change 1
- Change 2
- Change 3

## Related Issues
<!-- Link related issues -->
Fixes #
Related to #

## Testing
<!-- Describe testing performed -->
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Tested in development environment

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] Dependent changes merged

## Screenshots
<!-- If UI changes, add screenshots -->

## Deployment Notes
<!-- Any special deployment considerations -->

## Reviewers
<!-- Tag specific reviewers if needed -->
@biu-seniors
```

### Review Process

#### As a Reviewer

**1. Start Review**
- Click **Files changed** tab
- Review each file's changes
- Add inline comments on specific lines

**2. Comment Types**

```markdown
💬 General Comment:
"This approach looks good overall"

🤔 Question:
"Could we use a map instead of filter + find for better performance?"

⚠️ Concern:
"This function doesn't handle null values. We should add validation."

✅ Approval:
"LGTM! Nice work on the error handling."

🎓 Learning:
"TIL: This is a clever use of destructuring"
```

**3. Submit Review**
- **Comment**: General feedback, no approval
- **Approve**: Changes look good, ready to merge
- **Request Changes**: Must address issues before merge

#### As an Author

**1. Respond to Comments**
```markdown
✅ Resolved: "Fixed in abc123"
💬 Discussion: "I considered that, but..."
🔄 Updated: "Changed approach as suggested"
❓ Question: "Could you clarify what you mean?"
```

**2. Make Updates**
```bash
# Address feedback
git checkout feature/login
# Make changes
git add .
git commit -m "Address review feedback"
git push origin feature/login
```

**3. Request Re-review**
- Resolve conversations
- Click **Re-request review** button

### Draft Pull Requests

Use **Draft PRs** for work in progress:
- Shows progress without requesting review
- Can get early feedback
- Mark as "Ready for review" when complete

```
Draft PR Title: WIP: Add authentication system
Status: 🟡 Draft
```

### Pull Request Checks

**Automatic Checks:**
```
✅ CI Build Passing
✅ Tests Passing (143/143)
✅ Code Coverage: 87%
✅ Linting: No errors
✅ Security Scan: No vulnerabilities
❌ Performance Test: Failed (needs review)
```

**Required Reviews:**
```
Reviews: 1 of 2 required
✅ @senior-engineer1 approved
⏳ @senior-engineer2 pending
```

### Merge Strategies

#### 1. **Squash and Merge** (ABB Default)
```
All commits combined into one:
- Cleaner history
- Easier to revert
- Loses individual commit details
```

#### 2. **Merge Commit**
```
Preserves all commits:
- Complete history
- Shows exact development flow
- More complex history
```

#### 3. **Rebase and Merge**
```
Linear history:
- No merge commits
- Clean, straight-line history
- Can be confusing if done wrong
```

---

## GitHub Projects

### What are GitHub Projects?

**GitHub Projects** is an agile project management tool integrated with repositories.

### Project Views

#### 1. **Board View** (Kanban)
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│   Backlog    │   To Do      │ In Progress  │     Done     │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ Issue #245   │ Issue #234   │ Issue #123   │ Issue #100   │
│ Feature req  │ Bug fix      │ In dev       │ Completed    │
│              │              │              │              │
│ Issue #246   │ Issue #235   │ PR #124      │ Issue #101   │
│ Tech debt    │ Enhancement  │ Under review │ Deployed     │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

#### 2. **Table View**
| Title | Status | Assignee | Priority | Due Date | Labels |
|-------|--------|----------|----------|----------|--------|
| Fix dashboard | In Progress | @dev1 | High | 2024-11-15 | bug |
| Add auth | To Do | @dev2 | Medium | 2024-11-30 | feature |

#### 3. **Roadmap View**
```
Timeline view showing:
├── Q4 2024
│   ├── Analytics Dashboard v2.0
│   └── User Authentication
└── Q1 2025
    ├── Reporting Module
    └── Mobile Support
```

### Creating a Project

**1. Create Project**
- Go to organization or repository
- Click **Projects** tab
- Click **New project**
- Choose template (Kanban, Scrum, etc.)

**2. Configure Columns**
```
Workflow:
├── 📥 Backlog (Triage needed)
├── 📋 To Do (Ready for work)
├── 🏗️ In Progress (Active development)
├── 👀 In Review (PR open)
├── ✅ Done (Completed)
└── 🎉 Released (In production)
```

**3. Add Items**
- Link existing issues and PRs
- Create new issues directly
- Convert notes to issues

**4. Automation**
```yaml
Automations:
├── When issue created → Add to Backlog
├── When PR opened → Move to In Review
├── When PR merged → Move to Done
└── When issue closed → Archive
```

### ABB Project Example

**Project**: BIU Analytics Platform Q4 2024

**Columns:**
- **Backlog**: User stories and feature requests
- **Sprint Ready**: Refined and estimated
- **In Development**: Current sprint work
- **Code Review**: PRs awaiting review
- **Testing**: QA validation
- **Done**: Completed this sprint
- **Released**: Deployed to production

**Filters:**
- By team member
- By priority
- By label (frontend/backend)
- By milestone

---

## Wikis

### What is a Wiki?

**Wikis** provide collaborative documentation space within a repository.

### When to Use Wikis

✅ **Good for:**
- Internal documentation
- Onboarding guides
- Architecture documentation
- Development workflows
- Troubleshooting guides
- Meeting notes

❌ **Not ideal for:**
- User-facing documentation (use `docs/` folder)
- Code documentation (use inline comments)
- Versioned documentation (use `docs/` in main branch)

### Wiki Structure Example

```
Home
├── Getting Started
│   ├── Local Development Setup
│   ├── GCP Access Setup
│   └── First Time Contributors
├── Architecture
│   ├── System Overview
│   ├── Data Flow
│   └── Technology Stack
├── Development
│   ├── Coding Standards
│   ├── Testing Guidelines
│   ├── CI/CD Pipeline
│   └── Deployment Process
├── Operations
│   ├── Monitoring
│   ├── Incident Response
│   └── Runbooks
└── Team
    ├── Team Members
    ├── Meetings Schedule
    └── Decision Log
```

### Creating Wiki Content

**Markdown Example:**

```markdown
# Local Development Setup

## Prerequisites
- Python 3.11+
- Node.js 18+
- Docker Desktop
- GCP CLI

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/ABB/biu_analytics_dashboard.git
cd biu_analytics_dashboard
```

### 2. Install Dependencies
```bash
npm install
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Start Development Server
```bash
npm run dev
```

Visit http://localhost:3000

## Troubleshooting

### Port Already in Use
If port 3000 is in use:
```bash
lsof -ti:3000 | xargs kill -9
```

### Database Connection Issues
Check your `.env` file has correct credentials:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=analytics_dev
```

## Next Steps
- Read [Coding Standards](Coding-Standards)
- Join team Slack channel
- Review [Architecture Overview](Architecture-Overview)
```

### Wiki Best Practices

✅ **Do:**
- Keep pages focused and concise
- Use clear hierarchy
- Link related pages
- Update regularly
- Include examples
- Add table of contents for long pages

❌ **Don't:**
- Duplicate content from main docs
- Let pages become outdated
- Use for code-level documentation
- Include sensitive information

---

## Discussions

### What are GitHub Discussions?

**Discussions** are a forum-style communication tool for community conversations.

### Discussion Categories

```
Categories:
├── 📢 Announcements
│   └── Official team announcements
├── 💡 Ideas
│   └── Feature suggestions and brainstorming
├── ❓ Q&A
│   └── Questions and answers
├── 🙏 Help Wanted
│   └── Request for assistance
├── 🎉 Show and Tell
│   └── Share accomplishments
└── 💬 General
    └── Anything else
```

### When to Use Discussions vs Issues

| Use Case | Issues | Discussions |
|----------|--------|-------------|
| Bug reports | ✅ | ❌ |
| Feature requests | ✅ | ⚠️ (Use Ideas) |
| Questions | ❌ | ✅ |
| Brainstorming | ❌ | ✅ |
| General chat | ❌ | ✅ |
| Announcements | ❌ | ✅ |
| Show work | ❌ | ✅ |
| Task tracking | ✅ | ❌ |

### Example Discussion

**Category**: Ideas  
**Title**: Suggestion: Add Dark Mode to Dashboard

```markdown
## Background
Many users work late hours and have requested a dark mode option.

## Proposal
Add a theme toggle that switches between light and dark modes.

## Benefits
- Better for low-light environments
- Reduced eye strain
- Modern UX expectation
- Potential power savings on OLED displays

## Implementation Considerations
- CSS variables for colors
- Persist preference in localStorage
- System theme detection

## What do you think?
Would this be valuable? Any concerns or alternative approaches?
```

**Responses:**
```
👍 25 reactions
💬 8 comments

@designer1: Love this idea! We can use CSS custom properties 
to make this easy to maintain.

@developer2: Should we also consider a "system" option that 
follows the OS theme?

@senior3: Let's create an issue to track this once we agree 
on the approach.
```

### Discussion Best Practices

✅ **Do:**
- Use appropriate categories
- Search before posting
- Be respectful and constructive
- Mark helpful answers
- Convert to issues when actionable

❌ **Don't:**
- Use for urgent matters (use issues)
- Post sensitive information
- Report security issues (use private channel)
- Spam or cross-post

---

## Putting It All Together

### Typical ABB Workflow

**1. Planning Phase**
- Create **Project** for sprint/milestone
- Add user stories as **Issues**
- Organize in Project board
- Assign to team members

**2. Development Phase**
- Create feature branch
- Make code changes
- Reference issue in commits
- Open **Pull Request**
- Add to Project (auto-moves to "In Review")

**3. Review Phase**
- Team reviews PR
- **Discussions** for design questions
- Address feedback
- Approvals received

**4. Deployment Phase**
- Merge PR (auto-closes issue)
- CI/CD deploys to GCP
- Update **Wiki** if needed
- Move card to "Done" in Project

**5. Documentation Phase**
- Update README
- Add to Wiki if needed
- Post in **Discussions** to share

### Example: Feature Development

**Scenario**: Add patient wait time analytics

**Issues:**
```
#123: [FEATURE] Add wait time data model
#124: [FEATURE] Create wait time API endpoints
#125: [FEATURE] Build wait time dashboard UI
#126: [DOCS] Document wait time calculations
```

**Project Board:**
```
To Do: #123, #124
In Progress: #125
Review: PR #130
Done: #126
```

**Pull Requests:**
```
PR #127: Add wait time data model (closes #123)
PR #128: Create wait time API (closes #124)
PR #129: Build dashboard UI (closes #125)
PR #130: Add documentation (closes #126)
```

**Wiki:**
```
New page: Wait Time Analytics Guide
Updated: API Reference
```

**Discussion:**
```
Topic: "Wait Time Analytics is Live!"
Category: Announcements
```

---

## Summary

### Key Takeaways

✅ **Repositories** are the foundation - organize them well  
✅ **Issues** track work - use templates and labels effectively  
✅ **Pull Requests** enable quality - review thoroughly  
✅ **Projects** organize work - visualize progress  
✅ **Wikis** document - keep knowledge accessible  
✅ **Discussions** foster community - encourage collaboration

### ABB Component Usage

| Component | Usage | Recommended For |
|-----------|-------|-----------------|
| **Issues** | ✅ Heavy | All task tracking |
| **Pull Requests** | ✅ Heavy | All code changes |
| **Projects** | ✅ Medium | Sprint planning |
| **Wikis** | ⚠️ Light | Internal docs |
| **Discussions** | ⚠️ Light | Q&A and ideas |

### Next Session Preview

In **Session 6: Using GitHub with Hybrid Workflows**, we'll explore:
- VS Code GitHub integration
- Working with GCP Cloud Code
- Developer workflow optimization
- IDE extensions and tools

---

## Additional Resources

- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [Pull Request Best Practices](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)
- [GitHub Projects Guide](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Discussions](https://docs.github.com/en/discussions)
- [GitHub Wikis](https://docs.github.com/en/communities/documenting-your-project-with-wikis)

---

*Session 5 of 7 | GitHub Training Package*  
*Aneurin Bevan University Health Board*
