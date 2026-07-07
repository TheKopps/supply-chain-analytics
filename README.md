# Supply Chain Analytics

End-to-end supply chain and e-commerce analytics project using a reusable Python analytics framework.

This project analyzes the Brazilian Olist e-commerce dataset to produce business KPIs, data quality checks, automated reports, visualizations and Excel exports.

---

## Project Objective

The goal of this project is to simulate a real Data Analyst / BI Analyst workflow:

- ingest raw business data
- validate data quality
- clean and transform data
- engineer business features
- compute KPIs
- generate visualizations
- export Excel reports
- produce an executive Markdown report

This project is built on top of my reusable Python package:

[analytics-framework](https://github.com/TheKopps/analytics-framework)

---

## Tech Stack

- Python
- pandas
- matplotlib
- openpyxl
- YAML
- Git / GitHub
- analytics-framework
- Power BI later

---

## Dataset

This project uses the Brazilian E-Commerce Public Dataset by Olist.

Expected raw files:

```text
data/raw/
├── olist_customers_dataset.csv
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_products_dataset.csv
├── olist_sellers_dataset.csv
└── olist_order_reviews_dataset.csv
```

Raw data is not tracked in GitHub because of file size and licensing constraints.

---

## Project Structure

```text
supply-chain-analytics/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   └── domain/
│       └── olist_steps.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── powerbi/
│
├── reports/
│   ├── figures/
│   ├── executive_dashboard.xlsx
│   ├── executive_report.md
│   ├── validation_report.csv
│   └── pipeline.log
│
├── notebooks/
└── powerbi/
```

---

## Pipeline

The project pipeline is orchestrated using `analytics-framework`.

```text
Raw CSV Files
      ↓
Multiple CSV Ingestion
      ↓
Olist Sales Table Creation
      ↓
Data Quality Validation
      ↓
Cleaning & Date Conversion
      ↓
Business Feature Engineering
      ↓
KPI Computation
      ↓
CSV / Excel Export
      ↓
Automated Visualizations
      ↓
Markdown Executive Report
```

---

## Generated Outputs

When running the pipeline, the following files are generated:

```text
data/processed/sales_featured.csv

reports/pipeline.log
reports/validation_report.csv
reports/executive_dashboard.xlsx
reports/executive_report.md

reports/figures/monthly_revenue.png
reports/figures/revenue_by_category.png
```

---

## Business KPIs

The pipeline computes metrics such as:

- total revenue
- average order value
- total orders
- total customers
- average review score
- delayed order rate
- revenue by product category
- monthly revenue evolution

---

## Run the Project

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the pipeline:

```bash
python app.py
```

---

## Why This Project Matters

This project demonstrates how a reusable analytics framework can be applied to a real business dataset.

It shows skills in:

- data engineering
- business intelligence
- data quality
- KPI creation
- reporting automation
- reusable software architecture
- Git and GitHub workflow

---

## Next Improvements

- Add Power BI dashboard
- Add SQL analysis layer
- Add automated business recommendations
- Add tests for domain-specific Olist steps
- Add Docker support
- Add GitHub Actions CI
- Add Streamlit dashboard

---

## Related Repository

- [analytics-framework](https://github.com/TheKopps/analytics-framework)

---

## Author

Adrien Monteiro