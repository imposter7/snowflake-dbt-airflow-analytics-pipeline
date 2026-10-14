{{ config(materialized='view') }}

WITH source AS (
    SELECT *
    FROM {{ source('raw', 'orders') }}
)

SELECT
    ORDER_ID AS order_id,
    CUSTOMER_ID AS customer_id,
    ORDER_DATE AS order_date,
    LOWER(TRIM(ORDER_STATUS)) AS order_status
FROM source
