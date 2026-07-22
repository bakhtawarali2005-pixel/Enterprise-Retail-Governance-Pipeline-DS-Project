import logging
from pathlib import Path
from src.ingest import load_raw_data
from src.plots import generate_all_plots
from src.transform import run_transformations
from src.validate import validate_and_clean_data

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_pipeline() -> None:
    """Orchestrates the end-to-end data pipeline sequentially."""
    logging.info("Starting Enterprise Retail Pipeline Execution")

    try:
        raw_df = load_raw_data()
        clean_df, quarantined_df = validate_and_clean_data(raw_df)

        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)

        clean_df.to_csv(output_dir / "clean_retail_data.csv", index=False)
        quarantined_df.to_csv(output_dir / "quarantined_records.csv", index=False)
        logging.info("Exported clean_retail_data.csv and quarantined_records.csv")

        customer_mart, monthly_mart = run_transformations(clean_df)
        generate_all_plots(monthly_mart, customer_mart)

        print("[SUCCESS] Pipeline completed successfully!")

    except Exception as e:
        logging.critical(f"Pipeline execution failed: {e}")
        print(f"[ERROR] Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()