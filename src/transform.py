import logging
import pandas as pd

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def calculate_customer_metrics(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Computes Customer-level metrics: Total Spend, Order Count, and Average Order Value (AOV)."""
    logging.info("Calculating Customer Metrics Data Mart...")

    df = clean_df.copy()
    df["TotalAmount"] = df["Quantity"] * df["Price"]

    customer_mart = (
        df.groupby("Customer ID")
        .agg(
            TotalSpend=("TotalAmount", "sum"),
            TotalOrders=("Invoice", "nunique"),
            TotalItemsPurchased=("Quantity", "sum"),
            FirstPurchaseDate=("InvoiceDate", "min"),
            LastPurchaseDate=("InvoiceDate", "max"),
        )
        .reset_index()
    )

    customer_mart["AOV"] = (
        customer_mart["TotalSpend"] / customer_mart["TotalOrders"]
    ).round(2)
    customer_mart["TotalSpend"] = customer_mart["TotalSpend"].round(2)

    logging.info(
        f"Customer Mart created successfully with {len(customer_mart):,} active customers."
    )
    return customer_mart


def calculate_monthly_revenue(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates revenue and order volume by year-month for executive reporting."""
    logging.info("Calculating Monthly Revenue Data Mart...")

    df = clean_df.copy()
    df["TotalAmount"] = df["Quantity"] * df["Price"]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

    monthly_mart = (
        df.groupby("YearMonth")
        .agg(
            MonthlyRevenue=("TotalAmount", "sum"),
            TotalOrders=("Invoice", "nunique"),
            UniqueCustomers=("Customer ID", "nunique"),
        )
        .reset_index()
    )

    monthly_mart["MonthlyRevenue"] = monthly_mart["MonthlyRevenue"].round(2)
    monthly_mart["YearMonth"] = monthly_mart["YearMonth"].astype(str)

    logging.info(f"Monthly Revenue Mart created across {len(monthly_mart)} months.")
    return monthly_mart


def run_transformations(
    clean_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Executes all transformation logic and returns summary data marts."""
    customer_mart = calculate_customer_metrics(clean_df)
    monthly_mart = calculate_monthly_revenue(clean_df)
    return customer_mart, monthly_mart


if __name__ == "__main__":
    print("Transformation module ready for pipeline execution.")