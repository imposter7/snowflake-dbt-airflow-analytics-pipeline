{{ config(materialized='view') }}

WITH source AS (
    SELECT *
    FROM {{ source('raw', 'order_items') }}
)

SELECT
    ORDER_ITEM_ID AS order_item_id,
    ORDER_ID AS order_id,
    PRODUCT_ID AS product_id,
    QUANTITY AS quantity,
    UNIT_PRICE AS unit_price,
    QUANTITY * UNIT_PRICE AS line_total
FROM source
