![BIU Logo](links%20and%20logos/BIU%20LOGO.png) ![DDAT Logo](links%20and%20logos/DDAT%20Logo.png)
---

# Session 1: Introduction to GitHub and Why GitHub for Data Teams?



**Duration**: 30 minutes  
**Time**: 09:00 - 09:30

## 🎯 Learning Objectives
By the end of this session, you will understand:
- What GitHub is and its fundamental purpose
- Why GitHub is essential for healthcare analytics teams
- Core Git concepts and terminology
- How version control improves collaboration and auditability
- The specific benefits for SQL, Python, and notebook workflows

---

## 📚 What is GitHub?

**GitHub** is a cloud-based platform for version control and collaboration that allows multiple people to work on projects from anywhere (Location and IDE [IDE = Integrated Development Environment]).

### Core Components

#### Git (The Engine/Language)
- **Version Control System**: Tracks changes to files over time
- **Distributed**: Every user has a complete copy of the project history
- **Branching**: Create separate lines of development for different features and developments

#### GitHub (The Platform)
- **Web Interface**: Visual way to interact with Git repositories
- **Collaboration Tools**: Issues, pull requests, project boards
- **Cloud Storage**: Secure, reliable hosting for your code and data
- **Permissions & Access Control**: Manage who can view and edit your code

### How It Works
```
Local Computer          GitHub Cloud
     ↓                       ↓
[Your Code] ----Push---→ [Repository]
     ↑                       ↓
[Updated Code] ←--Pull--- [Shared Changes]
```

### Key Benefits for Any Organization
- **Backup**: Never lose work - everything is saved and tracked
- **History**: See exactly what changed, when, and who changed it
- **Collaboration**: Multiple people can work on the same project safely
- **Transparency**: All changes are visible and documented
- **Modularity**: Break down projects into smaller, manageable components

---

## 🏥 What is GitHub GIG Cymru?

**GitHub GIG Cymru** is a collaborative platform enabling secure and efficient development and sharing of analytics tools/code across NHS Wales organisations.

### Purpose
Facilitate advanced analytics, data engineering, data science, and innovation in health and care by breaking down silos and fostering collaboration.

### Key Benefits

#### Faster Development
- Remove technical barriers for collaborative work
- Reduce development timeframes through shared resources
- Enable rapid iteration and testing of analytics solutions

#### Enhanced Security
- Ensure secure code sharing within approved protocols
- Improve data protection through controlled access
- Maintain audit trails for compliance requirements

#### Improved Insights
- Enable efficient communication and partnership
- Facilitate code reuse for impactful healthcare insights
- Leverage collective intelligence across NHS Wales
- Acts as a change log for all modifications (this can be surfaced in pull requests and via GitHub API)


### Key Features

#### Secure Code Repository
- Central hub for storing, sharing, and collaborating on code
- Version control for all changes and iterations
- Backup and recovery capabilities

#### Collaboration Tools
- Enables teamwork across different NHS Wales organisations and ABUHB Departments
- Version control prevents conflicts and data loss
- Efficient project management and task tracking
- Enables external collaboration with partners and stakeholders 

#### Governance Framework
- Adheres to information governance requirements
- Complies with data handling regulations
- Maintains security standards for data

---

## Why GitHub for Data Teams?

### 1. Collaboration and Auditability

#### For SQL Development
```sql
-- Before: SQL files shared via email or network drives
-- Issues: Version conflicts, no change tracking, no review process

-- After: SQL in GitHub repositories
-- Benefits: Every change tracked, reviewed, and documented
```


#### For Python Analytics
```python
# Before: Python scripts in personal folders
# Issues: Code duplication, no standardization, limited sharing

# After: Centralized Python repositories
# Benefits: Shared libraries, consistent coding standards, collaborative development
```


#### For Jupyter Notebooks
- **Version Control**: Track changes to analysis workflows
- **Collaboration**: Multiple data scientists working on the same research
- **Reproducibility**: Ensure analyses can be repeated and verified
- **Documentation**: Combine code, results, and explanations

### 2. Single Source of Truth

#### Traditional Problems
- Multiple versions of the same data products scattered across systems 
- Uncertainty about which version is "current" or "approved" (v2, v2 Final, V2 Final Dan, V2 Final Prod)
- Difficulty tracking who made what changes when

#### GitHub Solution
- **One canonical repository** for each project, product, deployment or analysis
- **Clear branching strategy** for development vs. production
- **Tagged releases** for specific versions (e.g., "Q1-2024-Report")
- **Protected main branch** ensures only reviewed code reaches production

### 3. Rollback Capability

#### Scenario: Production Issue
```bash
# Problem: New SQL query causing performance issues
# Traditional approach: Manual restoration from backups

# GitHub approach: Simple rollback to previous working version
git revert <commit-hash>
# or
git reset --hard <previous-commit> # This statement using --hard means discarding all changes after the specified commit
```



### 4. Traceability Between Code, Tests, and Deployments

#### Complete Development Lifecycle
```
Issue Created → Branch Created → Code Developed → Tests Added → 
PR Opened → Code Reviewed → Merged → Deployed → Issue Closed
```

#### Compliance Benefits
- **Regulatory Audits**: Complete history of all changes
- **Quality Assurance**: Link between requirements and implementation
- **Risk Management**: Impact analysis for all modifications
- **Knowledge Transfer**: Documentation of decisions and rationale

---

## 🎓 Key Concepts Recap

### Core Git/GitHub Concepts

