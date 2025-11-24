# Session 3: GitHub On-Premises vs Cloud

**Duration**: 30 minutes  
**Time**: 10:15 - 10:45

## 🎯 Learning Objectives

By the end of this session, you will understand:
- Key differences between GitHub Enterprise Server and GitHub Enterprise Cloud
- Advantages and trade-offs of each deployment model
- GitHub Desktop for intuitive workflow management
- Using GitHub workflows for on-premises scenarios
- When to use desktop tools vs command line (as a last resort)
- When to use on-premises vs cloud solutions

---

## Deployment Models Overview

### The Two Main Options

| Feature | GitHub Enterprise Cloud | GitHub Enterprise Server |
|---------|------------------------|--------------------------|
| **Hosting** | GitHub's infrastructure (SaaS) | Your infrastructure (On-Prem) |
| **URL** | github.com | your-server.company.com |
| **Updates** | Automatic, continuous | Manual, scheduled |
| **Data Location** | GitHub's data centres | Your data centre |
| **Maintenance** | GitHub manages | You manage |
| **Cost Model** | Per-user subscription | License + infrastructure costs |

---

## GitHub Enterprise Cloud (github.com)

### Architecture

```
                    Internet
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
  Developer's              GitHub Cloud Infrastructure
   Computer                (Globally Distributed)
        │                             │
        │        HTTPS/SSH            │
        └─────────────────────────────┘
                       │
            ┌──────────┴──────────┐
            │                     │
        Repositories          CI/CD Actions
        Issues/PRs           Cloud Storage
```

### Key Features

#### ✅ Advantages

**1. Zero Infrastructure Management**
- No servers to maintain
- No operating system updates
- No database backups
- No capacity planning

**2. Always Latest Features**
- New features released weekly
- Security patches applied immediately
- No manual upgrades needed
- Beta features available first

**3. Global Performance**
- CDN-accelerated content delivery
- Low latency worldwide
- 99.9% uptime SLA
- Automatic scaling

**4. Enterprise Features**
- Advanced security and compliance
- SAML single sign-on (SSO)
- Audit log streaming
- Enterprise Managed Users (EMU)

**5. Ecosystem Integration**
- GitHub Marketplace with 1000+ apps
- GitHub Actions hosted runners
- GitHub Copilot integration
- GitHub Advanced Security

#### ⚠️ Considerations

**1. Internet Dependency**
- Requires internet connectivity
- Can't work during outages
- Latency for remote locations

**2. Data Location**
- Data stored in GitHub's data centres
- Subject to GitHub's data policies
- May have regulatory implications

**3. Customization Limits**
- Can't modify GitHub's infrastructure
- Limited to provided features
- Must wait for feature requests

### Pricing Structure

```
Enterprise Cloud Pricing (2024)
├── Base: £16-21 per user/month
├── GitHub Advanced Security: +£35 per active committer/month
├── GitHub Copilot Business: +£15 per user/month
└── Storage: 50GB included, then £0.20/GB/month
```

---

## GitHub Enterprise Server (On-Premises)

### Architecture

```
        Your Data Centre / Private Network
    ┌─────────────────────────────────────┐
    │                                     │
    │  ┌────────────────────────────┐    │
    │  │  GitHub Enterprise Server  │    │
    │  │    (Your VM/Hardware)      │    │
    │  │                            │    │
    │  │  ┌──────────────────────┐ │    │
    │  │  │  Git Repositories    │ │    │
    │  │  │  Database (MySQL)    │ │    │
    │  │  │  Storage Backend     │ │    │
    │  │  │  Actions Runners     │ │    │
    │  │  └──────────────────────┘ │    │
    │  └────────────────────────────┘    │
    │               │                     │
    └───────────────┼─────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
    Internal Network      (Optional)
    Developers            Internet
```

### Key Features

#### ✅ Advantages

**1. Complete Control**
- Full access to server infrastructure
- Custom backup and disaster recovery
- Network-level security controls
- Choose your own update schedule

**2. Data Sovereignty**
- All data stays on your premises
- Meet data residency requirements
- No third-party data access
- Comply with strict regulations

**3. Air-Gap Capability**
- Can run without internet connection
- Isolated network environments
- Enhanced security posture
- No external dependencies

**4. Integration with On-Prem Systems**
- Direct LDAP/Active Directory integration
- Internal CI/CD tool connections
- Legacy system compatibility
- Custom authentication systems

#### ⚠️ Considerations

**1. Infrastructure Requirements**
- Hardware or VM provisioning
- Operating system management
- Database administration
- Storage capacity planning

