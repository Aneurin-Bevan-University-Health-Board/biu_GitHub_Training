# Session 7: Issues, Projects, and Discussions

![BIU Logo](links%20and%20logos/BIU%20LOGO.png) ![DDAT Logo](links%20and%20logos/DDAT%20Logo.png)

**Duration**: 30 minutes  
**Time**: 14:00 - 14:30

## Learning Objectives

By the end of this session, you will understand:

- GitHub Issues for task management and bug tracking in healthcare analytics
- GitHub Projects for organising and visualising initiatives
- GitHub Discussions for team knowledge sharing and collaboration
- Workflow automation with GitHub Actions 


---

## GitHub Issues 

### Overview of Issues 

GitHub Issues provide a powerful, integrated approach to project management that works seamlessly with code development. In ABUHB BIU, Issues are used to track tasks, bugs, feature requests, and clinical validation activities related to healthcare analytics projects.

### Core Issue Features

#### Issue Types for NHS Wales Analytics

```text
Potential Type of Issue Categories:
├── 🐛 Bug Reports
│   ├── Data quality issues in outputs
│   ├── Calculation errors in clinical metrics
│   ├── Performance problems with large datasets
│   └── Integration failures 
├── ✨ Feature Requests
│   ├── New clinical indicators or metrics
│   ├── Additional data sources or integrations
│   ├── Enhanced visualization requirements
│   └── Compliance or regulatory updates
├── 📊 Data Issues
│   ├── Missing or incomplete data sources
│   ├── Data validation failures
│   ├── Schema changes in source systems
│   └── Data quality threshold violations
├── 🔧 Technical Debt
│   ├── Code refactoring for maintainability
│   ├── Performance optimization needs
│   ├── Documentation improvements
│   └── Testing coverage enhancements
└── 📋 Project Tasks
    ├── Clinical validation requirements
    ├── Stakeholder review and approval
    ├── Training and documentation needs
    └── Deployment and go-live activities
```

### Creating Effective Issues 

#### Issue Templates - Example

```markdown
<!-- .github/ISSUE_TEMPLATE/clinical_feature_request.md -->
---
name: Clinical Feature Request
about: Request a new clinical indicator or analytical feature
title: '[CLINICAL] '
labels: enhancement, clinical-validation-required
assignees: ''
---

## Clinical Context
**Clinical Guideline Reference:** 
*Specify NHS clinical guideline or standard (e.g., NICE CG123)*

**Clinical Lead Contact:**
*Name and role of clinical stakeholder*

**Priority Level:**
- [ ] Critical (Patient Safety Impact)
- [ ] High (Quality Improvement)
- [ ] Medium (Operational Efficiency)
- [ ] Low (Nice to Have)

## Feature Description
**What clinical need does this address?**
*Describe the healthcare problem or opportunity*

**Proposed Solution:**
*Describe the analytical feature or indicator needed*

**Success Criteria:**
*How will we know this feature is working correctly?*

## Technical Considerations
**Data Sources Required:**
- [ ] Patient Administration System (PAS)
- [ ] Electronic Health Records (EHR)
- [ ] Laboratory Information System (LIS)
- [ ] National datasets (e.g., ONS, NHS Digital)
- [ ] Other: _______________

**Expected Data Volume:**
*Estimate of records/transactions per month*

**Performance Requirements:**
*Response time expectations for reports/dashboards*

#### Issue Template (Single Example)
**Data Sensitivity Level:**
- [ ] Public
- [ ] Internal
- [ ] Confidential
- [ ] Restricted

**Regulatory Considerations:**
- [ ] GDPR compliance required
- [ ] NHS Digital approval needed
- [ ] Clinical audit requirements
- [ ] Information governance review

## Acceptance Criteria
- [ ] Clinical validation completed
- [ ] Data quality validation (>95% completeness)
- [ ] Performance testing passed
- [ ] Documentation updated
- [ ] Training materials prepared
- [ ] Stakeholder sign-off obtained

## Additional Context
*Add any other context, screenshots, or examples*
```

#### Bug Report Template for Analytics

