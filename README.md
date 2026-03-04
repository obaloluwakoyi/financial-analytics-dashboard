# Financial Analytics Dashboard & Automation System

## Project Overview

This project is a Python-based financial analytics dashboard designed to support **data-driven decision-making for Micro, Small, and Medium Enterprises (MSMEs)**. It automates the ingestion, cleaning, storage, analysis, and reporting of financial data, transforming raw records into structured insights suitable for research, operational monitoring, and policy-oriented analysis.

The system is built with a focus on **data quality, transparency, and reproducibility**, making it suitable for analytical environments where accuracy and clarity are critical.

---

## Problem Statement

Many MSMEs maintain financial records in fragmented formats such as Excel sheets and PDF files. These records are often inconsistent, error-prone, and difficult to analyze at scale. This limits the ability of decision-makers, researchers, and policymakers to extract reliable insights.

This project addresses that challenge by:

* Standardizing heterogeneous financial data
* Enforcing validation and quality checks
* Automating reporting and visualization
* Producing clear, decision-ready outputs

---

## Key Features

* Interactive financial dashboard for real-time data exploration
* Automated data ingestion from Excel and PDF sources
* Data cleaning, normalization, and validation pipelines
* Structured storage using a relational database (SQLite)
* Automated report generation with charts and PDF summaries
* Centralized logging for transparency and traceability

---

## Data Sources

* Excel financial records (e.g., income, expenses, transactions)
* PDF financial documents and reports uploaded by users

All data inputs are validated and standardized before analysis.

---

## Data Cleaning & Validation

The system applies multiple data quality controls, including:

* Column name normalization
* Data type enforcement (dates, numeric values)
* Missing value handling
* Consistency checks across financial fields
* Error logging for auditability

These steps ensure that downstream analysis is based on reliable and structured data.

---

## Analysis & Reporting

Once validated, the data is:

* Stored in a structured SQLite database
* Queried for trend analysis and performance indicators
* Visualized through an interactive dashboard
* Summarized in automated PDF reports suitable for executive or research review

The outputs are designed to support:

* Financial performance monitoring
* MSME operational decision-making
* Research and policy-oriented analysis

---

## Tools & Technologies

* **Python** (Pandas, Streamlit)
* **SQL** (SQLite, SQLAlchemy)
* **Data Visualization** (Matplotlib)
* **Automation & Logging**
* **Docker** for reproducible deployment

---

## Project Structure

```
├── app.py                # Streamlit dashboard interface
├── automation.py         # Data ingestion, cleaning, and ETL logic
├── database.py           # Database schema and SQL operations
├── make_pdf.py           # Automated PDF report generation
├── logger.py             # Centralized logging and error tracking
├── requirements.txt      # Project dependencies
├── Dockerfile            # Deployment configuration
└── README.md             # Project documentation
```

---

## Impact & Use Cases

This project demonstrates how automated data systems can:

* Improve financial transparency for MSMEs
* Support evidence-based business decisions
* Enable researchers to work with clean, structured datasets
* Assist policy-focused organizations with reliable analytical outputs

---

## Future Improvements

* Integration with cloud databases
* Enhanced statistical analysis modules
* Role-based access control
* Policy indicator dashboards (e.g., MSME growth metrics)

---

## Author

**Obaloluwa Temidayo Koyi-Kayode**
Data Analyst | Mathematics Graduate
