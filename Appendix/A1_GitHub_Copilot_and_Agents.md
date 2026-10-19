# Appendix A1: Using GitHub Copilot and Agents

**Duration**: 30 minutes (self-directed)

> The hands-on Copilot exercise is in [Session 8](../Training/08_Session_8_Codespaces_and_Copilot_Exercise.md). This appendix goes deeper on Copilot Chat, Workspace and agents.

## 🎯 Learning Objectives

By the end of this session, you will understand:
- What GitHub Copilot is and how it works
- Using Copilot for code generation and completion
- GitHub Copilot Chat for problem-solving
- GitHub Copilot Workspace and Agents
- Best practices and responsible AI usage
- Limitations and when to rely on human expertise

---

## Introduction to GitHub Copilot

### What is GitHub Copilot?

**GitHub Copilot** is an AI-powered coding assistant that helps you write code faster and with less effort.

### How It Works

```
Developer Types Code
        ↓
AI Analyzes Context
├── Current file
├── Related files  
├── Code comments
└── Function names
        ↓
Copilot Suggests Code
├── Auto-completions
├── Entire functions
├── Test cases
└── Documentation
        ↓
Developer Reviews
├── Accept (Tab)
├── Reject (Esc)
└── Modify suggestion
```

### Powered by OpenAI

- Trained on billions of lines of public code
- Based on GPT models (similar to ChatGPT)
- Understands multiple programming languages
- Learns from context in your code

### GitHub Copilot Products

| Product | Description | Use Case |
|---------|-------------|----------|
| **Copilot Individual** | Personal subscription | Individual developers |
| **Copilot Business** | Organization subscription | ABB teams |
| **Copilot Enterprise** | Advanced features + knowledge base | Large enterprises |
| **Copilot Chat** | Conversational AI in editor | Problem-solving |
| **Copilot Workspace** | AI-powered development environment | Full project work |

### ABB Context

The Aneurin Bevan University Health Board has **GitHub Copilot Business** licenses available for development teams.

---

## Setting Up GitHub Copilot

### Prerequisites

- GitHub account with Copilot access
- VS Code (or supported IDE)
- Active internet connection

### Installation in VS Code

**1. Install Extension:**
```
1. Open Extensions (Ctrl+Shift+X)
2. Search "GitHub Copilot"
3. Install "GitHub Copilot" extension
4. Install "GitHub Copilot Chat" extension
```

**2. Sign In:**
```
1. Click GitHub Copilot icon in status bar
2. Sign in to GitHub
3. Authorize Copilot
4. Wait for activation (may take a few minutes)
```

**3. Verify Installation:**
```
1. Create new file (test.js)
2. Type: // function to calculate sum
3. Press Enter
4. Copilot should suggest code
```

### Configuration

**Settings.json:**
```json
{
  "github.copilot.enable": {
    "*": true,
    "yaml": false,
    "plaintext": false
  },
  "github.copilot.editor.enableAutoCompletions": true,
  "editor.inlineSuggest.enabled": true
}
```

---

## Using GitHub Copilot

### Code Completion

#### Basic Completion

**You type:**
```javascript
// Function to format UK phone numbers
function formatPhoneNumber
```

**Copilot suggests:**
```javascript
function formatPhoneNumber(number) {
  // Remove all non-numeric characters
  const cleaned = number.replace(/\D/g, '');
  
  // Format as UK phone number
  if (cleaned.length === 11 && cleaned.startsWith('0')) {
    return `${cleaned.slice(0, 4)} ${cleaned.slice(4, 7)} ${cleaned.slice(7)}`;
  }
  
  return number;
}
```

**Accept:** Press `Tab`  
**Reject:** Press `Esc`  
**See alternatives:** Press `Alt+]` or `Alt+[`

#### Function Implementation

**You type:**
```python
def calculate_patient_wait_time(arrival_time, treatment_time):
    """
    Calculate wait time for a patient in minutes.
    
    Args:
        arrival_time: datetime when patient arrived
        treatment_time: datetime when treatment started
    
    Returns:
        int: wait time in minutes
    """
```

**Copilot suggests:**
```python
    if not arrival_time or not treatment_time:
        return 0
    
    wait_time = (treatment_time - arrival_time).total_seconds() / 60
    return max(0, int(wait_time))
```

