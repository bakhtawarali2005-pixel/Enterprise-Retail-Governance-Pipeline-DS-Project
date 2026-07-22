import logging
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

sns.set_theme(style="whitegrid")


def get_figures_dir() -> Path:
    """Resolves and creates the reports/figures directory dynamically."""
    project_root = Path(__file__).resolve().parent.parent
    figures_dir = project_root / "reports" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    return figures_dir


def plot_monthly_revenue(monthly_mart: pd.DataFrame) -> None:
    """Generates and saves a Monthly Revenue trend line chart 📈."""
    logging.info("Generating Monthly Revenue Trend plot...")

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        data=monthly_mart,
        x="YearMonth",
        y="MonthlyRevenue",
        marker="o",
        color="#1f77b4",
        linewidth=2.5,
        ax=ax,
    )

    ax.set_title(
        "Executive Dashboard: Monthly Revenue Growth Trend",
        fontsize=14,
        pad=15,
        weight="bold",
    )
    ax.set_xlabel("Year-Month", fontsize=11)
    ax.set_ylabel("Total Revenue (£)", fontsize=11)
    plt.xticks(rotation=45)

    ax.yaxis.set_major_formatter("{x:,.0f}")

    plt.tight_layout()

    output_path = get_figures_dir() / "monthly_revenue_trend.png"
    plt.savefig(output_path, dpi=300)
    plt.close(fig) 

    logging.info(f"Saved monthly revenue chart to {output_path}")


def plot_top_customers(
    customer_mart: pd.DataFrame, top_n: int = 10
) -> None:
    """Generates and saves a Top N Customers by Spend bar chart 🏆."""
    logging.info(f"Generating Top {top_n} Customer Spend plot...")

    top_customers = customer_mart.nlargest(top_n, "TotalSpend")

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=top_customers,
        x="TotalSpend",
        y="Customer ID",
        orient="h",
        palette="Blues_r",
        order=top_customers.sort_values("TotalSpend", ascending=False)[
            "Customer ID"
        ],
        ax=ax,
    )

    ax.set_title(
        f"Top {top_n} Customers by Total Spend (CLV)",
        fontsize=14,
        pad=15,
        weight="bold",
    )
    ax.set_xlabel("Total Spend (£)", fontsize=11)
    ax.set_ylabel("Customer ID", fontsize=11)

    ax.xaxis.set_major_formatter("{x:,.0f}")

    plt.tight_layout()

    output_path = get_figures_dir() / f"top_{top_n}_customers.png"
    plt.savefig(output_path, dpi=300)
    plt.close(fig)

    logging.info(f"Saved top customers chart to {output_path}")


def generate_all_plots(
    monthly_mart: pd.DataFrame, customer_mart: pd.DataFrame
) -> None:
    """Orchestrates the creation of all report visualizations."""
    plot_monthly_revenue(monthly_mart)
    plot_top_customers(customer_mart)


if __name__ == "__main__":
    print("Plotting module ready for pipeline execution.")