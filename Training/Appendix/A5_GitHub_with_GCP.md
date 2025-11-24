# Session 4: GitHub with GCP Context

**Duration**: 30 minutes  
**Time**: 10:45 - 11:15

## 🎯 Learning Objectives

By the end of this session, you will understand:
- How GitHub integrates with Google Cloud Platform (GCP)
- CI/CD pipelines using GitHub Actions and Cloud Build
- Deploying applications to GCP services from GitHub
- Managing secrets and credentials securely
- Best practices for cloud-native development workflows

---

## GitHub and GCP Integration Overview

### Why Integrate GitHub with GCP?

The Aneurin Bevan University Health Board uses both GitHub and GCP extensively. Integration enables:

- **Automated Deployments**: Code changes automatically deploy to cloud infrastructure
- **Continuous Integration**: Automated testing in cloud environments
- **Infrastructure as Code**: Manage GCP resources via GitHub repositories
- **Secure Pipelines**: Managed secrets and workload identity
- **Scalable Builds**: Leverage GCP's compute power for builds

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                      GitHub                              │
│                                                          │
│  ┌─────────────┐      ┌──────────────┐     ┌─────────┐ │
│  │ Source Code │──►   │ GitHub       │──►  │ Actions │ │
│  │ Repository  │      │ Actions      │     │ Runners │ │
│  └─────────────┘      └──────────────┘     └────┬────┘ │
└───────────────────────────────────────────────────┼──────┘
                                                    │
                            Workload Identity       │
                            Authentication          │
                                                    ▼
┌─────────────────────────────────────────────────────────┐
│              Google Cloud Platform (GCP)                 │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ Cloud Build  │  │ Cloud Run    │  │ GKE           │ │
│  └──────────────┘  └──────────────┘  └───────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ BigQuery     │  │ Cloud Storage│  │ Secret Manager│ │
│  └──────────────┘  └──────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## GitHub Actions for GCP

### What are GitHub Actions?

**GitHub Actions** is GitHub's built-in CI/CD platform. It allows you to automate workflows triggered by GitHub events (push, pull request, release, etc.).

### Basic GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GCP

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy my-service \
            --source . \
            --region europe-west2 \
            --platform managed
```

### Key GitHub Actions Concepts

#### 1. **Triggers (on)**
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  workflow_dispatch:  # Manual trigger
```

#### 2. **Jobs**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm test
  
  deploy:
    needs: build  # Runs after build
    runs-on: ubuntu-latest
    steps:
      - run: deploy.sh
```

#### 3. **Steps**
- Individual tasks in a job
- Can use actions from marketplace
- Can run shell commands

#### 4. **Runners**
- Machines that execute workflows
- GitHub-hosted (free minutes included)
- Self-hosted (your own infrastructure)

---

## GCP Services Integration

### 1. Cloud Build

**Cloud Build** is GCP's managed CI/CD service. It can be triggered from GitHub.

#### Setup Cloud Build with GitHub

```yaml
# cloudbuild.yaml in repository root
steps:
  # Build container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-app:$SHORT_SHA', '.']
  
  # Run tests
  - name: 'gcr.io/$PROJECT_ID/my-app:$SHORT_SHA'
    args: ['npm', 'test']
  
  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-app:$SHORT_SHA']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-app'
      - '--image=gcr.io/$PROJECT_ID/my-app:$SHORT_SHA'
      - '--region=europe-west2'
      - '--platform=managed'

images:
  - 'gcr.io/$PROJECT_ID/my-app:$SHORT_SHA'
