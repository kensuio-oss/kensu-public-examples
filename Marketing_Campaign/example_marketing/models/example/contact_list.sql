{{ config(materialized='table') }}


select first_name, phone
from {{ ref('orders_and_customers') }}