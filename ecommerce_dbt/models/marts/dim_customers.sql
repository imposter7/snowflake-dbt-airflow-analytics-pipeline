
{{ config(materialized='table', schema='MARTS') }}

SELECT
    customer_id,
    customer_name,
    email,
    city,
    state,
    signup_date
FROM {{ ref('stg_customers') }}

