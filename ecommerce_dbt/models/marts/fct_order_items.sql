
{{ config(materialized='table', schema='MARTS') }}

SELECT
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS line_total
FROM {{ ref('stg_order_items') }} oi
INNER JOIN {{ ref('stg_orders') }} o
    ON oi.order_id = o.order_id

