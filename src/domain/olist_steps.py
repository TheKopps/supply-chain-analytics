from typing import Any

from analytics_framework import PipelineStep


class CreateOlistSalesTableStep(PipelineStep):
    """
    Domain-specific step used to create the consolidated Olist sales table.
    """

    def __init__(
        self,
        input_key: str = "datasets",
        output_key: str = "sales",
    ):
        super().__init__("Create Olist Sales Table")
        self.input_key = input_key
        self.output_key = output_key

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        datasets = context[self.input_key]

        sales = datasets["orders"].copy()

        sales = sales.merge(datasets["customers"], on="customer_id", how="left")
        sales = sales.merge(datasets["order_items"], on="order_id", how="left")
        sales = sales.merge(datasets["payments"], on="order_id", how="left")
        sales = sales.merge(datasets["products"], on="product_id", how="left")

        sales = sales.merge(
            datasets["sellers"],
            on="seller_id",
            how="left",
            suffixes=("", "_seller"),
        )

        sales = sales.merge(datasets["reviews"], on="order_id", how="left")

        context[self.output_key] = sales

        return context


class AddOlistBusinessFeaturesStep(PipelineStep):
    """
    Domain-specific step used to add business features for the Olist project.
    """

    def __init__(
        self,
        input_key: str = "sales",
        output_key: str = "sales_featured",
    ):
        super().__init__("Add Olist Business Features")
        self.input_key = input_key
        self.output_key = output_key

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        sales = context[self.input_key].copy()

        sales["purchase_year"] = sales["order_purchase_timestamp"].dt.year
        sales["purchase_month"] = sales["order_purchase_timestamp"].dt.month
        sales["purchase_quarter"] = sales["order_purchase_timestamp"].dt.quarter
        sales["purchase_day"] = sales["order_purchase_timestamp"].dt.day
        sales["purchase_weekday"] = sales["order_purchase_timestamp"].dt.day_name()
        sales["purchase_hour"] = sales["order_purchase_timestamp"].dt.hour

        sales["delivery_time_days"] = (
            sales["order_delivered_customer_date"] - sales["order_purchase_timestamp"]
        ).dt.days

        sales["delivery_delay_days"] = (
            sales["order_delivered_customer_date"]
            - sales["order_estimated_delivery_date"]
        ).dt.days

        sales["approval_time_hours"] = (
            sales["order_approved_at"] - sales["order_purchase_timestamp"]
        ).dt.total_seconds() / 3600

        sales["shipping_time_days"] = (
            sales["order_delivered_carrier_date"] - sales["order_approved_at"]
        ).dt.days

        sales["total_order_value"] = sales["price"] + sales["freight_value"]
        sales["freight_ratio"] = sales["freight_value"] / sales["total_order_value"]
        sales["is_delayed"] = (sales["delivery_delay_days"] > 0).astype(int)

        sales["review_label"] = sales["review_score"].apply(
            lambda score: "Satisfied" if score >= 4 else "Unsatisfied"
        )

        context[self.output_key] = sales

        return context
