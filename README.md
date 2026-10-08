# SkillBridge – Mobilisation, Training & Placement Analytics System

SkillBridge is a Python-based data analytics and machine learning application designed to analyse the complete candidate journey from **mobilisation and enrolment to training and placement**.

The application allows users to upload candidate datasets in CSV, Excel, SQL, or SQLite format and automatically generates actionable insights, performance KPIs, visual reports, candidate-risk analysis, and downloadable Excel reports.

---
<img width="1853" height="889" alt="image" src="https://github.com/user-attachments/assets/b88f3ded-f56e-4884-a103-f5e792e93d6e" />

## Key Features

### 1. Data Upload & Automatic Analysis

Upload candidate data in:

* CSV
* Excel (.xlsx, .xls)
* SQL (.sql)
* SQLite (.db, .sqlite)

SkillBridge automatically reads the uploaded dataset and identifies relevant fields based on column names.

The system can recognise information related to:

* Placement status
* Salary / CTC
* Assessment scores
* Attendance
* Course / programme
* Mobilisation source
* Location / district
* Employer / company

---

## 2. Mobilisation Analytics

Analyse how candidates are being mobilised and enrolled.

The system provides insights into:

* Candidate sources
* Referral performance
* Job fairs
* Camps
* Social media
* Candidate distribution by location
* Course-wise enrolment
* Mobilisation trends

This helps identify which channels and locations are generating the highest number of candidates.

---

## 3. Training Analytics

SkillBridge analyses training-related information such as:

* Attendance
* Assessment scores
* Course performance
* Candidate performance distribution
* Course-wise outcomes
* Training performance patterns

The system also generates statistical summaries for available numerical fields.

---

## 4. Placement Analytics

The application calculates important placement KPIs including:

* Total candidates
* Placement rate
* Number of placed candidates
* Number of candidates not placed
* Average salary
* Placement rate by course
* Employer distribution
* Candidate placement outcomes

This allows users to evaluate the effectiveness of different training programmes and placement activities.

---

## 5. Machine Learning

SkillBridge includes machine-learning functionality for candidate analysis.

### Placement Prediction

When a suitable placement outcome field is available, the system uses a:

**Random Forest Classifier**

to estimate placement probability.

The model uses available candidate attributes such as:

* Attendance
* Assessment scores
* Course
* Location
* Mobilisation source
* Other suitable numerical/categorical attributes

The application performs cross-validation and reports the model's cross-validated accuracy.

It also identifies the most influential features associated with placement outcomes.

---

## 6. Candidate Risk Identification

SkillBridge identifies candidates who are currently not placed and ranks them according to their predicted placement probability.

This creates an actionable list of candidates who may require additional:

* Training
* Counselling
* Interview preparation
* Career guidance
* Employer matching
* Placement support

The purpose is to help training and placement teams prioritise candidates who need additional intervention.

---

## 7. Candidate Segmentation

If the uploaded dataset does not contain a suitable placement outcome field, SkillBridge can automatically perform candidate segmentation using:

**K-Means Clustering**

The system groups candidates into three segments based on available numerical and categorical features.

This can help identify different candidate profiles and support targeted training or counselling strategies.

---

## 8. Visual Analytics

The generated report can include visualisations such as:

* Mobilisation by source
* Candidates by location
* Enrolment by course
* Top employers
* Placement rate by course
* Placed vs. not placed
* Assessment score distribution
* Placement-driving features

The reporting interface provides an interactive dashboard-style presentation of the analysis.

---

## 9. Excel Reporting

SkillBridge automatically generates a downloadable Excel report containing:

* KPI summaries
* Candidate action lists
* Numerical statistics
* Analytical results

This makes the output suitable for further reporting and operational use.

---

# Technology Stack

## Backend

* Python
* Flask

## Data Analysis

* Pandas
* NumPy

## Machine Learning

* Scikit-learn
* Random Forest
* K-Means Clustering
* Cross-validation

## Data Sources

* CSV
* Excel
* SQL
* SQLite

## Reporting

* Excel
* OpenPyXL
* HTML reports
* Chart.js

## Deployment

* Gunicorn
* Render

---

# Project Architecture

```text
SkillBridge
│
├── app.py
│
├── templates/
│   ├── index.html
│   ├── report.html
│   └── base.html
│
├── static/
│   └── ...
│
├── sample_candidates.csv
├── requirements.txt
├── render.yaml
├── README.md
└── LICENSE
```

---

# Application Workflow