```

#### Connect GitHub to Cloud Build

1. **In GCP Console**:
   - Navigate to Cloud Build → Triggers
   - Click "Connect Repository"
   - Select GitHub and authorize
   - Choose your repository

2. **Create Trigger**:
   - Name: "Deploy on main branch"
   - Event: Push to branch
   - Branch: `^main$`
   - Build configuration: Cloud Build configuration file
   - Location: `cloudbuild.yaml`

### 2. Cloud Run

**Cloud Run** is a fully managed container platform. Perfect for APIs and web services.

#### Deploy to Cloud Run from GitHub Actions

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

env:
  PROJECT_ID: abb-analytics-platform
  SERVICE_NAME: patient-dashboard
  REGION: europe-west2

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      id-token: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2
      
      - name: Build and deploy
        run: |
          gcloud builds submit \
            --tag gcr.io/${{ env.PROJECT_ID }}/${{ env.SERVICE_NAME }}
          
          gcloud run deploy ${{ env.SERVICE_NAME }} \
            --image gcr.io/${{ env.PROJECT_ID }}/${{ env.SERVICE_NAME }} \
            --region ${{ env.REGION }} \
            --platform managed \
            --allow-unauthenticated
```

### 3. Google Kubernetes Engine (GKE)

**GKE** provides managed Kubernetes clusters for containerized applications.

#### Deploy to GKE

```yaml
name: Deploy to GKE

on:
  push:
    branches: [main]

env:
  PROJECT_ID: abb-gke-production
  GKE_CLUSTER: production-cluster
  GKE_ZONE: europe-west2-a
  DEPLOYMENT_NAME: analytics-api

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2
      
      - name: Configure kubectl
        run: |
          gcloud container clusters get-credentials ${{ env.GKE_CLUSTER }} \
            --zone ${{ env.GKE_ZONE }}
      
      - name: Build and push Docker image
        run: |
          docker build -t gcr.io/${{ env.PROJECT_ID }}/${{ env.DEPLOYMENT_NAME }}:${{ github.sha }} .
          gcloud auth configure-docker
          docker push gcr.io/${{ env.PROJECT_ID }}/${{ env.DEPLOYMENT_NAME }}:${{ github.sha }}
      
      - name: Deploy to GKE
        run: |
          kubectl set image deployment/${{ env.DEPLOYMENT_NAME }} \
            ${{ env.DEPLOYMENT_NAME }}=gcr.io/${{ env.PROJECT_ID }}/${{ env.DEPLOYMENT_NAME }}:${{ github.sha }}
          kubectl rollout status deployment/${{ env.DEPLOYMENT_NAME }}
```

### 4. BigQuery

**BigQuery** is GCP's serverless data warehouse. Ideal for analytics workloads.

#### Deploy BigQuery Scripts

```yaml
name: Deploy BigQuery Views

on:
  push:
    branches: [main]
    paths:
      - 'bigquery/**'

jobs:
  deploy-views:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Deploy views
        run: |
          for view in bigquery/views/*.sql; do
            view_name=$(basename "$view" .sql)
            bq query --use_legacy_sql=false < "$view"
            echo "Deployed view: $view_name"
          done
```

### 5. Cloud Functions

**Cloud Functions** are serverless functions for event-driven processing.

#### Deploy Cloud Function

```yaml
name: Deploy Cloud Function

on:
  push:
    branches: [main]
    paths:
      - 'functions/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Deploy function
        run: |
          gcloud functions deploy process-patient-data \
            --runtime python311 \
            --trigger-http \
            --entry-point main \
            --source functions/ \
            --region europe-west2 \
            --allow-unauthenticated
```

---

## Authentication and Security

### Workload Identity Federation (Recommended)

**Workload Identity Federation** allows GitHub Actions to authenticate to GCP without storing service account keys.

#### Setup Process

**1. Create Workload Identity Pool**
```bash
gcloud iam workload-identity-pools create "github-actions-pool" \
  --project="abb-analytics-platform" \
  --location="global" \
  --display-name="GitHub Actions Pool"
```

**2. Create Workload Identity Provider**
```bash
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="abb-analytics-platform" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

**3. Grant Permissions**
```bash
gcloud iam service-accounts add-iam-policy-binding "github-actions@abb-analytics-platform.iam.gserviceaccount.com" \
  --project="abb-analytics-platform" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/Aneurin-Bevan-University-Health-Board/biu_analytics_dashboard"
