# Appendix A7: Using GitHub with Hybrid Workflows

**Duration**: 30 minutes (self-directed)

## 🎯 Learning Objectives

By the end of this session, you will understand:
- How to integrate GitHub with VS Code for seamless development
- Using GitHub with Google Cloud Platform tools
- GitHub Codespaces for cloud-based development
- Optimizing your developer workflow with IDE extensions
- Best practices for hybrid (local + cloud) development
- Keyboard shortcuts and productivity tips

---

## VS Code and GitHub Integration

### Why VS Code?

**Visual Studio Code** is the most popular code editor and integrates deeply with GitHub:

- Built-in Git support
- GitHub Pull Requests and Issues extension
- GitHub Copilot integration
- Live collaboration features
- Rich extension ecosystem
- Free and open source

### Setting Up VS Code for GitHub

#### 1. Install VS Code
```bash
# Windows (using Chocolatey)
choco install vscode

# macOS (using Homebrew)
brew install --cask visual-studio-code

# Linux (Ubuntu/Debian)
sudo snap install code --classic
```

#### 2. Sign in to GitHub
```
1. Open VS Code
2. Click account icon (bottom left)
3. Select "Sign in to sync settings"
4. Choose "Sign in with GitHub"
5. Authorize in browser
```

#### 3. Essential Extensions

**GitHub Extensions:**
```
1. GitHub Pull Requests and Issues
   - ID: GitHub.vscode-pull-request-github
   - Manage PRs and issues from VS Code

2. GitHub Copilot
   - ID: GitHub.copilot
   - AI-powered code completion

3. GitHub Copilot Chat
   - ID: GitHub.copilot-chat
   - Conversational AI assistant

4. GitLens
   - ID: eamodio.gitlens
   - Supercharge Git capabilities
```

**GCP Extensions:**
```
5. Cloud Code
   - ID: GoogleCloudTools.cloudcode
   - Deploy to GCP from VS Code

6. Cloud Run
   - ID: GoogleCloudTools.cloudrun
   - Manage Cloud Run services
```

**General Development:**
```
7. Python
   - ID: ms-python.python
   
8. ESLint
   - ID: dbaeumer.vscode-eslint
   
9. Prettier
   - ID: esbenp.prettier-vscode
   
10. Remote - SSH
    - ID: ms-vscode-remote.remote-ssh
```

### Installing Extensions

**Via VS Code:**
```
1. Click Extensions icon (Ctrl+Shift+X)
2. Search for extension name
3. Click "Install"
```

**Via Command Line:**
```bash
# Install multiple extensions at once
code --install-extension GitHub.vscode-pull-request-github
code --install-extension GitHub.copilot
code --install-extension GoogleCloudTools.cloudcode
code --install-extension eamodio.gitlens
```

---

## Built-in Git Features

### Source Control View

**Access:** Click Source Control icon (Ctrl+Shift+G)

```
┌─────────────────────────────────────┐
│ SOURCE CONTROL: GIT                │
├─────────────────────────────────────┤
│ Changes (3)                    [+] │
│ ☑ Modified                         │
│   M  src/components/Dashboard.tsx  │
│   M  src/utils/api.ts              │
│ ☐ Untracked                        │
│   U  src/components/NewWidget.tsx  │
├─────────────────────────────────────┤
│ Message: Add dashboard widget      │
│                               [✓]  │
└─────────────────────────────────────┘
```

### Common Git Operations in VS Code

#### Staging Changes
```
Method 1: Click + icon next to file
Method 2: Right-click file → Stage Changes
Method 3: Stage All Changes button
```

#### Committing
```
1. Type commit message in text box
2. Click ✓ (checkmark) or press Ctrl+Enter
3. Choose "Commit" or "Commit & Push"
```

#### Branching
```
Bottom left corner shows current branch
├── Click branch name
├── Select "Create new branch"
├── Type branch name: feature/new-widget
└── Press Enter
```