```markdown
<!-- .github/ISSUE_TEMPLATE/analytics_bug_report.md -->
---
name: Analytics Bug Report
about: Report a problem with analytical outputs or calculations
title: '[BUG] '
labels: bug, needs-investigation
assignees: ''
---

## Bug Description
**Summary:**
*Brief description of the issue*

**Impact Assessment:**
- [ ] Critical - Affects patient safety or clinical decisions
- [ ] High - Significant impact on operations or reporting
- [ ] Medium - Moderate impact on workflow
- [ ] Low - Minor inconvenience

## Steps to Reproduce
1. 
2. 
3. 

**Expected Result:**
*What should happen*

**Actual Result:**
*What actually happened*

## Environment Information
**Analysis Environment:**
- [ ] Production
- [ ] Test/Staging
- [ ] Development
- [ ] Local development

**Data Period:**
*Specify the time period of data affected*

**Affected Reports/Dashboards:**
*List specific outputs showing the issue*

## Evidence
**Screenshots/Outputs:**
*Attach screenshots or sample outputs showing the issue*

**Data Samples:**
*Include anonymized data samples if helpful (ensure no patient data)*

**Error Messages:**

## Clinical Context
**Clinical Validation:**
- [ ] Issue confirmed by clinical lead
- [ ] Impact on clinical decisions assessed
- [ ] Workaround identified if needed

**Affected Stakeholders:**
*Who is impacted by this issue?*

## Technical Details
**Suspected Root Cause:**
*If known, describe potential cause*

**Related Code/Reports:**
*Link to specific files or reports*

**Additional Information:**
*Any other relevant technical details*
```

### Issue Management Workflows

#### Issue Lifecycle

```text
Issue Workflow:
1. 📝 Issue Creation
   ├── Stakeholder identifies need or problem
   ├── Initial triage and categorization
   ├── Clinical validation if required
   └── Assignment to appropriate team member

2. 🔍 Investigation and Planning
   ├── Technical feasibility assessment
   ├── Data source identification and validation
   ├── Compliance and governance review
   └── Effort estimation and prioritization

3. 🛠️ Development Phase
   ├── Feature branch creation linked to issue
   ├── Implementation with regular updates
   ├── Code review with clinical validation
   └── Testing and quality assurance

4. ✅ Validation and Deployment
   ├── Clinical stakeholder testing
   ├── Data quality validation
   ├── Performance testing
   └── Production deployment

5. 📋 Closure and Documentation
   ├── Stakeholder acceptance confirmation
   ├── Documentation updates
   ├── Training delivery if required
   └── Issue closure with lessons learned
```

## 📊 GitHub Projects (Lightweight Guide)

Purpose: Provide a single shared picture of current work, what's next, and what's blocked. Keep it simple so people actually use it. If you need a Gantt chart or capacity planning, do that elsewhere – this board is for flow.

### 5‑Minute Setup

```text
1. Create project → Name: "Quality Indicators Q1" (short & outcome focused)
2. Columns: Backlog | In Progress | Review | Blocked (optional) | Done
3. Fields: Priority (Critical/High/Med/Low), Target Date, Owner
4. Saved view filter: is:open label:quality-indicators
5. Automation: new issue with label → Backlog; merged PR → move linked issue to Done
```

### Columns & Definitions

| Column | Purpose | Exit Criterion |
|--------|---------|----------------|
| Backlog | Accepted but not started | Has priority + owner |
| In Progress | Actively being worked | PR opened or progress comment in last 3 days |
| Review | Awaiting code and/or clinical review | Checklist complete + reviewer assigned |
| Blocked | External dependency halting progress | Block cause + next action noted |
| Done | Completed & validated | Issue closed + docs / indicators updated |



### Mini Issue Template (Put in Description)

```text
Context: <why this matters>
Definition of Done:
- [ ] Logic / code implemented
- [ ] Clinical review (if required)
- [ ] Data quality ≥95% (if data dependent)
- [ ] Documentation updated
Risks/Blockers: <if any>
```

### Recommended Labels (≤12 Total)

| Category | Labels |
|----------|--------|
| Type | feature, bug, data, doc |
| Priority | critical, high, medium, low |
| Status (optional) | blocked, needs-review |
| Compliance | clinical-validation, governance |

### Simple Automation Recipes

| Goal | Rule |
|------|------|
| Auto intake | Add issues with label:quality-indicators to project |
| Progress | When PR opened referencing issue → move to In Progress |
| Review gate | When PR marked ready for review → move issue to Review |
| Completion | When issue closed → move to Done |
| Surface blockers | If label:blocked added → move to Blocked |






**Tags:** #clinical-validation #cardiology #risk-scoring #cross-site-collaboration
```

#### Discussion Moderation Guidelines

```text
NHS Wales Discussion Moderation:
✅ Encourage Participation:
- Welcome questions from all experience levels
- Celebrate knowledge sharing and collaboration
- Recognize helpful contributions and solutions
- Foster inclusive and respectful dialogue