```text
                 Candidate Dataset
                        │
                        ▼
                Upload Data File
                        │
                        ▼
                 Data Processing
                        │
                        ▼
              Automatic Column Detection
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     Mobilisation    Training     Placement
       Analysis      Analysis      Analysis
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                  KPI Generation
                        │
                        ▼
               Exploratory Analytics
                        │
                        ▼
              Machine Learning Layer
                 │              │
                 ▼              ▼
          Placement Model    K-Means
          Random Forest     Segmentation
                 │              │
                 └──────┬───────┘
                        ▼
                 Actionable Insights
                        │
                        ▼
                Candidate Risk List
                        │
                        ▼
                Excel Report Export
```

---

# Sample Dataset

The repository includes a sample candidate dataset containing fields such as:

```text
candidate_id
name
source
district
course
attendance
assessment_score
placement_status
salary
```

The sample data represents candidates across different mobilisation channels, districts, training courses, attendance levels, assessment scores, placement outcomes, and salaries.

---

# Example Analysis

For a suitable dataset, SkillBridge can produce KPIs such as:

```text
Records
Columns
Missing Cells
Duplicates Removed
Placement Rate
Average Assessment Score
Average Attendance
Average Salary
```

It can also generate findings such as:

```text
Candidates placed: X
Placement rate: X%

Best converting course: XXXXX
Weakest converting course: XXXXX

Strongest placement drivers:
1. XXXXX
2. XXXXX
3. XXXXX
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/IB-Indraditya/SkillBridge-student-management-system.git
```

## 2. Open the project

```bash
cd SkillBridge-student-management-system
```

## 3. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Run the application

```bash
python app.py
```

The application will start locally.

Open the displayed local Flask URL in your browser.

---

# Deployment

The project includes a `render.yaml` configuration for deployment on Render.

The production server uses:

```bash
gunicorn app:app --timeout 120 --workers 1
```

Python version configured for deployment:

```text
3.11.9
```

---

# How to Use

1. Open the SkillBridge application.
2. Select a candidate dataset.
3. Upload the CSV, Excel, SQL, or SQLite file.
4. Click **Build Report**.
5. SkillBridge processes the dataset.
6. Review the generated KPIs and insights.
7. Analyse mobilisation, training, and placement performance.
8. Review machine-learning results.
9. Identify candidates requiring additional support.
10. Download the generated Excel report.

---

# Machine Learning Methodology

The placement prediction workflow includes:

```text
Raw Candidate Data
        ↓
Data Cleaning
        ↓
Duplicate Removal
        ↓
Feature Detection
        ↓
Missing Value Handling
        ↓
Categorical Encoding
        ↓
Feature Preparation
        ↓
Random Forest Classification
        ↓
Cross-Validated Prediction
        ↓
Accuracy Evaluation
        ↓
Feature Importance
        ↓
Candidate Placement Probability
```

For datasets without a suitable placement outcome:

```text
Candidate Data
      ↓
Feature Preparation
      ↓
Standardisation
      ↓
K-Means Clustering
      ↓
3 Candidate Segments
      ↓
Segment Profiles
```

---

# Business Use Cases

SkillBridge can support organisations involved in:

* Student mobilisation
* Skill development
* Vocational training
* Candidate counselling
* Training management
* Employability programmes
* Placement operations
* Workforce development
* NGO training programmes
* CSR skill-development initiatives

The analytics can help programme teams understand **where candidates are coming from, how they are performing during training, which programmes produce better placement outcomes, and which candidates may require additional intervention.**

---

# Project Highlights

* Automated dataset analysis
* Flexible column detection
* Multi-format data ingestion
* Mobilisation analytics
* Training performance analytics
* Placement analytics
* Random Forest placement prediction
* K-Means candidate segmentation
* Feature importance analysis
* Candidate risk prioritisation
* Interactive charts
* Automated Excel reporting
* Cross-validation
* Deployable Flask application

---

# Future Enhancements

Potential future improvements include:

* Student login and profile management
* Trainer dashboard
* Batch management
* Attendance management
* Employer management
* Job vacancy management
* Interview scheduling
* Automated candidate-job matching
* Placement follow-up tracking
* PostgreSQL/MySQL integration
* Role-based authentication
* Advanced ML models
* Automated email/SMS notifications
* Power BI integration
* REST API
* Real-time operational dashboard

---

# License

This project is licensed under the MIT License.

---

## Author

**Indraditya Bhattacharyya**

GitHub:
https://github.com/IB-Indraditya

---

## Project Summary

**SkillBridge** transforms candidate data into actionable mobilisation, training, and placement insights using **Python, Flask, Pandas, NumPy, and Scikit-learn**. It combines data analytics, machine learning, candidate-risk identification, and automated reporting into a single application designed around the student-to-employment lifecycle.