#### Test Generation

**You type:**
```python
# Test cases for calculate_patient_wait_time
def test_calculate_patient_wait_time():
```

**Copilot suggests:**
```python
    from datetime import datetime, timedelta
    
    # Test normal wait time
    arrival = datetime(2024, 1, 15, 9, 0)
    treatment = datetime(2024, 1, 15, 9, 30)
    assert calculate_patient_wait_time(arrival, treatment) == 30
    
    # Test zero wait time
    arrival = datetime(2024, 1, 15, 9, 0)
    treatment = datetime(2024, 1, 15, 9, 0)
    assert calculate_patient_wait_time(arrival, treatment) == 0
    
    # Test with None values
    assert calculate_patient_wait_time(None, None) == 0
```

### Code Comments to Code

**Natural language → Code:**

```javascript
// Create a React component that displays patient information
// including name, NHS number, and date of birth
// Format the date as DD/MM/YYYY
```

**Copilot generates:**
```javascript
function PatientInfo({ patient }) {
  const formatDate = (date) => {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
  };

  return (
    <div className="patient-info">
      <h2>{patient.name}</h2>
      <p>NHS Number: {patient.nhsNumber}</p>
      <p>Date of Birth: {formatDate(patient.dateOfBirth)}</p>
    </div>
  );
}
```

### Common Patterns

#### Database Queries

**Comment:**
```python
# Query to get all patients waiting more than 4 hours in A&E
```

**Copilot suggests:**
```python
query = """
    SELECT patient_id, name, arrival_time, 
           TIMESTAMPDIFF(MINUTE, arrival_time, NOW()) as wait_minutes
    FROM ae_patients
    WHERE status = 'waiting'
      AND TIMESTAMPDIFF(MINUTE, arrival_time, NOW()) > 240
    ORDER BY arrival_time ASC
"""
```

#### API Endpoints

**Comment:**
```javascript
// Express endpoint to get patient appointment by ID
```

**Copilot suggests:**
```javascript
app.get('/api/appointments/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const appointment = await db.query(
      'SELECT * FROM appointments WHERE id = ?',
      [id]
    );
    
    if (!appointment) {
      return res.status(404).json({ error: 'Appointment not found' });
    }
    
    res.json(appointment);
  } catch (error) {
    console.error('Error fetching appointment:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

#### Configuration Files

**Comment:**
```yaml
# GitHub Actions workflow to deploy to Cloud Run
```

**Copilot suggests:**
```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_CREDENTIALS }}
      
      - name: Deploy
        run: |
          gcloud run deploy my-service \
            --source . \
            --region europe-west2
```

---

## GitHub Copilot Chat

### What is Copilot Chat?

**Copilot Chat** is a conversational AI interface for asking questions and solving problems.

### Opening Copilot Chat

```
Methods:
├── Click chat icon in Activity Bar
├── Ctrl+Shift+I (inline chat)
├── Ctrl+I (quick chat)
└── Right-click → "Copilot: Explain This"
```

### Chat Interface

```
┌─────────────────────────────────────────┐
│ GITHUB COPILOT CHAT                 [X] │
├─────────────────────────────────────────┤
│ 💬 You:                                 │
│ How do I connect to BigQuery from       │
│ Python?                                 │
│                                         │
│ 🤖 Copilot:                             │
│ To connect to BigQuery from Python:     │
│                                         │
│ ```python                               │
│ from google.cloud import bigquery       │
│                                         │
│ client = bigquery.Client(               │
│     project='abb-analytics-platform'    │
│ )                                       │
│                                         │
│ query = """                             │
│     SELECT * FROM dataset.table         │
│     LIMIT 10                            │
│ """                                     │
│ results = client.query(query)           │
│ ```                                     │
└─────────────────────────────────────────┘
```

### Common Chat Commands

#### Explain Code

**Select code → Right-click → "Copilot: Explain This"**

```
You selected:
const result = data.reduce((acc, item) => 
  ({ ...acc, [item.id]: item }), {});

Copilot explains:
This code transforms an array into an object where:
- Keys are the 'id' property of each item
- Values are the complete item objects
- Uses reduce() with object spread syntax
- Useful for creating lookup tables from arrays
```

#### Fix Code

**Select buggy code → Chat: "/fix"**

```
You: /fix this code