✅ Maintain Quality:
- Ensure clinical accuracy in medical discussions
- Fact-check against official NHS guidelines
- Request evidence and references for claims
- Escalate clinical disagreements to appropriate leads

✅ Protect Sensitive Information:
- Never share patient identifiable information
- Avoid detailed system configuration details
- Use anonymized examples and data samples
- Follow NHS Wales information governance policies

✅ Facilitate Resolution:
- Help connect questioners with subject matter experts
- Summarize complex discussions for clarity
- Archive resolved discussions for future reference
- Follow up on outstanding questions and actions
```

### Knowledge Management Integration

#### Discussion-to-Documentation Pipeline

```text
Knowledge Capture Workflow:
1. 💬 Discussion and Resolution
   ├── Problem identified and discussed
   ├── Solutions proposed and evaluated
   ├── Consensus reached on best approach
   └── Implementation guidance provided

2. 📝 Documentation Creation
   ├── Key insights extracted from discussion
   ├── Formal documentation created in repository
   ├── Best practices and guidelines updated
   └── Training materials enhanced

3. 🔍 Searchable Knowledge Base
   ├── Discussion archives maintained
   ├── Solutions indexed and categorized
   ├── Cross-references to documentation
   └── Regular knowledge base updates

4. 🎓 Training Integration
   ├── Common discussions become training topics
   ├── Real-world examples used in courses
   ├── Community expertise leveraged
   └── Continuous learning culture promoted
```

---

## 🤖 GitHub Actions for Healthcare Automation

### Automation Opportunities in Healthcare Analytics

#### Common Automation Scenarios

```text
NHS Wales Automation Use Cases:
├── 🔄 Data Quality Monitoring
│   ├── Automated data validation checks
│   ├── Data completeness monitoring
│   ├── Schema change detection
│   └── Data freshness verification
├── 📊 Report Generation
│   ├── Scheduled monthly/quarterly reports
│   ├── Executive dashboard updates
│   ├── Clinical indicator calculations
│   └── Performance metric monitoring
├── 🧪 Testing and Validation
│   ├── Automated unit testing for calculations
│   ├── Clinical validation test suites
│   ├── Performance testing for large datasets
│   └── Regression testing for model updates
├── 🚀 Deployment Automation
│   ├── Automated deployment to test environments
│   ├── Production deployment with approvals
│   ├── Database migration automation
│   └── Configuration management
└── 🔐 Compliance Monitoring
    ├── GDPR compliance checking
    ├── Data retention policy enforcement
    ├── Access control validation
    └── Audit trail generation
```

### GitHub Actions

#### Example: Monthly Clinical Report Automation

```yaml
# .github/workflows/monthly_clinical_reports.yml
# Automated Monthly Clinical Report Generation

name: Monthly Clinical Reports

on:
  schedule:
    # Run on the 1st of every month at 6 AM UTC
    - cron: '0 6 1 * *'
  workflow_dispatch:
    inputs:
      reporting_month:
        description: 'Reporting month (YYYY-MM)'
        required: true
        default: '2024-01'
      site_code:
        description: 'NHS Wales site code'
        required: true
        default: 'CARDIFF'
        type: choice
        options:
          - 'CARDIFF'
          - 'SWANSEA'
          - 'NEWPORT'
          - 'BRIDGEND'
          - 'ALL_SITES'

env:
  PYTHON_VERSION: '3.11'
  NHS_WALES_ENV: 'production'

