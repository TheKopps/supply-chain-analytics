from pathlib import Path

from analytics_framework import Config, Pipeline, setup_logger
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

from src.domain.insights import GenerateOlistBusinessInsightsStep
from src.domain.olist_steps import (
    AddOlistBusinessFeaturesStep,
    CreateOlistSalesTableStep,
)

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

config = Config.from_yaml(CONFIG_PATH)

DATA_RAW = config.resolve_path("paths.raw_data", base_path=PROJECT_ROOT)

files = {
    dataset_name: DATA_RAW / file_name
    for dataset_name, file_name in config.get("raw_files").items()
}

logger = setup_logger(
    name="supply_chain_analytics",
    log_file=config.resolve_path("outputs.pipeline_log", base_path=PROJECT_ROOT),
)

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
    project_name=config.get("project.name"),
    logger=logger,
    stop_on_error=config.get("pipeline.stop_on_error", True),
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
    GenerateOlistBusinessInsightsStep(
        metrics_key="executive_metrics",
        category_metrics_key="category_metrics",
        quality_report_key="quality_report",
        output_key="business_recommendations",
    )
)

pipeline.add_step(
    CSVExportStep(
        input_key="sales_featured",
        output_path=config.resolve_path(
            "outputs.sales_featured",
            base_path=PROJECT_ROOT,
        ),
        output_key="sales_featured_export_path",
    )
)

pipeline.add_step(
    CSVExportStep(
        input_key="quality_report",
        output_path=config.resolve_path(
            "outputs.validation_report",
            base_path=PROJECT_ROOT,
        ),
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
        output_path=config.resolve_path(
            "outputs.executive_dashboard",
            base_path=PROJECT_ROOT,
        ),
    )
)

pipeline.add_step(
    LinePlotStep(
        input_key="monthly_revenue",
        x_column="order_purchase_timestamp",
        y_column="sum_total_order_value",
        output_path=config.resolve_path(
            "outputs.monthly_revenue_figure",
            base_path=PROJECT_ROOT,
        ),
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
        output_path=config.resolve_path(
            "outputs.revenue_by_category_figure",
            base_path=PROJECT_ROOT,
        ),
        title="Revenue by Product Category",
        xlabel="Category",
        ylabel="Revenue",
    )
)

pipeline.add_step(
    MarkdownReportStep(
        title="Supply Chain Analytics Executive Report",
        output_path=config.resolve_path(
            "outputs.executive_report",
            base_path=PROJECT_ROOT,
        ),
        context_keys=[
            "executive_metrics",
            "category_metrics",
            "quality_report",
            "business_recommendations",
        ],
    )
)


if __name__ == "__main__":
    pipeline.run()
