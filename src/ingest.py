import logging
from pathlib import Path
import pandas as pd

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def load_raw_data(relative_path: str = "Data/online_retail_II.csv") -> pd.DataFrame:
    """Ingests raw CSV data safely into a pandas DataFrame."""
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / relative_path

    try:
        logging.info(f"Starting ingestion from: {file_path}")
        df = pd.read_csv(file_path)
        logging.info(f"Successfully ingested {len(df):,} records.")
        return df
    except FileNotFoundError:
        logging.error(f"Ingestion failed: File not found at {file_path}")
        raise FileNotFoundError(f"Ensure raw CSV exists at {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error during ingestion: {e}")
        raise


if __name__ == "__main__":
    raw_df = load_raw_data()
    print(f"Data ingested successfully. Shape: {raw_df.shape}")