jobs:
  data_quality_check:
    name: Data Quality Validation
    runs-on: ubuntu-latest
    outputs:
      data_quality_passed: ${{ steps.quality_check.outputs.passed }}
      data_completeness: ${{ steps.quality_check.outputs.completeness }}
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      
      - name: Setup Python Environment
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install Dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Configure NHS Wales Database Access
        env:
          NHS_DB_CONNECTION: ${{ secrets.NHS_WALES_DB_CONNECTION }}
          SERVICE_ACCOUNT_KEY: ${{ secrets.NHS_SERVICE_ACCOUNT }}
        run: |
          echo "Configuring secure database connection..."
          python scripts/setup_database_connection.py
      
      - name: Run Data Quality Checks
        id: quality_check
        env:
          REPORTING_MONTH: ${{ github.event.inputs.reporting_month || '2024-01' }}
          SITE_CODE: ${{ github.event.inputs.site_code || 'CARDIFF' }}
        run: |
          echo "Running data quality validation..."
          python src/data_quality_validator.py \
            --month "$REPORTING_MONTH" \
            --site "$SITE_CODE" \
            --output-json quality_results.json
          
          # Extract results for next jobs
          PASSED=$(python -c "import json; print(json.load(open('quality_results.json'))['overall_passed'])")
          COMPLETENESS=$(python -c "import json; print(json.load(open('quality_results.json'))['data_completeness'])")
          
          echo "passed=$PASSED" >> $GITHUB_OUTPUT
          echo "completeness=$COMPLETENESS" >> $GITHUB_OUTPUT
          
          echo "Data quality check completed: PASSED=$PASSED, COMPLETENESS=$COMPLETENESS"
      
      - name: Upload Quality Report
        uses: actions/upload-artifact@v3
        with:
          name: data-quality-report
          path: quality_results.json
          retention-days: 30

  generate_clinical_reports:
    name: Generate Clinical Reports
    runs-on: ubuntu-latest
    needs: data_quality_check
    if: needs.data_quality_check.outputs.data_quality_passed == 'true'
    
    strategy:
      matrix:
        report_type: ['patient_safety', 'quality_indicators', 'operational_metrics']
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      
      - name: Setup Python Environment
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install Dependencies
        run: |
          pip install -r requirements.txt
          # Additional healthcare analytics libraries
          pip install matplotlib seaborn plotly pandas numpy
      
      - name: Generate Clinical Report
        env:
          REPORTING_MONTH: ${{ github.event.inputs.reporting_month || '2024-01' }}
          SITE_CODE: ${{ github.event.inputs.site_code || 'CARDIFF' }}
          REPORT_TYPE: ${{ matrix.report_type }}
          NHS_DB_CONNECTION: ${{ secrets.NHS_WALES_DB_CONNECTION }}
        run: |
          echo "Generating $REPORT_TYPE report for $SITE_CODE - $REPORTING_MONTH"
          
          python src/clinical_report_generator.py \
            --report-type "$REPORT_TYPE" \
            --month "$REPORTING_MONTH" \
            --site "$SITE_CODE" \
            --output-dir "reports/" \
            --format "pdf,html,csv"
      
      - name: Clinical Validation
        env:
          REPORT_TYPE: ${{ matrix.report_type }}
        run: |
          echo "Running clinical validation for $REPORT_TYPE report"
          
          python src/clinical_validator.py \
            --report-path "reports/${REPORT_TYPE}_report.html" \
            --validation-rules "config/clinical_validation_rules.json" \
            --output "reports/${REPORT_TYPE}_validation.json"
      
      - name: Upload Report Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: clinical-reports-${{ matrix.report_type }}
          path: reports/
          retention-days: 90

  clinical_review_notification:
    name: Notify Clinical Teams
    runs-on: ubuntu-latest
    needs: [data_quality_check, generate_clinical_reports]
    if: always() && needs.data_quality_check.outputs.data_quality_passed == 'true'
    
    steps:
      - name: Create Clinical Review Issue
        uses: actions/github-script@v6
        env:
          REPORTING_MONTH: ${{ github.event.inputs.reporting_month || '2024-01' }}
          SITE_CODE: ${{ github.event.inputs.site_code || 'CARDIFF' }}
          DATA_COMPLETENESS: ${{ needs.data_quality_check.outputs.data_completeness }}
        with:
          script: |
            const reportingMonth = process.env.REPORTING_MONTH;
            const siteCode = process.env.SITE_CODE;
            const dataCompleteness = process.env.DATA_COMPLETENESS;
            
            const issueTitle = `[CLINICAL REVIEW] Monthly Reports - ${siteCode} - ${reportingMonth}`;
            const issueBody = `
            ## Monthly Clinical Reports Ready for Review
            
            **Reporting Period:** ${reportingMonth}  
            **Site:** ${siteCode}  
            **Data Quality:** ${dataCompleteness}% completeness  
            **Generated:** ${new Date().toISOString()}
            
            ### Reports Generated
            - [x] Patient Safety Indicators
            - [x] Quality Indicators Dashboard  
            - [x] Operational Metrics Summary
            
            ### Clinical Review Checklist
            - [ ] Clinical accuracy validation completed
            - [ ] Methodology review by clinical lead
            - [ ] Data interpretation verification
            - [ ] Stakeholder notification sent
            - [ ] Reports published to clinical dashboard
            
            ### Artifacts
            Reports and validation results are available in the [Actions artifacts](${context.payload.repository.html_url}/actions/runs/${context.runId}).
            
            **Clinical Lead:** Please review and approve for publication.
            
            ---
            *This issue was automatically generated by the Monthly Clinical Reports workflow.*
            `;
            
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: issueTitle,
              body: issueBody,
              labels: ['clinical-review', 'monthly-reports', 'needs-approval'],
              assignees: ['clinical-lead-cardiff'] // Replace with actual usernames
            });
      
      - name: Send Teams Notification
        env:
          TEAMS_WEBHOOK: ${{ secrets.NHS_WALES_TEAMS_WEBHOOK }}
          REPORTING_MONTH: ${{ github.event.inputs.reporting_month || '2024-01' }}
          SITE_CODE: ${{ github.event.inputs.site_code || 'CARDIFF' }}
        run: |
          echo "Sending notification to NHS Wales Teams channel..."
          
          curl -H "Content-Type: application/json" -X POST -d '{
            "type": "message",
            "attachments": [{
              "contentType": "application/vnd.microsoft.card.adaptive",
              "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.3",
                "body": [{
                  "type": "TextBlock",
                  "text": "📊 Monthly Clinical Reports Generated",
                  "weight": "Bolder",
                  "size": "Medium"
                }, {
                  "type": "FactSet",
                  "facts": [{
                    "title": "Site:",
                    "value": "'"$SITE_CODE"'"
                  }, {
                    "title": "Period:",
                    "value": "'"$REPORTING_MONTH"'"
                  }, {
                    "title": "Status:",
                    "value": "Ready for Clinical Review"
                  }]
                }],
                "actions": [{
                  "type": "Action.OpenUrl",
                  "title": "View Reports",
                  "url": "'"$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"'"
                }]
              }
            }]
          }' "$TEAMS_WEBHOOK"

  deployment_approval:
    name: Production Deployment
    runs-on: ubuntu-latest
    needs: [generate_clinical_reports, clinical_review_notification]
    environment: production
    if: github.event.inputs.site_code == 'ALL_SITES'
    
    steps:
      - name: Deploy Reports to Production
        env:
          PRODUCTION_SERVER: ${{ secrets.NHS_WALES_PRODUCTION_SERVER }}
          DEPLOYMENT_KEY: ${{ secrets.PRODUCTION_DEPLOYMENT_KEY }}
        run: |
          echo "Deploying monthly reports to production dashboard..."
          
          # Download all report artifacts
          # Deploy to NHS Wales clinical dashboard
          # Update production databases
          # Notify stakeholders of publication
          
          echo "Production deployment completed successfully"
