from pathlib import Path

from analytics_framework import Pipeline, setup_logger
from analytics_framework.analytics import (
    BasicMetricsStep,
    GroupByMetricsStep,
    TimeSeriesMetricsStep,
)
from analytics_framework.export import CSVExportStep, MultiSheetExcelExportStep
from analytics_framework.features import (
    ConvertDateColumnsStep,
    DropDuplicatesStep,
    FillMissingValuesStep,
)
from analytics_framework.ingestion import MultipleCSVLoaderStep
from analytics_framework.quality import DataQualityValidatorStep
from analytics_framework.reporting import MarkdownReportStep
from analytics_framework.visualization import BarPlotStep, LinePlotStep

from src.domain.olist_steps import (
    AddOlistBusinessFeaturesStep,
    CreateOlistSalesTableStep,
)

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_POWERBI = PROJECT_ROOT / "data" / "powerbi"
REPORTS = PROJECT_ROOT / "reports"
FIGURES = REPORTS / "figures"

logger = setup_logger(
    name="supply_chain_analytics",
    log_file=REPORTS / "pipeline.log",
)

files = {
    "customers": DATA_RAW / "olist_customers_dataset.csv",
    "orders": DATA_RAW / "olist_orders_dataset.csv",
    "order_items": DATA_RAW / "olist_order_items_dataset.csv",
    "payments": DATA_RAW / "olist_order_payments_dataset.csv",
    "products": DATA_RAW / "olist_products_dataset.csv",
    "sellers": DATA_RAW / "olist_sellers_dataset.csv",
    "reviews": DATA_RAW / "olist_order_reviews_dataset.csv",
}

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "shipping_limit_date",
    "review_creation_date",
    "review_answer_timestamp",
]


pipeline = Pipeline(
    project_name="Supply Chain Analytics",
    logger=logger,
)

pipeline.add_step(
    MultipleCSVLoaderStep(
        files=files,
        output_key="datasets",
    )
)

pipeline.add_step(
    CreateOlistSalesTableStep(
        input_key="datasets",
        output_key="sales",
    )
)

pipeline.add_step(
    DataQualityValidatorStep(
        input_key="sales",
        output_key="quality_report",
        required_columns=[
            "order_id",
            "customer_id",
            "product_id",
            "seller_id",
            "price",
            "freight_value",
            "order_purchase_timestamp",
        ],
        non_negative_columns=[
            "price",
            "freight_value",
        ],
        fail_on_error=True,
    )
)

pipeline.add_step(
    DropDuplicatesStep(
        input_key="sales",
        output_key="sales_clean",
    )
)

pipeline.add_step(
    FillMissingValuesStep(
        input_key="sales_clean",
        output_key="sales_clean",
        fill_values={
            "product_category_name": "unknown",
        },
    )
)

pipeline.add_step(
    ConvertDateColumnsStep(
        input_key="sales_clean",
        output_key="sales_clean",
        columns=date_columns,
    )
)

pipeline.add_step(
    AddOlistBusinessFeaturesStep(
        input_key="sales_clean",
        output_key="sales_featured",
    )
)

pipeline.add_step(
    BasicMetricsStep(
        input_key="sales_featured",
        output_key="executive_metrics",
        metrics={
            "total_revenue": {
                "column": "total_order_value",
                "operation": "sum",
            },
            "average_order_value": {
                "column": "total_order_value",
                "operation": "mean",
            },
            "total_orders": {
                "column": "order_id",
                "operation": "nunique",
            },
            "total_customers": {
                "column": "customer_unique_id",
                "operation": "nunique",
            },
            "average_review_score": {
                "column": "review_score",
                "operation": "mean",
            },
            "delayed_orders_rate": {
                "column": "is_delayed",
                "operation": "mean",
            },
        },
    )
)

pipeline.add_step(
    GroupByMetricsStep(
        input_key="sales_featured",
        output_key="category_metrics",
        groupby_columns=["product_category_name"],
        aggregations={
            "total_order_value": "sum",
            "order_id": "nunique",
        },
    )
)

pipeline.add_step(
    TimeSeriesMetricsStep(
        input_key="sales_featured",
        output_key="monthly_revenue",
        date_column="order_purchase_timestamp",
        value_column="total_order_value",
        frequency="M",
        operation="sum",
    )
)

pipeline.add_step(
    CSVExportStep(
        input_key="sales_featured",
        output_path=DATA_PROCESSED / "sales_featured.csv",
        output_key="sales_featured_export_path",
    )
)

pipeline.add_step(
    CSVExportStep(
        input_key="quality_report",
        output_path=REPORTS / "validation_report.csv",
        output_key="quality_report_export_path",
    )
)

pipeline.add_step(
    MultiSheetExcelExportStep(
        input_keys={
            "Executive KPIs": "executive_metrics",
            "Categories": "category_metrics",
            "Monthly Revenue": "monthly_revenue",
            "Quality Report": "quality_report",
        },
        output_path=REPORTS / "executive_dashboard.xlsx",
    )
)

pipeline.add_step(
    LinePlotStep(
        input_key="monthly_revenue",
        x_column="order_purchase_timestamp",
        y_column="sum_total_order_value",
        output_path=FIGURES / "monthly_revenue.png",
        title="Monthly Revenue Evolution",
        xlabel="Month",
        ylabel="Revenue",
    )
)

pipeline.add_step(
    BarPlotStep(
        input_key="category_metrics",
        x_column="product_category_name",
        y_column="total_order_value",
        output_path=FIGURES / "revenue_by_category.png",
        title="Revenue by Product Category",
        xlabel="Category",
        ylabel="Revenue",
    )
)

pipeline.add_step(
    MarkdownReportStep(
        title="Supply Chain Analytics Executive Report",
        output_path=REPORTS / "executive_report.md",
        context_keys=[
            "executive_metrics",
            "category_metrics",
            "quality_report",
        ],
    )
)


if __name__ == "__main__":
    pipeline.run()