#### Pulling and Pushing
```
Method 1: Click "..." menu → Pull/Push
Method 2: Click sync icon in status bar
Method 3: Command Palette (Ctrl+Shift+P) → Git: Pull
```

### Viewing Changes

**Diff View:**
```
Side-by-side comparison:
├── Original (left)    │  Modified (right)
├── Line 10: old code  │  Line 10: new code
└── Red = removed      │  Green = added
```

**Inline Diff:**
- Click file in Source Control
- Changes shown with highlighting
- Click gutter to stage individual lines

### Git Timeline

```
TIMELINE (bottom of Explorer)
├── 2 hours ago - Add dashboard widget (@you)
├── 5 hours ago - Fix API endpoint (@teammate)
├── Yesterday - Update dependencies (@you)
└── 2 days ago - Initial commit (@teammate)
```

---

## GitHub Pull Requests Extension

### Features Overview

The **GitHub Pull Requests and Issues** extension brings GitHub into VS Code.

### Setting Up

```
1. Install extension
2. Sign in to GitHub (if not already)
3. Extension detects GitHub repositories
4. Access via GitHub icon in Activity Bar
```

### Managing Pull Requests

#### View All PRs
```
GITHUB PULL REQUESTS
├── Assigned to Me (2)
│   ├── #234 - Fix date calculation
│   └── #235 - Add authentication
├── Created by Me (1)
│   └── #236 - Update documentation
├── Waiting For My Review (3)
│   ├── #237 - Dashboard improvements
│   ├── #238 - Bug fix in API
│   └── #239 - Performance optimization
└── All Open PRs (12)
```

#### Create Pull Request from VS Code

```
Method 1: Command Palette
1. Ctrl+Shift+P
2. "GitHub Pull Requests: Create Pull Request"
3. Fill in details
4. Click "Create"

Method 2: Source Control
1. Push branch
2. Click "Create Pull Request" notification
3. Fill in details
4. Click "Create"
```

#### Review Pull Requests

```
1. Click PR in GitHub view
2. Opens PR description and files
3. View changes inline
4. Add comments on specific lines
5. Submit review (Comment/Approve/Request Changes)
```

**Review Commands:**
```
💬 Add Comment:        Click line → Add comment
✅ Approve:            Click "Approve" button
⚠️ Request Changes:    Click "Request Changes"
💭 Start Review:       Begin multi-comment review
✓ Submit Review:       Send all comments at once
```

#### Checkout PR Locally

```
1. Right-click PR in GitHub view
2. Select "Checkout Pull Request"
3. Branch downloaded and checked out
4. Test and review locally
5. Add review comments from VS Code
```

### Managing Issues

#### View Issues
```
GITHUB ISSUES
├── Assigned to Me (5)
│   ├── #123 - Fix dashboard bug
│   ├── #124 - Add filtering
│   └── ...
├── Created by Me (2)
└── All Open Issues (45)
```

#### Create Issue

```
1. Ctrl+Shift+P → "GitHub Issues: Create Issue"
2. Enter title
3. Enter description
4. Add labels
5. Assign to someone
6. Create issue
```

#### Work on Issue

```
1. Right-click issue
2. "Start Working on Issue"
3. Creates branch: issue-123-fix-dashboard-bug
4. Automatically checks out branch
5. Make changes and commit
6. Create PR that references issue
```

---

## GitLens Extension

### What is GitLens?

**GitLens** supercharges Git in VS Code with advanced features.

### Key Features

#### 1. **Blame Annotations**

```
Inline blame (hover over line):
┌─────────────────────────────────────────────┐
│ John Smith, 2 days ago                      │
│ Fix date calculation in reporting module    │
│ commit abc123                               │
└─────────────────────────────────────────────┘
```

#### 2. **File History**

```
Right-click file → "Open File History"

Shows all commits that modified this file:
├── abc123 - Fix date calculation (2 days ago)
├── def456 - Add new column (1 week ago)
├── ghi789 - Initial implementation (2 weeks ago)
└── ...
```

#### 3. **Line History**

