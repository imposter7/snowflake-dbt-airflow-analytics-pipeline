{{ config(materialized='view') }}

WITH source AS (
    SELECT *
    FROM {{ source('raw', 'customers') }}
),

cleaned AS (
    SELECT
        CUSTOMER_ID AS customer_id,
        TRIM(CUSTOMER_NAME) AS customer_name,
        LOWER(TRIM(EMAIL)) AS email,
        TRIM(CITY) AS city,
        UPPER(TRIM(STATE)) AS state,
        SIGNUP_DATE AS signup_date
    FROM source
)

SELECT *
FROM cleaned