Copilot suggests:
The issue is that you're comparing dates as strings. 
Change line 15 to:
  if (new Date(date1) > new Date(date2))
```

#### Generate Tests

**Select function → Chat: "/tests"**

```
You: /tests

Copilot generates:
describe('formatPhoneNumber', () => {
  it('should format valid UK phone numbers', () => {
    expect(formatPhoneNumber('07123456789'))
      .toBe('0712 345 6789');
  });
  
  it('should handle numbers with spaces', () => {
    expect(formatPhoneNumber('0712 345 6789'))
      .toBe('0712 345 6789');
  });
  
  it('should return original for invalid numbers', () => {
    expect(formatPhoneNumber('123'))
      .toBe('123');
  });
});
```

#### Optimize Code

**Select code → Chat: "/optimize"**

```
You: /optimize this function

Copilot suggests:
Current implementation has O(n²) complexity due to nested loops.
Here's an optimized O(n) version using a Map:

```javascript
function findDuplicates(arr) {
  const seen = new Map();
  const duplicates = [];
  
  for (const item of arr) {
    if (seen.has(item)) {
      if (seen.get(item) === 1) {
        duplicates.push(item);
      }
      seen.set(item, seen.get(item) + 1);
    } else {
      seen.set(item, 1);
    }
  }
  
  return duplicates;
}
```
```

### Slash Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/explain` | Explain code | Explain this regex |
| `/fix` | Fix issues | Fix this bug |
| `/tests` | Generate tests | Create unit tests |
| `/doc` | Generate docs | Document this API |
| `/optimize` | Improve performance | Optimize this loop |
| `/help` | Show help | How do I use... |

### Context-Aware Chat

Copilot Chat understands:
- Current file content
- Selected code
- Open files in editor
- Project structure
- Recent edits

**Example:**
```
You: How do I add error handling to the getPatients function?

Copilot knows:
- You have a function called getPatients
- It's in the current file
- It's an async function
- It calls an API

Copilot suggests error handling specific to your code.
```

---

## GitHub Copilot Workspace

### What is Copilot Workspace?

**Copilot Workspace** (preview) is an AI-native development environment for working on entire features or issues.

### How It Works

```
1. Start from GitHub Issue
   ↓
2. Copilot analyzes issue and codebase
   ↓
3. Copilot creates implementation plan
   ↓
4. Copilot generates code changes
   ↓
5. Developer reviews and refines
   ↓
6. Create pull request
```

### Key Features

**1. Issue Analysis**
- Reads issue description
- Understands requirements
- Analyzes existing codebase
- Identifies files to change

**2. Implementation Planning**
- Creates step-by-step plan
- Identifies dependencies
- Suggests architecture
- Estimates complexity

**3. Code Generation**
- Generates new files
- Modifies existing code
- Creates tests
- Updates documentation

**4. Iterative Refinement**
- Chat with Copilot about changes
- Request modifications
- Add requirements
- Improve implementation

### Example Workflow

**Issue #234:**
```
Title: Add patient appointment reminder system

Description:
We need to send email reminders to patients 24 hours before 
their appointments. Should include:
- Patient name and NHS number
- Appointment time and location
- Instructions for cancellation
```

**Copilot Workspace generates:**

1. **Plan:**
   ```
   ✓ Create email template service
   ✓ Add scheduled job to check appointments
   ✓ Implement reminder logic
   ✓ Add configuration for email service
   ✓ Create tests for reminder system
   ✓ Update documentation
   ```

2. **Files to create/modify:**
   ```
   New files:
   - src/services/reminderService.js
   - src/templates/appointmentReminder.html
   - tests/reminderService.test.js
   
   Modified files:
   - src/jobs/scheduledJobs.js
   - config/email.js
   - README.md
   ```

3. **Generated code:**
   ```javascript
   // src/services/reminderService.js
   class ReminderService {
     async sendAppointmentReminders() {
       const tomorrow = new Date();
       tomorrow.setDate(tomorrow.getDate() + 1);
       
       const appointments = await this.getAppointmentsForDate(tomorrow);
       
       for (const appointment of appointments) {
         await this.sendReminder(appointment);
       }
     }
     
     // ... more implementation
   }
   ```

