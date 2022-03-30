

select *
from "testme"."public"."orders"
left join "testme"."public"."customers"
on customers.id = orders.customer_id