# ServiGo — Service Operations & Partner Performance Analytics

An end-to-end business analytics portfolio project exploring marketplace operations, cancellation patterns, partner performance, and service quality using synthetic data.

## Project Overview

ServiGo simulates a multi-city, on-demand home services marketplace. The project uses data preparation, ETL, SQL analysis, KPI reporting, and interactive Power BI dashboards to investigate operational performance and identify areas for further analysis.

**Objectives**
- Measure order completion, cancellations, and no-shows.
- Identify city and service-category cancellation hotspots.
- Examine cancellation reason codes and partner performance.
- Analyse customer complaints, rework, and partner onboarding.
- Build an interactive operations dashboard.

> **Data disclaimer:** All data is synthetic and generated for portfolio purposes. Findings do not represent a real company or prove causation.

## Dataset

| Attribute | Details |
|---|---|
| Observation period | January–August 2026 |
| Orders | 35,000 |
| Partners | 800 |
| Customers | 25,000 |
| Cities | Delhi NCR, Bengaluru, Mumbai, Pune, Chandigarh |
| Service categories | AC & Appliance Repair; Cleaning & Pest Control; Electricians; Plumbers; Beauty & Spa |
| Onboarding records | 800 |
| Partner-day availability records | 194,400 |

### Main cleaned datasets

- `orders_integrated_clean.csv` — 35,000 rows and 54 columns.
- `availability_monthly_clean.csv` — 6,400 partner-month rows and 5 columns.

## Technology Stack

- **Python:** Synthetic data generation and validation.
- **Alteryx:** Data integration, cleaning, and ETL.
- **MySQL / SQL:** Structured analysis and KPI calculation.
- **Microsoft Excel:** KPI summary and executive reporting.
- **Power BI:** Interactive dashboard and visual analysis.

**Workflow:** Python → Alteryx → MySQL / SQL → Excel → Power BI

## Key Findings

### Marketplace performance

| KPI | Result |
|---|---:|
| Total orders | 35,000 |
| Completed orders | 29,648 |
| Cancelled orders | 4,595 |
| No-show orders | 757 |
| Completion rate | 84.71% |
| Cancellation rate | 13.13% |
| No-show rate | 2.16% |

### Cancellation analysis

| Recorded cancellation reason | Orders |
|---|---:|
| No Partner Available | 1,022 |
| Customer Cancelled | 874 |
| Partner Unavailable | 862 |
| Scheduling Conflict | 803 |
| Partner Rejected | 653 |
| Other | 381 |

Availability-related reason codes accounted for 1,884 cancellations, or **41.00% of all cancellations**. These codes are recorded classifications, not independently verified root causes.

### City-level cancellation rates

| City | Rate |
|---|---:|
| Delhi NCR | 13.38% |
| Mumbai | 13.33% |
| Pune | 12.98% |
| Bengaluru | 12.97% |
| Chandigarh | 12.78% |

Selected city-category hotspots included Delhi NCR AC & Appliance Repair (17.15%), Bengaluru Electricians (16.21%), and Mumbai Cleaning & Pest Control (15.88%).

### Partner performance and quality

| Experience level | Completion | Avg. rating | Complaints | Rework |
|---|---:|---:|---:|---:|
| Experienced | 88.15% | 4.18 | 6.76% | 5.77% |
| Beginner | 88.01% | 4.18 | 7.08% | 5.53% |
| Intermediate | 87.54% | 4.19 | 7.14% | 5.08% |

Overall completed-order complaint and rework rates were 6.97% and 5.49%, respectively.

### Partner onboarding

- Verification passed: 703 partners (87.88%).
- Training completed: 647 partners (80.88%).
- Activated: 617 partners (77.13%).

### Customer segments

Repeat customers accounted for 26,310 orders (75.17%); one-time customers accounted for 8,690 orders (24.83%). Segments are based on the complete observed synthetic dataset, not future behaviour.

## Power BI Dashboard

### Dashboard Preview

<img width="1135" height="521" alt="image" src="https://github.com/user-attachments/assets/30829c75-5494-4e77-a60b-3402107b938b" />



The dashboard contains two pages:

**1. Marketplace Operations Overview**
- Marketplace KPI cards.
- Cancellation rates by city.
- Cancellation hotspots by city and service category.
- Cancellation reasons.
- City, category, and month filters.

**2. Partner Performance & Service Quality**
- Completion rate, average rating, complaint rate, and rework rate by experience level.
- Partner-level performance table.
- City, category, and month filters.

## Business Implications

The analysis suggests several areas for further investigation:
1. Examine availability-related cancellation records alongside assignment and scheduling data.
2. Investigate city-category combinations with elevated cancellation rates.
3. Monitor complaints and rework alongside completion rates and ratings.
4. Review onboarding progression and investigate drop-off between stages.
5. Validate availability-hour definitions before drawing capacity conclusions.

These are proposed investigation priorities, not proven interventions or measured business improvements.

## Limitations

- Data is synthetic and does not describe real marketplace performance.
- Descriptive comparisons do not establish causation.
- Cancellation reason codes do not independently prove root causes.
- The observation period is limited to January–August 2026.
- Partner availability utilization requires further validation before operational conclusions are drawn.
- Customer segments describe the observed history only.

## Project Files

The repository contains the project scripts and analytical deliverables. File names and folders should reflect the actual uploaded files.

- `generate_data.py` — synthetic data generation.
- `validate_data.py` — data validation.
- `ServiGo_ETL.yxmd` — Alteryx workflow.
- `ServiGo_Operations_Dashboard.pbix` — Power BI dashboard.
- SQL analysis script — KPI calculations and analytical queries.
- `ServiGo_Analysis.xlsx` — KPI Summary and Executive Summary.
- Cleaned CSV datasets — analytical inputs used by the workflow.

## Reproducibility

1. Run the Python data-generation script.
2. Validate the generated data.
3. Run the Alteryx ETL workflow.
4. Load the cleaned datasets into MySQL.
5. Execute the SQL analysis.
6. Review the Excel KPI and executive summaries.
7. Open the Power BI dashboard and verify data connections and filter behaviour.

Local paths and database connections may need to be updated on another machine. The dashboard alone may not reproduce the results without its underlying data.

## Future Enhancements

- Root-cause analysis of availability-related cancellations.
- Demand-versus-capacity analysis by city, category, and time.
- Onboarding cohort and activation-time analysis.
- Automated data-quality and KPI reconciliation checks.
- Evaluation of operational interventions using an appropriate comparison design.

Project type: Independent business and operations analytics portfolio project
Tools: Python · Alteryx · MySQL · SQL · Excel · Power BI
**Project type:** Independent business and operations analytics portfolio project  
**Tools:** Python · Alteryx · MySQL · SQL · Excel · Power BI