| Concept | Healthcare Analytics Context | Example |
|---------|----------------------------|---------|
| **Repository** | Project folder for analytics work | `patient-pathway-analysis` |
| **Commit** | Snapshot of your analysis at a point in time | "Add diabetes risk calculation" |
| **Branch** | Independent development line | `feature/RTT_Pop_up` |
| **Pull Request** | Request to review and merge changes | Code review for new DAG implementation |
| **Remote** | Shared repository on GitHub | Central repo for AB Tools |

> **Note**: These concepts will be explored in depth in Session 2 (Introduction to GIT), where you'll learn how GIT's architecture makes these features possible.

---

## 🏗️ Setting Up for Success

### Repository Structure for Healthcare Analytics

```
analytics-project/
├── README.md                 # Project overview and setup
├── sql/
│   ├── extracts/           # Data extraction queries
│   ├── transforms/         # Data transformation logic
│   └── reports/            # Reporting queries
├── python/
│   ├── src/                # Source code modules
│   ├── notebooks/          # Jupyter notebooks for analysis
│   └── tests/              # Unit tests for validation
├── docs/
│   ├── methodology/        # Analysis methodology documentation
│   ├── results/            # Analysis results and insights
│   └── compliance/         # Regulatory and governance docs
└── deployment/
    ├── configs/            # Configuration files
    └── scripts/            # Deployment automation
```

### 📦 Repository Provisioning (HALO Ticket Process)

All new repositories in ABUHB GitHub GIG Cymru require a **HALO ticket** before creation. This ensures governance, consistency, and auditability.

#### Why a HALO ticket?

- Enforces naming, visibility defaults (private unless justified)
- Confirms data classification (e.g. no patient identifiable data unless approved controls)
- Captures initial access (teams, maintainers) for least‑privilege
- Links purpose → approval → configuration for audit
- Provides change traceability to future Terraform updates

#### Required HALO Fields

| Field | Description |
|-------|-------------|
| Proposed Name | Kebab/snake case, clear scope (e.g. `emergency-flow-analytics`) |
| Purpose / Scope | One concise paragraph of intent |
| Data Classification | None / Aggregated / Synthetic / (if sensitive → controls) |
| Maintainers | Initial responsible users/teams |
| Team Access Matrix | Teams + permission levels (admin / maintain / write / triage / read) |
| Visibility | Usually `private` (public requires explicit approval) |
| Compliance Notes | IG considerations, validation requirements |
| Dependencies | Upstream data sources / scheduled jobs |
| Terraform Timing | Immediate / Scheduled batch |
| HALO Reference | Ticket ID for audit (stored in repo description if needed) |

#### Approval & Deployment Flow

1. Analyst submits HALO ticket with required fields.
2. Governance review: naming, classification, access sanity check.
3. GitHub Admin updates `terraform.tfvars` (adds repo block) in a feature branch.
4. Terraform plan runs in secure Codespace; plan artifact attached to PR & HALO.
5. CODEOWNERS / second reviewer approves.
6. **Terraform apply (currently admin-only)** executed by GitHub Admin in Codespace.
7. Repo appears; URL and team slugs posted back to HALO ticket; ticket closed.

> Self-service creation will be reassessed once policy-as-code maturity increases (see Session 8 roadmap). Until then, **no new repos without HALO + admin Terraform apply**.

> Looking Ahead: Session 8 details Terraform governance and why restricting apply reduces configuration drift and risk.


### Naming Conventions

#### Branch Names

- `feature/new_api_onboarding`
- `bugfix/measure_Count`
- `data/new-patient-pathway-source`
- `hotfix/urgent_data_sync`

#### Commit Messages

```text
Add patient risk stratification model

- Implement logistic regression for admission risk
- Include age, comorbidities, and prior admissions
- Add validation against historical data
- Update documentation with model methodology

Closes #123
```

#### File Organization

- `extract_patient_data.sql` (descriptive, action-based)
- `transform_demographics.py` (clear purpose)
- `analyze_emergency_admissions.ipynb` (specific analysis)

---



**Discussion Points**

1. How does this workflow improve on email-based collaboration?
2. What compliance benefits does this provide for NHS Wales?
3. How would you handle an urgent bug fix in this system?
4. What happens if two analysts modify the same SQL file?

---

## Key Takeaways

### For Data Teams:

1. **Version Control is Essential**
   - NHS/Public Sector data must be accurate and auditable
   - Git provides the foundation for both requirements

2. **Collaboration Improves Quality**
   - Code review catches errors before they impact patient care
   - Shared knowledge leads to better analytical approaches

3. **Standardization Enables Scale**
   - Consistent processes across NHS Wales
   - Reusable components and methodologies

4. **Compliance is Built-In**
   - Audit trails and approval processes
   - Documentation and traceability requirements

### Success Metrics:
- Reduced time from analysis idea to implementation
- Improved accuracy through code review
- Increased collaboration across NHS Wales sites
- Enhanced compliance and audit readiness

---

## 🎯 Next Session Preview

**Session 2: Introduction to GIT**
- Understanding GIT as a version control system
- GIT's core architecture and object model
- The three-tree architecture: working directory, staging area, and repository
- How GIT tracks changes and ensures data integrity
- The distributed model and its benefits for NHS Wales teams

---

## 📖 Additional Resources

- [GitHub for Healthcare Analytics Best Practices](../Technical_Configuration/README.md)
- [ABUHB Wales GitHub Setup Guide](../Technical_Configuration/2.%20New_Repo_Setup.md)

---

*Session 1 of 8 | GitHub GIG Cymru Training Series*
*ABUHB BIU | Business Intelligence Unit*