```
Right-click line → "Open Line History"

Shows all commits that changed this specific line:
├── abc123 - Changed condition (2 days ago)
├── def456 - Added validation (1 month ago)
└── ghi789 - Initial code (3 months ago)
```

#### 4. **Compare**

```
Compare:
├── Working Tree vs HEAD
├── Working Tree vs Branch
├── Branch vs Branch
└── Commit vs Commit
```

#### 5. **Git Graph**

```
Visual representation of repository history:

main ──●──●──●──────●──●──►
        \      \    /
feature  ●──●──●   /
                  /
hotfix ──────────●
```

### GitLens Configuration

**Settings.json:**
```json
{
  "gitlens.currentLine.enabled": true,
  "gitlens.codeLens.enabled": true,
  "gitlens.hovers.currentLine.over": "line",
  "gitlens.blame.highlight.enabled": true,
  "gitlens.blame.format": "${author}, ${date} • ${message}",
  "gitlens.advanced.messages": {
    "suppressLineUncommittedWarning": true
  }
}
```

---

## Cloud Code for VS Code

### What is Cloud Code?

**Cloud Code** brings GCP development directly into VS Code.

### Features

#### 1. **Deploy to Cloud Run**

```
1. Open Command Palette (Ctrl+Shift+P)
2. "Cloud Code: Deploy to Cloud Run"
3. Select service name
4. Choose region: europe-west2
5. Set environment variables
6. Click "Deploy"
7. Monitor deployment in terminal
8. Service URL provided when complete
```

#### 2. **Deploy to GKE**

```
1. "Cloud Code: Deploy to GKE"
2. Select cluster
3. Configure deployment
4. Monitor pod status
5. View logs in VS Code
```

#### 3. **Cloud Run Development**

**Local Development:**
```
1. "Cloud Code: Run on Cloud Run Emulator"
2. Test locally with Cloud Run environment
3. Hot reload on file changes
4. Debug with breakpoints
5. Deploy when ready
```

#### 4. **Secret Management**

```
Access GCP Secret Manager:
1. Cloud Code sidebar
2. Select "Secret Manager"
3. View/create/update secrets
4. Use in deployments
```

#### 5. **Log Viewing**

```
Real-time log streaming:
├── Cloud Run logs
├── GKE pod logs
├── Cloud Functions logs
└── Filter by severity/time
```

### Cloud Code Configuration

**Create `.vscode/launch.json`:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Cloud Run: Run/Debug Locally",
      "type": "cloudcode.cloudrun",
      "request": "launch",
      "build": {
        "docker": {
          "path": "Dockerfile"
        }
      },
      "image": "analytics-dashboard",
      "service": {
        "name": "analytics-dashboard",
        "containerPort": 8080,
        "resources": {
          "limits": {
            "memory": "512Mi"
          }
        }
      },
      "target": {
        "minikube": {}
      },
      "watch": true
    }
  ]
}
```

---

## Integrated Terminal

### Git Commands in Terminal

VS Code includes a fully integrated terminal:

**Open Terminal:**
```
View → Terminal
Or: Ctrl+` (backtick)
```

**Multiple Terminals:**
```
Click + to create new terminal
Split terminal with split icon
Switch between terminals in dropdown
```

**Run Git Commands:**
```bash
# Status
git status

# Create branch
git checkout -b feature/new-widget

# Commit
git add .
git commit -m "Add new widget"

# Push
git push origin feature/new-widget

# GCP commands
gcloud run deploy my-service --source .
```

---

## Productivity Tips and Shortcuts

### Essential Keyboard Shortcuts

