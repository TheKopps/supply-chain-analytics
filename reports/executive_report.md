# Supply Chain Analytics Executive Report

## Executive Metrics

| metric | column | operation | value |
| --- | --- | --- | --- |
| total_revenue | total_order_value | sum | 16643731.3 |
| average_order_value | total_order_value | mean | 140.67898994167865 |
| total_orders | order_id | nunique | 99441.0 |
| total_customers | customer_unique_id | nunique | 96096.0 |
| average_review_score | review_score | mean | 4.015582414978078 |
| delayed_orders_rate | is_delayed | mean | 0.06344476805183687 |

## Category Metrics

| product_category_name | total_order_value | order_id |
| --- | --- | --- |
| agro_industria_e_comercio | 90808.77 | 182 |
| alimentos | 37649.99 | 450 |
| alimentos_bebidas | 21230.81 | 227 |
| artes | 28912.99 | 202 |
| artes_e_artesanato | 2184.1400000000003 | 23 |
| artigos_de_festas | 5636.43 | 39 |
| artigos_de_natal | 12079.84 | 128 |
| audio | 58494.16 | 350 |
| automotivo | 714431.95 | 3897 |
| bebes | 506539.48 | 2885 |

_Showing 10 of 74 rows._

## Quality Report

| check_name | status | details | value |
| --- | --- | --- | --- |
| required_columns | PASS | All required columns are present. | ['order_id', 'customer_id', 'product_id', 'seller_id', 'price', 'freight_value', 'order_purchase_timestamp'] |
| duplicates | PASS | Duplicate row check completed. | 0 |
| missing_values | WARNING | Missing values check completed. | {'order_id': 0.0, 'customer_id': 0.0, 'order_status': 0.0, 'order_purchase_timestamp': 0.0, 'order_approved_at': 0.0015, 'order_delivered_carrier_date': 0.0175, 'order_delivered_customer_date': 0.0287, 'order_estimated_delivery_date': 0.0, 'customer_unique_id': 0.0, 'customer_zip_code_prefix': 0.0, 'customer_city': 0.0, 'customer_state': 0.0, 'order_item_id': 0.007, 'product_id': 0.007, 'seller_id': 0.007, 'shipping_limit_date': 0.007, 'price': 0.007, 'freight_value': 0.007, 'payment_sequential': 0.0, 'payment_type': 0.0, 'payment_installments': 0.0, 'payment_value': 0.0, 'product_category_name': 0.0213, 'product_name_lenght': 0.0213, 'product_description_lenght': 0.0213, 'product_photos_qty': 0.0213, 'product_weight_g': 0.0072, 'product_length_cm': 0.0072, 'product_height_cm': 0.0072, 'product_width_cm': 0.0072, 'seller_zip_code_prefix': 0.007, 'seller_city': 0.007, 'seller_state': 0.007, 'review_id': 0.0084, 'review_score': 0.0084, 'review_comment_title': 0.8826, 'review_comment_message': 0.5783, 'review_creation_date': 0.0084, 'review_answer_timestamp': 0.0084} |
| non_negative_values | PASS | Non-negative values check completed. | {'price': 0, 'freight_value': 0} |

## Business Recommendations

- Total revenue reached 16,643,731.30. Keep revenue monitoring as a key reporting priority.
- Average order value is 140.68. Marketing could focus on bundles and cross-selling.
- Delayed orders represent 6.34% of orders. Logistics performance should be monitored.
- Average review score is strong at 4.02/5. Delivery reliability should remain a priority.
- The top revenue category is 'beleza_saude' with 1,491,397.76 in revenue. This category should be prioritized.
- All data quality checks passed successfully. The generated analytics outputs are reliable.

