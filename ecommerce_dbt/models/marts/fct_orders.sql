
{{ config(materialized='table', schema='MARTS') }}

WITH order_totals AS (
    SELECT
        order_id,
        SUM(quantity * unit_price) AS total_amount,
        SUM(quantity) AS total_items
    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status AS order_status,
    COALESCE(t.total_items, 0) AS total_items,
    COALESCE(t.total_amount, 0) AS total_amount
FROM {{ ref('stg_orders') }} o
LEFT JOIN order_totals t
    ON o.order_id = t.order_id