```

**4. Add to GitHub Secrets**
```
WIF_PROVIDER: projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider
SERVICE_ACCOUNT: github-actions@abb-analytics-platform.iam.gserviceaccount.com
```

### GCP Secret Manager Integration

Store sensitive configuration in **Secret Manager**, not in code or GitHub Secrets.

```yaml
- name: Access secret
  run: |
    DB_PASSWORD=$(gcloud secrets versions access latest --secret="db-password")
    export DB_PASSWORD
    ./deploy.sh
```

---

## Infrastructure as Code

### Terraform with GitHub

Manage GCP infrastructure using **Terraform** stored in GitHub.

#### Repository Structure
```
biu_infrastructure/
├── .github/
│   └── workflows/
│       ├── terraform-plan.yml
│       └── terraform-apply.yml
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
└── modules/
    ├── bigquery/
    ├── cloud-run/
    └── gke/
```

#### Terraform Plan Workflow
```yaml
name: Terraform Plan

on:
  pull_request:
    branches: [main]

jobs:
  plan:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Terraform Init
        run: terraform init
        working-directory: environments/production
      
      - name: Terraform Plan
        run: terraform plan -no-color
        working-directory: environments/production
```

#### Terraform Apply Workflow
```yaml
name: Terraform Apply

on:
  push:
    branches: [main]

jobs:
  apply:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Terraform Init
        run: terraform init
        working-directory: environments/production
      
      - name: Terraform Apply
        run: terraform apply -auto-approve
        working-directory: environments/production
```

---

## ABB Use Cases

### 1. Business Intelligence Dashboard Deployment

**Repository**: `biu_analytics_dashboard`

```yaml
# .github/workflows/deploy.yml
name: Deploy BI Dashboard

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
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy analytics-dashboard \
            --source . \
            --region europe-west2 \
            --platform managed \
            --set-env-vars="BQ_PROJECT=abb-analytics"
```

### 2. ETL Pipeline Deployment

**Repository**: `biu_etl_pipelines`

```yaml
name: Deploy ETL to Cloud Composer