```

### Integration

#### Workflow Integration Patterns

```text
NHS Wales Integration Architecture:
├── 🔐 Authentication and Authorization
│   ├── Azure Active Directory integration
│   ├── NHS Wales service accounts
│   ├── Role-based access controls
│   └── Multi-factor authentication
├── 📊 Data Source Connections
│   ├── NHS Wales data warehouse
│   ├── Patient Administration Systems (PAS)
│   ├── Electronic Health Records (EHR)
│   └── National data feeds
├── 🚀 Deployment Targets
│   ├── NHS Wales clinical dashboards
│   ├── Power BI service integration
│   ├── SharePoint document libraries
│   └── Clinical portal systems
└── 📢 Notification Systems
    ├── Microsoft Teams integration
    ├── Email notifications to clinical leads
    ├── Dashboard alert systems
    └── Mobile app notifications
```

---

## 🎯 Next Session Preview

**Session 8: Group Exercises and Consolidation**

- Comprehensive hands-on workshop scenarios
- Real-world NHS Wales case studies and simulations
- Skills assessment and competency validation
- Team collaboration exercises
- Next steps and continuing development roadmap

---

## 📚 Additional Resources

- [GitHub Issues Guide](../Technical_Configuration/README.md)
- [GitHub Projects Documentation](../Technical_Configuration/Service_Management_and_SLA.md)
- [NHS Wales Workflow Standards](../Workflow_Management/)
- [GitHub Actions Healthcare Examples](../Technical_Configuration/Integrating_GitHub_Into_Tools.md)

---

*Session 7 of 8 | GitHub GIG Cymru Training Series*  
*ABUHB BIU | Business Intelligence Unit*