

  create  table "testme"."testme_schema"."email_list__dbt_tmp"
  as (
    

-- FIXME: support views
-- Use the `ref` function to select from other models

select email
from "testme"."testme_schema"."orders_and_customers"
  );