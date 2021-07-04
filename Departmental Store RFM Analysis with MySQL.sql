use brazilian_ecommerce;
-- the datasets from kaggle for a departmental store in Brazil
-- create a customer_rfm view for scores working later
-- the analysis will based on three criterias:
-- # Recency - the most recent the purchase, the more responsive the customer is to promotions
-- # Frequency - the more frequently the customer buys, the more engaged and satisfied they are
-- # Monetary - monetary value differentiates heavy spenders from low-value purchasers

create view customer_rfm as (
select 
	od.customer_id, 
	od.order_id, 
    -- calculate the recency in days from the lastest  transaction date
    datediff((select max(order_purchase_timestamp) from olist_orders_dataset), order_purchase_timestamp) recency,
    o1.frequency,
    o1.monetary
from olist_orders_dataset od
join 
-- join with frequency and mometary table created from sub query
(select order_id, 
		count(*) frequency, 
		sum(price) monetary
		from olist_order_items_dataset
		group by order_id) o1 
on od.order_id = o1.order_id
-- look into orders which have been delivered and invoiced only
where order_status in ('delivered', 'invoiced')
order by recency 
);

-- using customer_rfm view to calculate the scores for each customer
-- rfm scores rank from low to high (from 1 point to 4 points)

select customer_id, 
	   recency_score*100 + frequency_score*10 + monetary_score as rfm_score,
       (recency_score + frequency_score + monetary_score)/3 as rfm_average
from (
	select customer_id, recency, frequency, monetary,
		ntile(4) over (order by recency desc) recency_score,
		ntile(4) over (order by frequency) frequency_score, 
		ntile(4) over (order by monetary) monetary_score
	from customer_rfm) rfm
    order by rfm_score desc;
    
    

    










