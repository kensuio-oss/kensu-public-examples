{{ config(materialized='table') }}

select *
from {{ source('raw_postgres_data', 'orders') }}
left join {{ source('raw_postgres_data', 'customers') }}
on customers.id = orders.customer_id