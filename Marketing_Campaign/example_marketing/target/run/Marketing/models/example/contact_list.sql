

  create  table "testme"."testme_schema"."contact_list__dbt_tmp"
  as (
    


select first_name, phone
from "testme"."testme_schema"."orders_and_customers"
  );