# Enterprise Retail Data & Governance Pipeline

An automated, production-grade Python & Docker retail data pipeline that ingests, validates, transforms, and visualizes over **1,000,000 transaction records** from raw retail data into executive data marts. 

Built with an emphasis on **data governance** and **observability**, this system isolates corrupted records using a Data Quarantine pattern before aggregating core financial metrics like Monthly Revenue Trends and Customer Lifetime Value (CLV).

---

## Pipeline Architecture

[ Data/online_retail_II.csv ]
    1. Ingest (`src/ingest.py`) 
    2. Validate (`src/validate.py`)
        Clean Records --- [ data/processed/clean_retail_data.csv ]
        Corrupted Records --- [ data/processed/quarantined_records.csv ] (Audit Log)
    3. Transform (`src/transform.py`)
        Customer Spend Mart (CLV & AOV)
        Monthly Revenue Mart
    4. Visualize (`src/plots.py`)
        Headless PNG Export --- [ reports/figures/ ]