#### General
```
Ctrl+Shift+P        Command Palette
Ctrl+P              Quick Open (files)
Ctrl+B              Toggle Sidebar
Ctrl+`              Toggle Terminal
Ctrl+Shift+E        Explorer
Ctrl+Shift+G        Source Control
Ctrl+Shift+D        Debug
Ctrl+Shift+X        Extensions
```

#### Editing
```
Ctrl+D              Select next occurrence
Ctrl+Shift+L        Select all occurrences
Alt+Up/Down         Move line up/down
Shift+Alt+Up/Down   Copy line up/down
Ctrl+/              Toggle line comment
Ctrl+Shift+K        Delete line
Ctrl+Space          Trigger suggestions
```

#### Git Operations
```
Ctrl+Shift+G        Open Source Control
Ctrl+Enter          Commit (in Source Control)
Ctrl+Shift+G G P    Pull
Ctrl+Shift+G G P S  Push
```

#### Search and Replace
```
Ctrl+F              Find
Ctrl+H              Replace
Ctrl+Shift+F        Find in files
Ctrl+Shift+H        Replace in files
```

### VS Code Git Workflow

**Typical Daily Workflow:**

```bash
Morning:
1. Ctrl+Shift+G         # Open Source Control
2. Pull latest          # Sync with team
3. Ctrl+Shift+P         # Command Palette
4. "Git: Create Branch" # Start new feature

Development:
5. Write code
6. Ctrl+S              # Save (auto-commits in some setups)
7. View changes inline # Diff view
8. Stage changes       # + icon in Source Control

Commit:
9. Ctrl+Shift+G        # Source Control
10. Write message      # Descriptive commit message
11. Ctrl+Enter         # Commit
12. Sync               # Push to GitHub

Pull Request:
13. Ctrl+Shift+P                              # Command Palette
14. "GitHub Pull Requests: Create Pull Request"
15. Fill details and create
```

---

## Hybrid Workflow Best Practices

### Local vs Cloud Development

#### Local Development
```
✅ Use for:
- Rapid iteration
- Debugging
- Offline work
- Fast feedback loops
- Testing

Tools:
- VS Code with local Git
- Local Node.js/Python
- Docker Desktop
- Git CLI
```

#### Cloud Development
```
✅ Use for:
- Integration testing
- Performance testing
- Production-like environment
- Team collaboration
- Final validation
- Working from any device

Tools:
- GitHub Codespaces (cloud-based VS Code)
- Cloud Run emulator
- GCP testing projects
- Cloud Build
- GitHub Actions
```

---

## GitHub Codespaces

### What are GitHub Codespaces?

**GitHub Codespaces** provides a complete, cloud-based development environment accessible from your browser or VS Code. It's like having VS Code in the cloud with your repository ready to code!

### Key Benefits

✅ **Instant Setup**
- Pre-configured development environment
- All dependencies installed automatically
- No local setup required
- Start coding in seconds

✅ **Consistent Environment**
- Same setup for all team members
- No "works on my machine" problems
- Defined in repository configuration
- Reproducible across team

✅ **Work from Anywhere**
- Access from any device
- Browser-based or local VS Code
- No need for powerful local machine
- Continue work across devices

✅ **Resource Flexibility**
- Choose machine size (2-32 cores)
- Scale resources as needed
- Don't burden local machine
- Perfect for resource-intensive tasks

### Creating a Codespace

#### Method 1: From GitHub Web
```
1. Navigate to repository on github.com
2. Click green "Code" button
3. Select "Codespaces" tab
4. Click "Create codespace on main"
5. Wait ~30 seconds for setup
6. VS Code opens in browser
7. Start coding!
```

#### Method 2: From VS Code Desktop
```
1. Open VS Code
2. Install "GitHub Codespaces" extension
3. Ctrl+Shift+P → "Codespaces: Create New Codespace"
4. Select repository
5. Codespace opens in VS Code desktop
```

### Codespace Configuration

Create `.devcontainer/devcontainer.json` in your repository:

```json
{
  "name": "ABB Analytics Development",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18"
    },
    "ghcr.io/devcontainers/features/gcloud:1": {}
  },
  
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot",
        "GitHub.vscode-pull-request-github",
        "ms-python.python",
        "GoogleCloudTools.cloudcode"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "editor.formatOnSave": true
      }
    }
  },
  
  "postCreateCommand": "pip install -r requirements.txt && npm install",
  
  "forwardPorts": [3000, 8080],
  
  "portsAttributes": {
    "3000": {
      "label": "Application",
      "onAutoForward": "notify"
    }
  }
}
```

### Key Configuration Options

**Base Image:**
- Python: `mcr.microsoft.com/devcontainers/python:3.11`
- Node.js: `mcr.microsoft.com/devcontainers/javascript-node:18`
- Universal: `mcr.microsoft.com/devcontainers/universal:2`

**Features (add tools):**
- Git: Pre-installed
- GCloud CLI: `ghcr.io/devcontainers/features/gcloud:1`
- Docker: `ghcr.io/devcontainers/features/docker-in-docker:1`

**Extensions (auto-install):**
- GitHub Copilot
- Python/Node.js support
- Cloud Code for GCP
- GitLens

**Lifecycle Scripts:**
- `postCreateCommand`: Run after creation (install dependencies)
- `postStartCommand`: Run each time codespace starts
- `postAttachCommand`: Run when attaching to codespace

### Using Codespaces

#### Basic Operations

**Access Terminal:**
```
Ctrl+` opens integrated terminal
Full access to git, npm, pip, gcloud, etc.
```