---

## GitHub Copilot for Agents

### What are Copilot Agents?

**Copilot Agents** are AI assistants that can perform tasks automatically, such as:
- Code reviews
- Documentation generation
- Security scanning
- Test generation
- Issue triage

### Agent Types

#### 1. **Code Review Agent**

**Automatically reviews PRs:**
```
Checks:
✓ Code follows style guidelines
✓ No obvious bugs
✓ Tests included
✓ Documentation updated
⚠️ Performance concerns identified
✓ Security best practices followed

Comments:
💬 Line 45: Consider using const instead of let
⚠️ Line 67: This query might be slow with large datasets
✅ Overall: Good implementation!
```

#### 2. **Documentation Agent**

**Generates documentation:**
```javascript
/**
 * Calculates the wait time for a patient.
 * 
 * @param {Date} arrivalTime - When the patient arrived
 * @param {Date} treatmentTime - When treatment started
 * @returns {number} Wait time in minutes
 * @throws {Error} If dates are invalid
 * 
 * @example
 * const waitTime = calculateWaitTime(
 *   new Date('2024-01-15T09:00:00'),
 *   new Date('2024-01-15T09:30:00')
 * );
 * // Returns: 30
 */
function calculateWaitTime(arrivalTime, treatmentTime) {
  // Implementation
}
```

#### 3. **Test Generation Agent**

**Creates comprehensive tests:**
```python
# Automatically generated test suite
class TestPatientWaitTime:
    def test_normal_wait_time(self):
        """Test calculation with valid dates"""
        
    def test_zero_wait_time(self):
        """Test when treatment is immediate"""
        
    def test_invalid_dates(self):
        """Test error handling for invalid dates"""
        
    def test_negative_wait_time(self):
        """Test when treatment is before arrival"""
```

#### 4. **Security Scanning Agent**

**Identifies security issues:**
```
Security findings:
🔴 CRITICAL: Hardcoded API key on line 23
🟡 WARNING: SQL injection risk on line 45
🟡 WARNING: Outdated dependency: lodash@4.17.19
🟢 INFO: Consider using environment variables
```

---

## Best Practices

### Do's ✅

**1. Review All Suggestions**
- Never accept code blindly
- Understand what it does
- Test thoroughly
- Verify for your use case

**2. Provide Context**
- Write clear comments
- Use descriptive names
- Structure code logically
- Include examples

**3. Iterate**
- Refine suggestions
- Ask for alternatives
- Use chat for clarification
- Combine multiple suggestions

**4. Use for Boilerplate**
- Configuration files
- Test scaffolding
- Common patterns
- Documentation templates

**5. Learn from Suggestions**
- Study generated code
- Understand new patterns
- Learn language features
- Improve your skills

### Don'ts ❌

**1. Never Accept Blindly**
```
❌ Don't: Press Tab on every suggestion
✅ Do: Review, understand, test
```

**2. Don't Share Sensitive Data**
```
❌ Don't: Include patient data in comments
❌ Don't: Add API keys in prompts
❌ Don't: Share PHI (Protected Health Information)
✅ Do: Use generic examples
```

**3. Don't Rely Completely**
```
❌ Don't: Let AI make all decisions
❌ Don't: Skip code review
❌ Don't: Ignore security concerns
✅ Do: Use as an assistant, not replacement
```

**4. Don't Use for Critical Security**
```
❌ Don't: Generate authentication code without review
❌ Don't: Accept crypto implementations
❌ Don't: Trust for HIPAA/GDPR compliance
✅ Do: Have security experts review
```

---

## ABB-Specific Guidelines

### Approved Use Cases

✅ **Recommended:**
- Boilerplate code generation
- Test case creation
- Documentation writing
- Code refactoring suggestions
- Learning new languages/frameworks
- Debugging assistance

⚠️ **Use with Caution:**
- Database queries (review carefully)
- API integrations (verify endpoints)
- Configuration files (check settings)
- Performance-critical code (benchmark)

❌ **Not Recommended:**
- PHI data handling (require review)
- Authentication/authorization (security review)
- Production database scripts (DBA review)
- Critical healthcare logic (clinical review)

