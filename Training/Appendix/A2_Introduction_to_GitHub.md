# Session 1: Introduction to GitHub

**Duration**: 30 minutes  
**Time**: 09:00 - 09:30

## 🎯 Learning Objectives

By the end of this session, you will understand:
- What GitHub is and why organisations use it
- The core components of GitHub's architecture
- The differences between GitHub Cloud and GitHub Enterprise Server (On-Premises)
- How GitHub fits into modern software development

---

## What is GitHub?

### Definition

**GitHub** is a cloud-based platform for version control and collaboration built on top of **Git**, the distributed version control system created by Linus Torvalds in 2005. GitHub has the ability to work in Hybrid enviroments using desktop tools.

### Key Purpose

GitHub enables teams to:
- **Store code** in repositories with full version history and premissions
- **Collaborate** on projects with multiple contributors internal and external to your organisation 
- **Track changes** and review code before merging - autoamted using co-pilot or, by notifiaction to team members
- **Manage projects** with integrated issue tracking and planning tools 
- **Automate workflows** with CI/CD pipelines
- **Document** projects with wikis and README files 

### The Git Foundation

GitHub is built on **Git**, which means:
- Every contributor has a complete copy of the repository history
- Work can be done offline and synchronized later
- Branching and merging are fast and efficient
- Changes are tracked with cryptographic integrity

---

## GitHub Architecture

### Cloud-Based Platform (github.com)

```
┌─────────────────────────────────────────────────────┐
│                   GitHub Cloud                      │
│                  (github.com)                       │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Repositories │  │   Actions    │  │  Issues   │ │
│  │   Storage    │  │   (CI/CD)    │  │  Tracking │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Pull Requests│  │   Projects   │  │   Wikis   │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │      GitHub API & Integration Layer          │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
           │                          │
           ▼                          ▼
    ┌─────────────┐          ┌──────────────┐
    │   Git CLI   │          │    GitHub    │
    │   Commands  │          │   Desktop    │
    └─────────────┘          └──────────────┘
```

### Key Cloud Infrastructure

- **Global CDN**: Fast access from anywhere in the world
- **Redundant Storage**: Multiple data centres for reliability
- **Scalable Compute**: Dynamic resources for CI/CD and Actions 
- **Integrated Security**: Secret scanning, dependency analysis, CodeQL
- **99.9% Uptime SLA**: Enterprise-grade reliability

---

## GitHub Deployment Models

### 1. GitHub Cloud (github.com)

**Hosted by GitHub** - Software as a Service (SaaS)

#### Characteristics
- ✅ **Fully Managed**: GitHub handles infrastructure, updates, and maintenance
- ✅ **Always Up-to-Date**: New features released continuously
- ✅ **Global Availability**: Access from anywhere with internet
- ✅ **Scalability**: Unlimited repositories and storage (on paid plans)
- ✅ **Integrated Marketplace**: Access to thousands of apps and actions

#### Best For
- Teams that want quick setup without infrastructure management
- Organisations comfortable with cloud-based/Hybrid tools
- Projects requiring global collaboration
- Teams using other cloud services (AWS, Azure, GCP)

#### ABB Context
The Aneurin Bevan University Health Board uses **GitHub Enterprise Cloud** for:
- Business Intelligence Unit repositories
- Public Health Nursing development
- Organisation-wide collaboration
- Integration with Google Cloud Platform

---

## How GitHub Works: The Development Flow

### Basic Workflow

```
Developer's Computer                    GitHub Cloud/Server
─────────────────────                   ───────────────────

1. Clone Repository
   git clone <url>      ────────────►   Repository
         │
         ▼
2. Create Branch
   git branch feature
   git checkout feature
         │
         ▼
3. Make Changes
   Edit files
   git add .
   git commit -m "message"
         │
         ▼
4. Push to Remote
   git push origin feature  ────────►   Feature Branch
                                              │
                                              ▼
5. Create Pull Request    ◄──────────   Review & Discuss
                                              │
                                              ▼
6. Code Review                           Approve/Request Changes
                                              │
                                              ▼
7. Merge to Main          ◄──────────   Merge Pull Request
         │
         ▼
8. Pull Latest
   git pull origin main   ◄────────────  Updated Main Branch
```