**2. Operational Overhead**
- Manual updates and patches
- 24/7 monitoring and support
- Backup and disaster recovery
- High availability setup

**3. Feature Lag**
- Features arrive 2-4 months after Cloud
- Must upgrade to get new features
- Testing required before upgrades
- Potential downtime for upgrades

**4. Cost Complexity**
- Server infrastructure costs
- IT staff for maintenance
- Backup storage costs
- High availability redundancy

### System Requirements

#### Minimum Configuration
```
CPU:      4 cores
RAM:      32 GB
Storage:  100 GB (root) + data storage
OS:       Ubuntu 20.04/22.04 or RHEL 8/9
```

#### Recommended Configuration (500-1000 users)
```
CPU:      8+ cores
RAM:      64+ GB
Storage:  500 GB+ SSD (root) + expandable data storage
Network:  1 Gbps+ connectivity
Backup:   Separate backup infrastructure
```

#### High Availability Setup
```
Primary:  Full GitHub Enterprise Server instance
Replica:  Synchronized replica for failover
Load Balancer: Distribute traffic
Shared Storage: Enterprise-grade SAN/NAS
```

---

## Detailed Comparison

### Feature Availability

| Feature | Cloud | Server | Notes |
|---------|-------|--------|-------|
| **Core Git** | ✅ | ✅ | Same functionality |
| **GitHub Actions** | ✅ | ✅ | Cloud has more hosted runners |
| **Advanced Security** | ✅ | ✅ | Feature parity |
| **Packages Registry** | ✅ | ✅ | Storage limits differ |
| **GitHub Copilot** | ✅ | ✅ | Cloud-only AI processing |
| **GitHub Projects** | ✅ | ✅ | Feature parity |
| **Marketplace Apps** | ✅ | ⚠️ | Limited on Server |
| **Discussion Forums** | ✅ | ✅ | Feature parity |
| **Wiki** | ✅ | ✅ | Feature parity |
| **Dependabot** | ✅ | ✅ | Feature parity |

✅ = Full Support | ⚠️ = Limited/Partial | ❌ = Not Available

### Security Features Comparison

| Security Feature | Cloud | Server |
|------------------|-------|--------|
| **Secret Scanning** | ✅ | ✅ |
| **Dependency Scanning** | ✅ | ✅ |
| **Code Scanning (CodeQL)** | ✅ | ✅ |
| **SAML SSO** | ✅ | ✅ |
| **LDAP Sync** | ❌ | ✅ |
| **IP Allow Lists** | ✅ | ✅ |
| **Audit Log Streaming** | ✅ | ✅ |
| **2FA Enforcement** | ✅ | ✅ |

### Compliance and Certifications

**GitHub Enterprise Cloud:**
- SOC 2 Type II
- ISO 27001, 27017, 27018
- FedRAMP Moderate (US)
- UK Cyber Essentials Plus
- GDPR compliant

**GitHub Enterprise Server:**
- You control compliance
- Inherits your infrastructure certifications
- Easier to meet strict data residency requirements
- Full audit control

---

## GitHub Desktop (Recommended Primary Tool)

### What is GitHub Desktop?

**GitHub Desktop** is a graphical user interface (GUI) application for Git and GitHub. It simplifies common workflows without needing command-line knowledge and is the **recommended primary tool** for most developers at ABB.

### Installation

1. Download from: https://desktop.github.com
2. Install (Windows or macOS)
3. Sign in with GitHub account
4. Configure Git settings

### Why GitHub Desktop is Recommended

✅ **User-Friendly**
- No command-line knowledge required
- Visual feedback for all operations
- Easier to learn for beginners
- Less error-prone than command line

✅ **Efficient Workflow**
- See all changes at once
- Intuitive branch management
- Visual merge conflict resolution
- Built-in pull request integration

✅ **Perfect for Daily Work**
- Faster for common tasks
- Real-time diff viewing
- Easy repository switching
- Integrated with github.com

### Key Features

#### Visual Interface
```
┌─────────────────────────────────────────┐
│ GitHub Desktop                      [X] │
├─────────────────────────────────────────┤
│ Current Repository: ABB_GitHub_Config   │
│ Current Branch: feature/training    [▼] │
├──────────────────┬──────────────────────┤
│ Changes (3)      │ Diff View            │
│ ☑ Training/      │  + Line added        │
│   README.md      │  - Line removed      │
│ ☑ Training/      │                      │
│   01_Intro.md    │  File contents with  │
│ ☐ Training/      │  visual diff         │
│   02_Basic.md    │                      │
├──────────────────┴──────────────────────┤
│ Summary: Add training materials         │
│ Description: (optional)                  │
│                                          │
│              [Commit to feature/...] │
└─────────────────────────────────────────┘
```

