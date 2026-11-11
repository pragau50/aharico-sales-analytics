
with city_rev AS (
    SELECT city, SUM(revenue) AS total_revenue
    FROM aharico_clean
    GROUP BY city
)
select * from city_rev WHERE total_revenue > 50000;

select city, sum(revenue) as total_revenue
from aharico_clean group by city HAVING sum(revenue) > 50000;



show tables;

with top_customers AS
(SELECT customer_name, segment, sum(revenue) as total_revenue, RANK() 
OVER (PARTITION BY segment ORDER BY sum(revenue) DESC) as rnk
FROM aharico_clean group BY customer_name,segment
)
select * from top_customers where rnk=1;

with city_rev AS (
    SELECT city, SUM(revenue) AS total_revenue
    FROM aharico_clean
    GROUP BY city
)
with product_rev AS (
    SELECT product, SUM(revenue) AS total_revenue
    FROM aharico_clean
    GROUP BY product
)
select * from city_rev WHERE total_revenue > 50000;
select * from product_rev WHERE total_revenue > 50000;