# Participant Details

- **Name:** Susmi Mariam Varughese
- **Team:** BI & Value - Finance
- **Today I want to learn:** GitHub

## What is in this folder

| File | Added in |
|------|----------|
| README.md | Session 2 |

## Patient analytics pipeline

The module uses fabricated data for training only; it is not for clinical use.

```mermaid
flowchart TD
    A[CLI arguments: count, seed, output format] --> B[Audit session]
    B --> C[Generate fictional patients and encounters]
    C --> D[Assess each patient]
    D --> E[Apply risk rules]
    E --> F[Risk score, tier, and reasons]
    F --> G{Output format}
    G -->|Text report| H[Cohort statistics, tier breakdown, condition prevalence, top patients]
    G -->|CSV| I[Assessment rows]
```
