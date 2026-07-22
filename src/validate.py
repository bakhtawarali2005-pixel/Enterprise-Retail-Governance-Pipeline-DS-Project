import logging
import pandas as pd

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def validate_and_clean_data(
    raw_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cleans raw retail data and isolates bad records into a quarantine DataFrame."""
    logging.info("Starting data validation checks...")

    missing_customer = raw_df["Customer ID"].isna()
    invalid_quantity = raw_df["Quantity"] <= 0
    invalid_price = raw_df["Price"] <= 0

    quarantine_mask = missing_customer | invalid_quantity | invalid_price

    clean_df = raw_df[~quarantine_mask].copy()
    quarantined_df = raw_df[quarantine_mask].copy()

    logging.info(f"Valid records: {len(clean_df):,} | Quarantined: {len(quarantined_df):,}")
    return clean_df, quarantined_df