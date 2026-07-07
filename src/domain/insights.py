from typing import Any

import pandas as pd
from analytics_framework import PipelineStep


def _get_metric_value(
    metrics: pd.DataFrame | dict[str, Any],
    metric_name: str,
) -> Any:
    if isinstance(metrics, dict):
        return metrics.get(metric_name)

    if isinstance(metrics, pd.DataFrame):
        if {"metric", "value"}.issubset(metrics.columns):
            matching_rows = metrics.loc[
                metrics["metric"] == metric_name,
                "value",
            ]

            if not matching_rows.empty:
                return matching_rows.iloc[0]

        if metric_name in metrics.columns:
            return metrics[metric_name].iloc[0]

    return None


class GenerateOlistBusinessInsightsStep(PipelineStep):
    """
    Domain-specific step used to generate business insights and recommendations
    for the Olist supply chain analytics project.
    """

    def __init__(
        self,
        metrics_key: str = "executive_metrics",
        category_metrics_key: str = "category_metrics",
        quality_report_key: str = "quality_report",
        output_key: str = "business_recommendations",
    ):
        super().__init__("Generate Olist Business Insights")
        self.metrics_key = metrics_key
        self.category_metrics_key = category_metrics_key
        self.quality_report_key = quality_report_key
        self.output_key = output_key

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        metrics = context[self.metrics_key]
        category_metrics = context[self.category_metrics_key]
        quality_report = context[self.quality_report_key]

        recommendations = []

        total_revenue = _get_metric_value(metrics, "total_revenue")
        average_order_value = _get_metric_value(metrics, "average_order_value")
        average_review_score = _get_metric_value(metrics, "average_review_score")
        delayed_orders_rate = _get_metric_value(metrics, "delayed_orders_rate")

        if total_revenue is not None:
            recommendations.append(
                f"Total revenue reached {total_revenue:,.2f}. "
                "Keep revenue monitoring as a key reporting priority."
            )

        if average_order_value is not None:
            recommendations.append(
                f"Average order value is {average_order_value:,.2f}. "
                "Marketing could focus on bundles and cross-selling."
            )

        if delayed_orders_rate is not None:
            delayed_rate_percentage = delayed_orders_rate * 100

            if delayed_rate_percentage > 5:
                recommendations.append(
                    f"Delayed orders represent {delayed_rate_percentage:.2f}% "
                    "of orders. Logistics performance should be monitored."
                )
            else:
                recommendations.append(
                    f"Delayed orders are controlled at {delayed_rate_percentage:.2f}%."
                )

        if average_review_score is not None:
            if average_review_score < 4:
                recommendations.append(
                    f"Average review score is {average_review_score:.2f}/5. "
                    "Customer satisfaction should be investigated."
                )
            else:
                recommendations.append(
                    f"Average review score is strong at "
                    f"{average_review_score:.2f}/5. "
                    "Delivery reliability should remain a priority."
                )

        if isinstance(category_metrics, pd.DataFrame) and not category_metrics.empty:
            if "total_order_value" in category_metrics.columns:
                top_category = category_metrics.sort_values(
                    "total_order_value",
                    ascending=False,
                ).iloc[0]

                category_name = top_category["product_category_name"]
                category_revenue = top_category["total_order_value"]

                recommendations.append(
                    f"The top revenue category is '{category_name}' "
                    f"with {category_revenue:,.2f} in revenue. "
                    "This category should be prioritized."
                )

        if isinstance(quality_report, pd.DataFrame) and not quality_report.empty:
            failed_checks = quality_report[
                quality_report["status"].astype(str).str.lower() == "fail"
            ]

            if not failed_checks.empty:
                recommendations.append(
                    f"{len(failed_checks)} data quality checks failed. "
                    "These issues should be reviewed before decision-making."
                )
            else:
                recommendations.append(
                    "All data quality checks passed successfully. "
                    "The generated analytics outputs are reliable."
                )

        context[self.output_key] = recommendations

        return context