#### Core Capabilities

**1. Repository Management**
- Clone repositories with one click
- Create new repositories
- Add local repositories
- Switch between repositories easily

**2. Branch Operations**
- Visual branch switcher
- Create branches with dialog
- See branch history graphically
- Merge branches visually

**3. Commit Interface**
- See all changes at once
- Select files to commit
- Write commit messages with spell check
- Amend previous commits

**4. Sync Operations**
- Fetch/pull with progress indicator
- Push changes with conflict detection
- Automatic merge conflict detection
- Visual merge conflict resolution

**5. GitHub Integration**
- Create pull requests in-app
- View pull request status
- Clone from GitHub directly
- Open repositories in browser

### GitHub Desktop for On-Premises (GitHub Enterprise Server)

GitHub Desktop fully supports **GitHub Enterprise Server** installations:

**Setup:**
1. Open GitHub Desktop
2. Go to Preferences/Options → Accounts
3. Click "Sign in" next to "GitHub Enterprise Server"
4. Enter your server URL (e.g., `github.abb.wales.nhs.uk`)
5. Authenticate with your credentials

**Features:**
- Same interface for Cloud and Enterprise Server
- Clone enterprise repositories
- Create PRs on enterprise instance
- Manage issues and reviews
- Full offline support

### GitHub Workflows for On-Premises Use

When using **GitHub Enterprise Server**, you can leverage GitHub Actions workflows just like in the cloud:

**Benefits:**
- Automated testing and deployment
- CI/CD pipelines on your infrastructure
- Self-hosted runners for security
- Custom actions for your environment

**Example workflow for on-prem deployment:**
```yaml
name: Deploy to On-Prem Server

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: self-hosted  # Uses your on-prem runner
    steps:
      - uses: actions/checkout@v4
      
      - name: Build application
        run: npm run build
      
      - name: Deploy to internal server
        run: |
          rsync -avz dist/ user@internal-server:/var/www/app/
```

**Self-hosted runners:**
- Run on your own infrastructure
- Access to internal resources
- Custom software and tools
- Complete control over environment

---

## Command Line Interface (Last Resort)

### When to Use Command Line

While GitHub Desktop is recommended for most tasks, the **command line** may be needed for:

⚠️ **Advanced scenarios only:**
- Server administration tasks
- CI/CD pipeline scripts
- Complex Git operations (interactive rebase, cherry-pick)
- Automated scripts and tooling
- SSH-only environments

### Basic Command Line Reference

**Only if GitHub Desktop cannot accomplish the task:**
```bash
# Configuration (if needed)
git config --global user.name "John Smith"
git config --global user.email "john.smith@wales.nhs.uk"

# Basic operations (prefer GitHub Desktop for these)
git status
git pull
git push
```

**Important:** Before using command line, always check if GitHub Desktop can accomplish the task. Most operations are easier and safer in the GUI.

---

## GitHub Desktop (Recommended Primary Tool)

### ABB Tool Recommendations

**Primary Tool (Use First):**
- ✅ **GitHub Desktop** - For all daily development work

**Secondary Tools:**
- ✅ **VS Code Git Integration** - When working in your code editor
- ✅ **GitHub Web Interface** - For pull requests and code reviews

**Last Resort Only:**
- ⚠️ **Command Line** - Only for advanced scenarios or automation

---

## Choosing the Right Tool

### Decision Matrix

| Scenario | Recommended Tool | Why |
|----------|------------------|-----|
| **Daily commits** | GitHub Desktop | Visual, fast, intuitive |
| **Code review** | GitHub Web + VS Code | Best PR experience |
| **Branch management** | GitHub Desktop | Visual branch tree |
| **Merge conflicts** | GitHub Desktop | Visual resolver |
| **New to Git** | GitHub Desktop | Easiest to learn |
| **Creating PRs** | GitHub Desktop or Web | One-click creation |
| **CI/CD scripts** | Command line | Automation needs |
| **Server tasks** | Command line | No GUI available |

### ABB Best Practice Workflow

**1. Daily Development (GitHub Desktop)**
```
1. Open GitHub Desktop
2. Select repository
3. Create new branch (button click)
4. Make code changes in editor
5. Review changes in Desktop (visual diff)
6. Write commit message
7. Commit (button click)
8. Push (button click)
9. Create PR (button click)
```

**2. Code Review (GitHub Web)**
```
1. Receive PR notification
2. Open PR in browser
3. Review files and changes
4. Add inline comments
5. Approve or request changes
```

**3. Advanced Operations (Command Line - if needed)**
```
Only for: CI/CD, server admin, complex Git operations
```