---

## Why Organisations Choose GitHub

### 1. **Collaboration at Scale**
- Thousands of contributors can work on the same project
- Clear ownership and responsibility through teams
- Code review processes built into the workflow

### 2. **Transparency and Visibility**
- All changes are tracked with full history
- Discussions and decisions are documented
- Easy to audit who changed what and why

### 3. **Automation and DevOps**
- GitHub Actions for CI/CD pipelines
- Automated testing and deployment
- Integration with cloud platforms and tools

### 4. **Security and Compliance**
- Dependency vulnerability scanning
- Secret detection and prevention
- Audit logs and compliance reporting
- SOC 2, ISO 27001 certified

### 5. **Developer Experience**
- Industry-standard tool with massive community
- Excellent documentation and learning resources
- Rich ecosystem of integrations and tools
- AI-powered coding with GitHub Copilot

---

## GitHub in Healthcare Context

### Why NHS/Healthcare Organizations Use GitHub

1. **Code Quality**: Peer review ensures clinical systems are thoroughly checked
2. **Audit Trail**: Complete history for regulatory compliance
3. **Collaboration**: Teams across sites can work together effectively
4. **Security**: Enterprise features protect sensitive development work
5. **Standards**: Follows industry best practices for software development

### Important Considerations

⚠️ **Data Sensitivity**
- Source code ≠ patient data
- GitHub is for code and documentation, not PHI (Protected Health Information)
- All repositories should be private unless specifically approved
- Secrets (passwords, API keys) must never be committed

⚠️ **Compliance**
- Follow NHS Digital Technology Standards
- Adhere to data protection regulations (GDPR, UK DPA)
- Maintain audit logs for all changes
- Regular security reviews and scanning

---

## Key Terminology

| Term | Definition |
|------|------------|
| **Repository (Repo)** | A project folder containing all files and their history |
| **Clone** | Creating a local copy of a repository |
| **Commit** | A saved snapshot of changes with a message |
| **Branch** | A parallel version of the code for isolated development |
| **Merge** | Combining changes from one branch into another |
| **Pull Request (PR)** | A request to merge changes with review process |
| **Fork** | A personal copy of someone else's repository |
| **Remote** | A version of the repository hosted on a server |
| **Origin** | The default name for the remote repository |
| **Main/Master** | The primary branch of the repository |

---

## Hands-On: Explore GitHub

### Activity: Navigate GitHub Cloud

1. **Visit**: https://github.com/Aneurin-Bevan-University-Health-Board
2. **Explore**: Browse public repositories
3. **Observe**: Notice the structure - code, issues, pull requests, etc.
4. **Navigate**: Click through to see how projects are organized

### Questions to Consider

- How many public repositories does the organisation have?
- What types of projects are being developed?
- How are teams organized?
- What information is available in README files?

---

## Summary

### Key Takeaways

✅ GitHub is a platform for version control, collaboration, and DevOps  
✅ Built on Git, providing distributed version control capabilities  
✅ Available as Cloud (SaaS) or Enterprise Server (On-Premises)  
✅ ABB uses GitHub Enterprise Cloud for organisation-wide development  
✅ Enables secure, auditable, and collaborative software development  
✅ Essential for modern healthcare IT development practices

### Next Session Preview

In **Session 2: Basic GitHub Concepts**, we'll dive deeper into:
- Commits and how they work
- Branching strategies
- Pull requests and code review
- Forks and collaboration models

---

## Additional Resources

- [GitHub Docs](https://docs.github.com)
- [GitHub Enterprise Cloud Documentation](https://docs.github.com/en/enterprise-cloud@latest)
- [Git Documentation](https://git-scm.com/doc)
- [ABB GitHub Configuration Repository](../README.md)

---

*Session 1 of 7 | GitHub Training Package*  
*Aneurin Bevan University Health Board*
