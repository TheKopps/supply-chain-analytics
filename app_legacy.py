import time

from src.analytics.metrics_engine import compute_all_metrics
from src.export.powerbi import export_powerbi_tables
from src.features.feature_engineering import add_features
from src.ingestion.data_loader import create_sales_table, load_raw_datasets
from src.insights.recommendations import export_business_insights
from src.quality.cleaning import clean_sales_data
from src.quality.validation import validate_sales_data
from src.utils.logger import setup_logger
from src.visualization.plots import generate_all_figures

from config import (
    DATA_POWERBI,
    DATA_PROCESSED,
    DATA_RAW,
    FIGURES_PATH,
    INSIGHTS_PATH,
    SALES_ANALYTICS_PATH,
    SALES_CLEAN_PATH,
    SALES_FEATURED_PATH,
)


def main():
    start_time = time.time()
    logger = setup_logger()

    logger.info("=" * 60)
    logger.info("SUPPLY CHAIN ANALYTICS PLATFORM")
    logger.info("=" * 60)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    DATA_POWERBI.mkdir(parents=True, exist_ok=True)

    logger.info("1. Loading raw datasets...")
    datasets = load_raw_datasets(DATA_RAW)
    logger.info("Raw datasets loaded successfully.")

    logger.info("2. Creating analytical sales table...")
    sales = create_sales_table(datasets)
    sales.to_csv(SALES_ANALYTICS_PATH, index=False)
    logger.info(f"Saved analytical table: {SALES_ANALYTICS_PATH}")

    logger.info("2.1 Validating raw analytical table...")
    validation_report = validate_sales_data(sales)
    validation_report.to_csv(DATA_PROCESSED / "validation_report.csv", index=False)
    logger.info("Validation report saved.")

    logger.info("3. Cleaning data...")
    sales_clean = clean_sales_data(sales)
    sales_clean.to_csv(SALES_CLEAN_PATH, index=False)
    logger.info(f"Saved clean table: {SALES_CLEAN_PATH}")

    logger.info("4. Adding business features...")
    sales_featured = add_features(sales_clean)
    sales_featured.to_csv(SALES_FEATURED_PATH, index=False)
    logger.info(f"Saved featured table: {SALES_FEATURED_PATH}")

    logger.info("5. Computing KPIs...")
    kpis = compute_all_metrics(sales_featured)
    kpis.to_csv(DATA_PROCESSED / "kpi_summary.csv", index=False)
    logger.info("KPI summary saved.")

    logger.info("6. Exporting Power BI tables...")
    export_powerbi_tables(sales_featured, DATA_POWERBI)
    logger.info("Power BI tables exported successfully.")

    logger.info("7. Generating automatic figures...")
    generate_all_figures(sales_featured, FIGURES_PATH)
    logger.info(f"Figures saved in: {FIGURES_PATH}")

    logger.info("8. Generating business insights...")
    export_business_insights(sales_featured, INSIGHTS_PATH)
    logger.info(f"Business insights saved in: {INSIGHTS_PATH}")

    elapsed_time = round(time.time() - start_time, 2)
    logger.info(f"Pipeline completed successfully in {elapsed_time} seconds.")


if __name__ == "__main__":
    main()