---

## ABB Context: Why We Chose Cloud

### Decision Factors for ABB

The Aneurin Bevan University Health Board selected **GitHub Enterprise Cloud** because:

**1. Focus on Healthcare Delivery**
- IT resources focused on patient systems
- No need for GitHub infrastructure management
- Faster time to value
- Reduced operational complexity

**2. Modern Collaboration**
- Work with external consultants easily
- Support remote and hybrid working
- Enable global collaboration
- Access to latest features

**3. Integration Strategy**
- Already using Google Cloud Platform
- GitHub Actions for GCP CI/CD
- Cloud-first approach
- Modern DevOps practices

**4. Cost Effectiveness**
- Predictable per-user pricing
- No hardware investment
- No dedicated infrastructure team needed
- Scale up/down as needed

**5. Security and Compliance**
- GitHub's SOC 2 certification
- Advanced Security features
- Secret scanning and dependency review
- Audit logging

### Our Tool Recommendations

**For ABB Developers:**
- **Primary**: GitHub Desktop (easiest and safest)
- **Secondary**: VS Code Git integration (when coding)
- **Web Interface**: For pull requests and reviews
- **Command Line**: Only when absolutely necessary

---

## Practical Comparison Exercise

### Exercise: Same Task, Different Tools

**Task**: Update a README file

#### Using GitHub Desktop (Recommended)
```
1. Open GitHub Desktop
2. Click "Fetch origin" button (sync with remote)
3. Click "Current Branch" → "New Branch"
   - Name: docs/update-readme
   - Click "Create Branch"
4. Edit README.md in your preferred editor
5. Return to GitHub Desktop
6. See changes appear automatically with visual diff
7. Review changes (side-by-side view)
8. Check the checkbox next to README.md
9. Write commit message: "Update README with deployment info"
10. Click "Commit to docs/update-readme"
11. Click "Publish branch" (pushes to GitHub)
12. Click "Create Pull Request" button
13. PR opens in browser - fill details and create
```

**Time:** ~2 minutes | **Errors:** Minimal | **Recommended:** ✅

#### Using Command Line (Last Resort)
```bash
# Only use if GitHub Desktop unavailable
git pull origin main
git checkout -b docs/update-readme
# Edit README.md in editor
git add README.md
git commit -m "Update README with deployment info"
git push origin docs/update-readme
# Create PR on GitHub web
```

**Time:** ~3 minutes | **Errors:** Higher risk | **Use when:** No GUI available

**Conclusion:** GitHub Desktop is faster, safer, and more intuitive!

---

## Summary

### Key Takeaways

✅ **GitHub Enterprise Cloud**: SaaS, always updated, zero maintenance  
✅ **GitHub Enterprise Server**: On-premises, full control, data sovereignty  
✅ **GitHub Desktop**: Primary tool - visual, intuitive, safer (RECOMMENDED)  
✅ **VS Code Integration**: Secondary tool for coding workflows  
✅ **Command Line**: Last resort only - for automation and advanced scenarios  
✅ **ABB uses Cloud**: Aligned with cloud strategy and collaboration needs  
✅ **GitHub Workflows**: Enable automation for both cloud and on-premises

### Tool Priority for ABB

**1st Choice:** GitHub Desktop 🥇  
**2nd Choice:** VS Code Git Integration 🥈  
**3rd Choice:** GitHub Web Interface 🥉  
**Last Resort:** Command Line ⚠️

### Decision Guide

**Choose GitHub Enterprise Cloud if:**
- You want zero infrastructure management
- You need latest features immediately
- You collaborate with external partners
- You have a cloud-first strategy

**Choose GitHub Enterprise Server if:**
- You have strict data residency requirements
- You need air-gap capability
- You have existing on-premises infrastructure
- You require custom integrations

### Next Session Preview

In **Session 4: GitHub with GCP Context**, we'll explore:
- GitHub Actions with Google Cloud Build
- Deploying to GCP from GitHub
- Secret management for GCP
- CI/CD pipelines for cloud-native apps

---

## Additional Resources

- [GitHub Enterprise Cloud Documentation](https://docs.github.com/en/enterprise-cloud@latest)
- [GitHub Enterprise Server Documentation](https://docs.github.com/en/enterprise-server@latest)
- [Git CLI Official Documentation](https://git-scm.com/doc)
- [GitHub Desktop User Guides](https://docs.github.com/en/desktop)
- [Pro Git Book (Free)](https://git-scm.com/book/en/v2)

---

*Session 3 of 7 | GitHub Training Package*  
*Aneurin Bevan University Health Board*
