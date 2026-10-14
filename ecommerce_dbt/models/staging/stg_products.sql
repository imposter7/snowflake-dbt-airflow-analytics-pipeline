{{ config(materialized='view') }}

WITH source AS (
    SELECT *
    FROM {{ source('raw', 'products') }}
)

SELECT
    PRODUCT_ID AS product_id,
    TRIM(PRODUCT_NAME) AS product_name,
    TRIM(CATEGORY) AS category,
    UNIT_PRICE AS unit_price
FROM source
