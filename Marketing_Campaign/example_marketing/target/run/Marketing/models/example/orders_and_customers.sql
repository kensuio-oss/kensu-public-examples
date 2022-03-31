

  create  table "testme"."testme_schema"."orders_and_customers__dbt_tmp"
  as (
    

select *
from "testme"."public"."orders"
left join "testme"."public"."customers"
on customers.id = orders.customer_id
  );