on:
  push:
    branches: [main]
    paths:
      - 'dags/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Deploy DAGs to Composer
        run: |
          gsutil -m cp -r dags/* \
            gs://europe-west2-abb-composer-bucket/dags/
```

### 3. Data Warehouse Schema Updates

**Repository**: `biu_bigquery_schemas`

```yaml
name: Update BigQuery Schemas

on:
  push:
    branches: [main]

jobs:
  update-schemas:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Authenticate to GCP
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}
      
      - name: Update tables
        run: |
          python scripts/update_schemas.py
```

---

## Best Practices

### 1. Environment Management

**Use GitHub Environments** for deployment protection:

```yaml
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.abb.wales.nhs.uk
    steps:
      # deployment steps
```

Benefits:
- Require manual approval before production deploys
- Different secrets per environment
- Deployment history tracking
- Protection rules

### 2. Least Privilege

**Service accounts should have minimal permissions:**

```bash
# ❌ Bad: Too broad
roles/owner

# ✅ Good: Specific permissions
roles/run.admin
roles/storage.objectViewer
roles/cloudbuild.builds.builder
```

### 3. Separate Environments

**Different GCP projects for different environments:**

```
Development:   abb-analytics-dev
Staging:       abb-analytics-staging
Production:    abb-analytics-prod
```

### 4. Monitoring and Alerting

**Add status checks:**

```yaml
- name: Check deployment health
  run: |
    # Wait for service to be ready
    sleep 30
    
    # Health check
    response=$(curl -s -o /dev/null -w "%{http_code}" https://api.abb.wales.nhs.uk/health)
    
    if [ $response != "200" ]; then
      echo "Health check failed"
      exit 1
    fi
```

### 5. Rollback Strategy

**Tag releases for easy rollback:**

```yaml
- name: Tag release
  run: |
    gcloud run deploy my-service \
      --image gcr.io/$PROJECT_ID/my-service:${{ github.sha }} \
      --tag pr-${{ github.event.pull_request.number }}
```

---

## Common Patterns

### Pattern 1: Multi-Environment Deployment

```yaml
name: Deploy Multi-Environment

on:
  push:
    branches:
      - develop
      - staging
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set environment
        run: |
          if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            echo "ENV=production" >> $GITHUB_ENV
            echo "PROJECT_ID=abb-prod" >> $GITHUB_ENV
          elif [[ "${{ github.ref }}" == "refs/heads/staging" ]]; then
            echo "ENV=staging" >> $GITHUB_ENV
            echo "PROJECT_ID=abb-staging" >> $GITHUB_ENV
          else
            echo "ENV=development" >> $GITHUB_ENV
            echo "PROJECT_ID=abb-dev" >> $GITHUB_ENV
          fi
      
      - name: Deploy to ${{ env.ENV }}
        run: |
          gcloud run deploy app --project=${{ env.PROJECT_ID }}
```

### Pattern 2: Automated Testing

```yaml
name: Test and Deploy

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
      - run: npm run lint
  
  deploy:
    needs: test  # Only deploy if tests pass
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      # deployment steps
```

### Pattern 3: Preview Environments

```yaml
name: PR Preview

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy preview
        run: |
          gcloud run deploy app-pr-${{ github.event.pull_request.number }} \
            --source . \
            --tag pr-${{ github.event.pull_request.number }}
      
      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'Preview: https://pr-${{ github.event.pull_request.number }}---app-hash.run.app'
            })
```

---

## Troubleshooting

### Common Issues

#### 1. Authentication Failures
```
Error: Failed to authenticate to GCP
```

**Solution**: Check Workload Identity configuration
```bash
gcloud iam service-accounts get-iam-policy SERVICE_ACCOUNT
```

#### 2. Permission Denied
```
Error: Permission denied on resource
```

**Solution**: Grant required IAM roles
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT" \
  --role="roles/REQUIRED_ROLE"
```

#### 3. Build Timeouts
```
Error: Build exceeded timeout
```

**Solution**: Increase timeout or optimize build
```yaml
- name: Build with timeout
  run: gcloud builds submit --timeout=20m
```

---

## Summary

### Key Takeaways

✅ **GitHub Actions** provides powerful CI/CD for GCP deployments  
✅ **Workload Identity** enables secure, keyless authentication  
✅ **Cloud Build** can be triggered directly from GitHub  
✅ **Multiple GCP services** integrate seamlessly with GitHub  
✅ **Infrastructure as Code** can be managed through GitHub  
✅ **ABB leverages** GitHub + GCP for modern cloud development

### ABB Integration Status

| Repository Type | Integration | Status |
|----------------|-------------|--------|
| **Analytics Dashboards** | Cloud Run | ✅ Active |
| **ETL Pipelines** | Cloud Composer | ✅ Active |
| **Data Schemas** | BigQuery | ✅ Active |
| **Infrastructure** | Terraform + GCP | ✅ Active |

### Next Session Preview

In **Session 5: GitHub Components**, we'll explore:
- Repositories structure and management
- Issues and project tracking
- Pull requests workflow
- Projects for planning
- Wikis and discussions

---

## Additional Resources

- [GitHub Actions for GCP](https://github.com/google-github-actions)
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Cloud Build with GitHub](https://cloud.google.com/build/docs/automating-builds/github/build-repos-from-github)
- [Terraform on GCP](https://cloud.google.com/docs/terraform)
- [GCP Best Practices](https://cloud.google.com/architecture/framework)

---

*Session 4 of 7 | GitHub Training Package*  
*Aneurin Bevan University Health Board*