### Data Privacy

**Copilot Business settings:**
- Code snippets NOT used for training
- Prompts NOT shared with other users
- Suggestions based on public code only
- Your code stays private

**Still avoid:**
- Patient names, NHS numbers
- Real email addresses
- Actual phone numbers
- Production credentials
- Sensitive business logic

### Code Review Requirements

**All Copilot-generated code must:**
1. Be reviewed by a human developer
2. Pass all automated tests
3. Meet ABB coding standards
4. Be approved by senior engineer for critical systems
5. Include proper error handling
6. Have appropriate logging

---

## Practical Examples

### Example 1: BigQuery Integration

**Prompt:**
```python
# Function to query patient wait times from BigQuery
# Group by department, calculate average wait time
# Filter for last 30 days
```

**Copilot generates:**
```python
from google.cloud import bigquery
from datetime import datetime, timedelta

def get_wait_times_by_department():
    client = bigquery.Client(project='abb-analytics-platform')
    
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    query = f"""
        SELECT 
            department,
            AVG(TIMESTAMP_DIFF(treatment_time, arrival_time, MINUTE)) 
                as avg_wait_minutes,
            COUNT(*) as patient_count
        FROM `abb-analytics-platform.patients.visits`
        WHERE arrival_time >= '{thirty_days_ago.isoformat()}'
            AND treatment_time IS NOT NULL
        GROUP BY department
        ORDER BY avg_wait_minutes DESC
    """
    
    results = client.query(query).result()
    
    return [
        {
            'department': row.department,
            'avg_wait_minutes': float(row.avg_wait_minutes),
            'patient_count': row.patient_count
        }
        for row in results
    ]
```

### Example 2: Cloud Run Deployment

**Chat: "How do I deploy a Python Flask app to Cloud Run?"**

**Copilot response:**
```
Here's how to deploy a Flask app to Cloud Run:

1. Create Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

2. Create .dockerignore:
```
__pycache__
*.pyc
.env
.git
```

3. Deploy:
```bash
gcloud run deploy my-app \
  --source . \
  --region europe-west2 \
  --platform managed \
  --allow-unauthenticated
```

The app will be available at the provided URL.
```

### Example 3: React Dashboard Component

**Comment:**
```javascript
// Create a dashboard card component that shows:
// - Title
// - Current value with large font
// - Change percentage (green if positive, red if negative)
// - Small trend sparkline chart
```

**Copilot generates:**
```javascript
import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

function DashboardCard({ title, value, change, trendData }) {
  const isPositive = change >= 0;
  
  return (
    <div className="dashboard-card">
      <h3 className="card-title">{title}</h3>
      
      <div className="card-value">
        {value}
      </div>
      
      <div className={`card-change ${isPositive ? 'positive' : 'negative'}`}>
        {isPositive ? <TrendingUp /> : <TrendingDown />}
        {Math.abs(change)}%
      </div>
      
      <div className="card-trend">
        <Sparkline data={trendData} />
      </div>
    </div>
  );
}
```

---

## Limitations and Considerations

### Known Limitations

**1. Not Always Correct**
- May suggest buggy code
- Can hallucinate APIs that don't exist
- Might not follow latest best practices
- May miss edge cases

**2. Context Window**
- Limited to recent code
- May not understand full architecture
- Doesn't know your business rules
- Can't access documentation sites

**3. Language Support Varies**
- Best for: Python, JavaScript, TypeScript, Java
- Good for: Go, C#, Ruby, PHP
- Limited for: Legacy languages, proprietary DSLs

**4. Not a Replacement**
- Can't make architectural decisions
- Doesn't understand business requirements
- Can't validate clinical logic
- Requires human oversight

### When NOT to Use Copilot

❌ **Critical Healthcare Logic**
- Medication dosage calculations
- Clinical decision algorithms
- Patient safety rules
- Emergency protocols

❌ **Sensitive Operations**
- Authentication systems
- Encryption implementation
- Access control logic
- Audit logging

❌ **Complex Algorithms**
- Performance-critical code
- Distributed systems logic
- Complex state management
- Race condition handling

### Alternative: Human Expertise

**Always consult humans for:**
- Architecture decisions
- Clinical validation
- Security reviews
- Performance optimization
- Complex debugging
- Regulatory compliance