**Port Forwarding:**
```
Ports listed in devcontainer.json automatically forward
Access via provided URL: https://xyz-3000.preview.app.github.dev
Share with team for demos
```

**File Sync:**
```
All changes automatically saved to cloud
Committed changes sync via Git
Can continue on different device
```

**GitHub Integration:**
```
Authenticated with your GitHub account
Create branches, commits, PRs normally
Use GitHub Desktop workflows in browser
```

#### Development Workflow in Codespaces

```
1. Open Codespace (from repository)
   ↓
2. Create feature branch (Source Control)
   ↓
3. Make code changes
   ↓
4. Run application (npm start / python app.py)
   ↓
5. Test via forwarded port
   ↓
6. Commit changes (Source Control panel)
   ↓
7. Push and create PR
   ↓
8. Close Codespace (stops billing)
```

### ABB Use Cases for Codespaces

**1. Quick Bug Fixes**
- Open Codespace from issue
- Fix bug in cloud environment
- Create PR directly
- No local setup needed

**2. Code Reviews with Testing**
- Open Codespace on PR branch
- Test changes live
- Verify functionality
- Comment with confidence

**3. Onboarding New Team Members**
- Share repository with devcontainer
- New joiner creates Codespace
- Environment ready immediately
- No setup troubleshooting

**4. Demo and Presentations**
- Start Codespace before meeting
- Share running application URL
- Live coding demonstrations
- No local environment issues

**5. Working from Different Locations**
- Start work on office desktop
- Continue on home laptop via Codespace
- Finish on tablet via browser
- Seamless continuation

### Codespaces vs Local Development

| Aspect | Local Development | GitHub Codespaces |
|--------|------------------|-------------------|
| **Setup Time** | Hours (install tools) | Seconds (automatic) |
| **Machine Requirements** | Powerful laptop needed | Any device with browser |
| **Consistency** | Varies per developer | Identical for all |
| **Cost** | Hardware investment | Pay per use |
| **Internet Required** | No | Yes |
| **Resource Intensive Tasks** | Limited by laptop | Scale up machine size |
| **Mobility** | One device | Any device |

### Best Practices for Codespaces

✅ **Do:**
- Stop Codespaces when not in use (saves money)
- Define devcontainer for consistent setup
- Use for resource-intensive tasks
- Leverage for quick fixes
- Share devcontainer config with team

❌ **Don't:**
- Leave Codespaces running overnight
- Store secrets in devcontainer (use GitHub Secrets)
- Use for offline work
- Forget to commit changes before stopping

### Codespace Machine Types

| Size | Cores | RAM | Storage | Use Case |
|------|-------|-----|---------|----------|
| **2-core** | 2 | 8 GB | 32 GB | Light development |
| **4-core** | 4 | 16 GB | 32 GB | Standard development (default) |
| **8-core** | 8 | 32 GB | 64 GB | Build-intensive projects |
| **16-core** | 16 | 64 GB | 128 GB | Data processing |
| **32-core** | 32 | 128 GB | 256 GB | Machine learning |

