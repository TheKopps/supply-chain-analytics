from typing import Any

import pandas as pd
from analytics_framework import PipelineStep


class BuildPowerBITablesStep(PipelineStep):
    """
    Domain-specific step used to build Power BI-ready tables
    from the featured Olist sales dataset.
    """

    def __init__(
        self,
        input_key: str = "sales_featured",
        fact_key: str = "fact_sales",
        customers_key: str = "dim_customers",
        products_key: str = "dim_products",
        sellers_key: str = "dim_sellers",
        dates_key: str = "dim_dates",
    ):
        super().__init__("Build Power BI Tables")
        self.input_key = input_key
        self.fact_key = fact_key
        self.customers_key = customers_key
        self.products_key = products_key
        self.sellers_key = sellers_key
        self.dates_key = dates_key

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        sales = context[self.input_key].copy()

        sales["purchase_date"] = sales["order_purchase_timestamp"].dt.date
        sales["date_key"] = (
            sales["order_purchase_timestamp"].dt.strftime("%Y%m%d").astype(int)
        )

        fact_columns = [
            "order_id",
            "customer_unique_id",
            "product_id",
            "seller_id",
            "date_key",
            "price",
            "freight_value",
            "total_order_value",
            "delivery_time_days",
            "delivery_delay_days",
            "is_delayed",
            "review_score",
            "review_label",
        ]

        fact_sales = sales[fact_columns].copy()

        dim_customers = (
            sales[
                [
                    "customer_unique_id",
                    "customer_city",
                    "customer_state",
                ]
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        dim_products = (
            sales[
                [
                    "product_id",
                    "product_category_name",
                ]
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        dim_sellers = (
            sales[
                [
                    "seller_id",
                    "seller_city",
                    "seller_state",
                ]
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        dim_dates = self._build_date_dimension(sales)

        context[self.fact_key] = fact_sales
        context[self.customers_key] = dim_customers
        context[self.products_key] = dim_products
        context[self.sellers_key] = dim_sellers
        context[self.dates_key] = dim_dates

        return context

    def _build_date_dimension(self, sales: pd.DataFrame) -> pd.DataFrame:
        min_date = sales["order_purchase_timestamp"].min().date()
        max_date = sales["order_purchase_timestamp"].max().date()

        dates = pd.date_range(start=min_date, end=max_date, freq="D")

        dim_dates = pd.DataFrame(
            {
                "date": dates,
            }
        )

        dim_dates["date_key"] = dim_dates["date"].dt.strftime("%Y%m%d").astype(int)
        dim_dates["year"] = dim_dates["date"].dt.year
        dim_dates["month"] = dim_dates["date"].dt.month
        dim_dates["month_name"] = dim_dates["date"].dt.month_name()
        dim_dates["quarter"] = dim_dates["date"].dt.quarter
        dim_dates["day"] = dim_dates["date"].dt.day
        dim_dates["weekday"] = dim_dates["date"].dt.weekday
        dim_dates["weekday_name"] = dim_dates["date"].dt.day_name()

        return dim_dates
