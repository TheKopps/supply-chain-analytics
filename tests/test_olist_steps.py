import pandas as pd

from src.domain.olist_steps import (
    AddOlistBusinessFeaturesStep,
    CreateOlistSalesTableStep,
)


def make_sample_olist_datasets():
    customers = pd.DataFrame(
        {
            "customer_id": ["customer_1"],
            "customer_unique_id": ["unique_customer_1"],
            "customer_city": ["sao paulo"],
            "customer_state": ["SP"],
        }
    )

    orders = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "customer_id": ["customer_1"],
            "order_purchase_timestamp": ["2018-01-01 10:00:00"],
            "order_approved_at": ["2018-01-01 11:00:00"],
            "order_delivered_carrier_date": ["2018-01-02 10:00:00"],
            "order_delivered_customer_date": ["2018-01-05 10:00:00"],
            "order_estimated_delivery_date": ["2018-01-07 10:00:00"],
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "product_id": ["product_1"],
            "seller_id": ["seller_1"],
            "shipping_limit_date": ["2018-01-03 10:00:00"],
            "price": [100.0],
            "freight_value": [20.0],
        }
    )

    payments = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "payment_value": [120.0],
            "payment_type": ["credit_card"],
        }
    )

    products = pd.DataFrame(
        {
            "product_id": ["product_1"],
            "product_category_name": ["electronics"],
        }
    )

    sellers = pd.DataFrame(
        {
            "seller_id": ["seller_1"],
            "seller_city": ["rio de janeiro"],
            "seller_state": ["RJ"],
        }
    )

    reviews = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "review_score": [5],
        }
    )

    return {
        "customers": customers,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
        "products": products,
        "sellers": sellers,
        "reviews": reviews,
    }


def make_sample_sales_dataframe():
    sales = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "customer_id": ["customer_1"],
            "customer_unique_id": ["unique_customer_1"],
            "product_id": ["product_1"],
            "seller_id": ["seller_1"],
            "price": [100.0],
            "freight_value": [20.0],
            "review_score": [5],
            "order_purchase_timestamp": ["2018-01-01 10:00:00"],
            "order_approved_at": ["2018-01-01 11:00:00"],
            "order_delivered_carrier_date": ["2018-01-02 10:00:00"],
            "order_delivered_customer_date": ["2018-01-05 10:00:00"],
            "order_estimated_delivery_date": ["2018-01-07 10:00:00"],
        }
    )

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        sales[column] = pd.to_datetime(sales[column])

    return sales


def test_create_olist_sales_table_step_creates_consolidated_table():
    datasets = make_sample_olist_datasets()

    step = CreateOlistSalesTableStep(
        input_key="datasets",
        output_key="sales",
    )

    context = {"datasets": datasets}

    result = step.execute(context)

    assert "sales" in result

    sales = result["sales"]

    assert sales.shape[0] == 1
    assert "order_id" in sales.columns
    assert "customer_unique_id" in sales.columns
    assert "product_category_name" in sales.columns
    assert "seller_state" in sales.columns
    assert "review_score" in sales.columns

    assert sales["order_id"].iloc[0] == "order_1"
    assert sales["customer_unique_id"].iloc[0] == "unique_customer_1"
    assert sales["product_category_name"].iloc[0] == "electronics"


def test_add_olist_business_features_step_adds_expected_columns():
    sales = make_sample_sales_dataframe()

    step = AddOlistBusinessFeaturesStep(
        input_key="sales",
        output_key="sales_featured",
    )

    context = {"sales": sales}

    result = step.execute(context)

    assert "sales_featured" in result

    sales_featured = result["sales_featured"]

    expected_columns = [
        "purchase_year",
        "purchase_month",
        "purchase_quarter",
        "purchase_day",
        "purchase_weekday",
        "purchase_hour",
        "delivery_time_days",
        "delivery_delay_days",
        "approval_time_hours",
        "shipping_time_days",
        "total_order_value",
        "freight_ratio",
        "is_delayed",
        "review_label",
    ]

    for column in expected_columns:
        assert column in sales_featured.columns


def test_add_olist_business_features_step_computes_correct_values():
    sales = make_sample_sales_dataframe()

    step = AddOlistBusinessFeaturesStep(
        input_key="sales",
        output_key="sales_featured",
    )

    result = step.execute({"sales": sales})

    sales_featured = result["sales_featured"]

    assert sales_featured["purchase_year"].iloc[0] == 2018
    assert sales_featured["purchase_month"].iloc[0] == 1
    assert sales_featured["purchase_hour"].iloc[0] == 10

    assert sales_featured["delivery_time_days"].iloc[0] == 4
    assert sales_featured["delivery_delay_days"].iloc[0] == -2
    assert sales_featured["approval_time_hours"].iloc[0] == 1.0
    assert sales_featured["total_order_value"].iloc[0] == 120.0
    assert sales_featured["freight_ratio"].iloc[0] == 20.0 / 120.0
    assert sales_featured["is_delayed"].iloc[0] == 0
    assert sales_featured["review_label"].iloc[0] == "Satisfied"