**Cost:** Billed per hour while running (free tier available)

### Managing Codespaces

**View all Codespaces:**
```
1. Go to github.com
2. Click profile → Settings
3. Click "Codespaces" in sidebar
4. See all active Codespaces
5. Stop or delete unused ones
```

**Configure defaults:**
```
Settings → Codespaces
- Default machine type
- Default timeout (auto-stop)
- Default region
- Secrets (API keys, tokens)
```

**Codespace lifecycle:**
- **Active**: Running and being used
- **Idle**: No activity, still running
- **Stopped**: Inactive, not billing
- **Deleted**: Removed (commits are in Git)

### ABB Codespaces Policy

**Recommended for:**
- ✅ Quick fixes and hotfixes
- ✅ Code review testing
- ✅ Demo and training sessions
- ✅ Working remotely
- ✅ Onboarding new developers

**Guidelines:**
- Stop Codespaces after use
- Use 4-core for standard work
- Configure devcontainer in repositories
- Don't store secrets in devcontainer files
- Clean up old Codespaces regularly

---

### Recommended Development Flow

```
1. Local Development
   ├── Code in VS Code
   ├── Run locally
   ├── Unit tests locally
   └── Commit to feature branch

2. Push to GitHub
   ├── Automatic CI/CD triggers
   ├── Tests run in cloud
   ├── Build happens in cloud
   └── Deploy to dev environment

3. Open Pull Request
   ├── Code review in browser
   ├── Comments in VS Code
   ├── Preview deployment created
   └── Team reviews

4. Merge to Main
   ├── Deploy to staging automatically
   ├── Integration tests run
   ├── Manual validation
   └── Deploy to production
```

### Environment Configuration

**Use `.env` files for local development:**

```bash
# .env (local development)
NODE_ENV=development
API_URL=http://localhost:3000
DB_HOST=localhost
GCP_PROJECT=abb-dev

# .env.staging (staging)
NODE_ENV=staging
API_URL=https://staging-api.abb.wales.nhs.uk
GCP_PROJECT=abb-staging

# .env.production (production - secrets in Secret Manager)
NODE_ENV=production
API_URL=https://api.abb.wales.nhs.uk
GCP_PROJECT=abb-prod
```

**Never commit `.env` to Git:**
```
# .gitignore
.env
.env.local
.env.*.local
```

---

## VS Code Settings for GitHub

### Recommended Settings

**File: `.vscode/settings.json`**
```json
{
  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true,
  "git.postCommitCommand": "push",
  
  // GitHub
  "github.pullRequests.defaultMergeMethod": "squash",
  "github.pullRequests.showInSCM": true,
  
  // Editor
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  
  // Files
  "files.autoSave": "onFocusChange",
  "files.exclude": {
    "**/.git": true,
    "**/.DS_Store": true,
    "**/node_modules": true
  },
  
  // Terminal
  "terminal.integrated.defaultProfile.windows": "Git Bash",
  
  // Cloud Code
  "cloudcode.autoDependencies": "on",
  
  // Python (for ABB data engineering)
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black"
}
```

### Workspace Settings

**For ABB repositories, create `.vscode/settings.json`:**

```json
{
  "editor.rulers": [80, 120],
  "editor.tabSize": 2,
  "files.eol": "\n",
  
  // ABB specific
  "python.linting.pylintArgs": [
    "--max-line-length=120"
  ],
  
  // GCP
  "cloudcode.gcpProject": "abb-analytics-platform"
}
```

---

## Collaboration Features

### Live Share (Real-time Collaboration)

**Install:** Live Share Extension Pack

**Features:**
- Share your workspace with teammates
- Collaborative editing (like Google Docs)
- Shared terminal and debugging
- Audio calls (optional)

