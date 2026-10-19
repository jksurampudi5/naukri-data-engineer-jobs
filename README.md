# 🔍 Naukri Data Engineer Jobs Pipeline & Market Analytics

[![CI - Test Suite](https://img.shields.io/badge/pytest-passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A specialized ingestion and market intelligence pipeline focused on the Indian Data Engineering job market (Naukri.com platform conventions). It parses, normalizes, and aggregates skill trends, experience requirements, compensation tiers, and location hubs (Bangalore, Hyderabad, Pune, Chennai, and Remote).

---

## 🌟 Key Features

* **Market-Specific Parsers**: Normalizes Indian job market formats including experience ranges (`"3-6 Yrs"`), salary brackets in Lakhs Per Annum (`"14-22 Lacs P.A."`), and regional tech hub aliases (`"Bangalore/Bengaluru"`, `"Hyderabad/Secunderabad"`).
* **DE Skills Trend Engine**: Tracks demand frequency and percentage share for Lakehouse (PySpark, Databricks, Delta Lake), Orchestration (Airflow, ADF), and Modern Data Stack (dbt, Snowflake, Redshift).
* **Safe Offline Mock Architecture**: Includes deterministic fixture playback mode (`offline_mode=True`) preventing rate-limits, IP bans, or network failures in CI/CD pipelines.
* **Compensation & Hub Analytics**: Computes average salary bands and regional hiring concentrations.
* **Strict Privacy Guardrails**: Zero storage or exposure of personal resumes, applicant contact information, or sensitive credentials. All demonstration datasets are synthetic and fictional.

---

## 🏗️ Architecture

```
                       ┌──────────────────────────────┐
                       │   Fictional Naukri Feed      │
                       │       (JSON Fixtures)        │
                       └──────────────┬───────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │     NaukriScraperClient      │
                       │   (Safe Rate-Limited Mode)   │
                       └──────────────┬───────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │        NaukriParser          │
                       │ (Exp, Salary & Hub Normalizer)│
                       └──────────────┬───────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │    MarketAnalyticsEngine     │
                       │ (Skill Share & Distribution) │
                       └──────────────┬───────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │         DataExporter         │
                       │ (Markdown / CSV Intelligence)│
                       └──────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and set up a Python virtual environment:

```bash
git clone https://github.com/jksurampudi5/naukri-data-engineer-jobs.git
cd naukri-data-engineer-jobs

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Market Analytics

Execute the analytics CLI over the included sample dataset:

```bash
# View market summary with top 5 in-demand skills
python3 -m src.naukri_de.cli --sample data/sample/fictional_naukri_jobs.json --top 5

# Generate full Markdown intelligence report
python3 -m src.naukri_de.cli --sample data/sample/fictional_naukri_jobs.json --report
```

### 3. Run Tests

Execute the automated test suite:

```bash
pytest -v
```

---

## 📂 Repository Structure

```
naukri-data-engineer-jobs/
├── .gitignore                      # Strict exclusions for scraping logs, resumes, and credentials
├── README.md                       # Project documentation
├── requirements.txt                # Project dependencies
├── setup.py                        # Package distribution configuration
├── pytest.ini                      # Test runner configuration
├── data/
│   └── sample/
│       └── fictional_naukri_jobs.json # Sanitized fictional Indian tech market DE jobs
├── src/
│   └── naukri_de/
│       ├── __init__.py             # Package exports
│       ├── analytics.py            # Market trends & skill aggregation engine
│       ├── cli.py                  # Command-line interface
│       ├── client.py               # Intake client with offline fallback
│       ├── exporter.py             # Markdown and CSV report exporter
│       ├── models.py               # Data models and structures
│       └── parser.py               # Experience, salary, and hub normalizer
└── tests/
    ├── test_analytics.py           # Market aggregation unit tests
    ├── test_cli.py                 # CLI integration tests
    ├── test_client.py              # Client fixture loading tests
    └── test_parser.py              # Parser & attribute extraction tests
```

---

## 🔒 Privacy & Open-Source Security

* This repository is configured to **strictly exclude** personal resumes (`.pdf`, `.docx`), phone numbers, email addresses, `.env` files, API keys, and local SQLite databases (`*.db`, `*.sqlite`).
* All included datasets are **synthetic and fictional**.
* Intended for demonstration of Data Engineering pipeline design, testing, and portfolio display.