---

## Summary

### Key Takeaways

✅ **Copilot** accelerates coding with AI-powered suggestions  
✅ **Chat** provides conversational problem-solving  
✅ **Workspace** handles entire features with AI  
✅ **Agents** automate review, testing, and documentation  
✅ **Best practices** include reviewing all suggestions  
✅ **Privacy** is maintained with Copilot Business  
✅ **Limitations** require human oversight and expertise

### Productivity Gains

Studies show Copilot users:
- Write code 55% faster
- Stay in flow state longer
- Focus on creative problem-solving
- Learn new APIs more quickly
- Reduce boilerplate writing time

### ABB Implementation

**Copilot Business available for:**
- BIU - Data Engineers
- BIU - Analytical Engineers
- PHN Development Team
- Approved contractors

**Request access:**
Contact ABB - GitHub Owners team

### Final Thoughts

**Copilot is a tool, not a replacement:**
```
Developer Judgment + Copilot Assistance = Best Results
```

**Use Copilot to:**
- Save time on repetitive tasks
- Learn new technologies
- Generate test cases
- Write documentation
- Explore alternative approaches

**Always remember:**
- You are responsible for the code
- Review everything carefully
- Test thoroughly
- Follow ABB guidelines
- Protect patient privacy

---

## Training Complete! 🎉

### What You've Learned

Throughout this training day, you've explored:

1. ✅ **GitHub Fundamentals** - Cloud vs on-premises
2. ✅ **Basic Concepts** - Commits, branches, PRs
3. ✅ **Deployment Models** - CLI and Desktop tools
4. ✅ **GCP Integration** - Cloud-native development
5. ✅ **GitHub Components** - Issues, projects, wikis
6. ✅ **Hybrid Workflows** - VS Code and productivity
7. ✅ **AI-Powered Development** - Copilot and agents

### Next Steps

**Continue Learning:**
- [GitHub Skills](https://skills.github.com/)
- [GitHub Docs](https://docs.github.com)
- [ABB GitHub Config](../README.md)

**Practice:**
- Clone repositories
- Create branches
- Submit pull requests
- Use Copilot daily

**Get Involved:**
- Join GitHub Discussions
- Review teammate's code
- Share knowledge
- Contribute to documentation

### Support

**Need Help?**
- ABB - GitHub Owners team
- Email: github-owners@wales.nhs.uk
- Training materials: `/Training/`
- Documentation: [Wiki](https://github.com/Aneurin-Bevan-University-Health-Board/ABB_GitHub_Config/wiki)

---

## Additional Resources

### GitHub Resources
- [GitHub Learning Lab](https://lab.github.com/)
- [GitHub Blog](https://github.blog/)
- [GitHub Changelog](https://github.blog/changelog/)

### Copilot Resources
- [Copilot Documentation](https://docs.github.com/en/copilot)
- [Copilot Trust Center](https://resources.github.com/copilot-trust-center/)
- [Copilot Best Practices](https://github.blog/2023-06-20-how-to-write-better-prompts-for-github-copilot/)

### Community
- [GitHub Community](https://github.community/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/github)
- [Dev.to GitHub](https://dev.to/t/github)

---

## Feedback

**Help us improve this training:**
- [Submit feedback issue](https://github.com/Aneurin-Bevan-University-Health-Board/ABB_GitHub_Config/issues/new)
- Email: github-owners@wales.nhs.uk
- Discussion: [Training feedback](https://github.com/Aneurin-Bevan-University-Health-Board/ABB_GitHub_Config/discussions)

---

## Certificate of Completion

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   GitHub Training Day - Certificate

   This certifies that you have completed the
   Aneurin Bevan University Health Board
   GitHub Training Programme

   Topics Covered:
   ✓ GitHub Fundamentals
   ✓ Version Control with Git
   ✓ GCP Integration
   ✓ Team Collaboration
   ✓ AI-Powered Development

   Date: _______________
   Trainer: ABB GitHub Owners Team
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**Thank you for attending!**

*Appendix A1 | GitHub Training Package*  
*Aneurin Bevan University Health Board*

---

*Training package version 1.0*  
*Last updated: 2024*  
*Maintained by: ABB - GitHub Owners team*