**Usage:**
```
1. Install Live Share extension
2. Click "Live Share" in status bar
3. Share link with teammates
4. They join your session
5. Collaborate in real-time
```

### Code Review in VS Code

**Review workflow:**
```
1. Checkout PR branch locally
2. View changes in diff view
3. Add comments inline
4. Test changes locally
5. Submit review from VS Code
```

---

## ABB Developer Workflow Example

### Scenario: Update Analytics Dashboard

**Morning Setup:**
```bash
# 1. Open VS Code
code ~/projects/biu_analytics_dashboard

# 2. Pull latest changes
Git: Pull (Ctrl+Shift+G G P)

# 3. Create feature branch
Git: Create Branch → feature/add-wait-time-chart
```

**Development:**
```bash
# 4. Make changes
- Edit src/components/WaitTimeChart.tsx
- Add unit tests
- Update documentation

# 5. Test locally
npm run dev
# Visit http://localhost:3000

# 6. Run tests
npm test
```

**Commit and Push:**
```bash
# 7. Stage changes
Click + in Source Control

# 8. Commit
Message: "Add wait time chart component"
Ctrl+Enter

# 9. Push
Click sync icon
```

**Create Pull Request:**
```bash
# 10. Open PR from VS Code
Ctrl+Shift+P → "GitHub Pull Requests: Create Pull Request"

Title: Add wait time chart to dashboard
Description: 
- Adds interactive wait time visualization
- Includes filters by department
- Responsive design
- Tests included

Reviewers: @senior-engineer1
Labels: feature, frontend
```

**Code Review:**
```bash
# 11. Address feedback
- View comments in VS Code
- Make changes
- Push updates
- Request re-review
```

**After Merge:**
```bash
# 12. Cleanup
Git: Checkout main
Git: Pull
Git: Delete Branch → feature/add-wait-time-chart

# 13. Deploy automatically via GitHub Actions
# Cloud Run deployment happens automatically
```

---

## Summary

### Key Takeaways

✅ **VS Code** is the ideal IDE for GitHub development  
✅ **Built-in Git** support simplifies version control  
✅ **GitHub Extensions** bring GitHub into your editor  
✅ **Cloud Code** integrates GCP deployment  
✅ **GitHub Codespaces** provides cloud-based development environment  
✅ **Keyboard shortcuts** boost productivity  
✅ **Hybrid workflow** balances local and cloud development

### Essential Extensions Recap

| Extension | Purpose | Priority |
|-----------|---------|----------|
| **GitHub Pull Requests** | Manage PRs and issues | ⭐⭐⭐ |
| **GitLens** | Advanced Git features | ⭐⭐⭐ |
| **Cloud Code** | GCP integration | ⭐⭐⭐ |
| **GitHub Codespaces** | Cloud development | ⭐⭐⭐ |
| **GitHub Copilot** | AI code completion | ⭐⭐ |
| **Remote - SSH** | Remote development | ⭐⭐ |

### Workflow Summary

```
Local Development → Commit → Push → PR → Review → Merge → Deploy
       ↓              ↓       ↓      ↓      ↓       ↓       ↓
    VS Code      Source   Sync   GitHub  VS Code  GitHub  Cloud Run
    or            Control  Icon   Web     Extension Web     Auto-deploy
  Codespaces      (GUI)   (GUI)  (GUI)   (GUI)    (GUI)
```

### Next Session Preview

In **Appendix A1: Using GitHub Copilot and Agents**, we'll explore:
- GitHub Copilot features and capabilities
- Code generation with AI
- Copilot Chat for problem-solving
- GitHub Copilot Agents for automated tasks
- Best practices and limitations

---

## Additional Resources

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [GitHub for VS Code](https://code.visualstudio.com/docs/sourcecontrol/github)
- [Cloud Code Documentation](https://cloud.google.com/code/docs/vscode)
- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [VS Code Tips and Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)
- [GitLens Documentation](https://gitlens.amod.io)

---

*Appendix A7 | GitHub Training Package*  
*Aneurin Bevan University Health Board*
