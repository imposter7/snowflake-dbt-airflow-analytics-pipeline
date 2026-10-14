
{{ config(materialized='table', schema='MARTS') }}

SELECT
    product_id,
    product_name,
    category,
    unit_price
FROM {{ ref('stg_products') }}

