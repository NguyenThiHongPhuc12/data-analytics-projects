-- Customers
CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  name VARCHAR(50),
  signup_date DATE
);

-- Orders
CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  customer_id INT,
  order_date DATE,
  amount DECIMAL(10,2),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Products
CREATE TABLE products (
  product_id INT PRIMARY KEY,
  category VARCHAR(50),
  product_name VARCHAR(50),
  price DECIMAL(10,2)
);

-- Order Items
CREATE TABLE order_items (
  order_id INT,
  product_id INT,
  qty INT,
  price DECIMAL(10,2),
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Sample data
INSERT INTO customers VALUES
(1,'Alice','2024-01-15'),(2,'Bob','2024-02-10'),(3,'Cindy','2024-02-20'),
(4,'Dan','2024-03-01'),(5,'Emma','2024-03-05');

INSERT INTO orders VALUES
(101,1,'2024-03-10',120.00),(102,1,'2024-04-05',200.00),
(103,2,'2024-03-15',80.00),(104,2,'2024-05-01',50.00),
(105,3,'2024-03-20',300.00),(106,4,'2024-04-02',60.00);

INSERT INTO products VALUES
(11,'Electronics','Earbuds',40.00),(12,'Electronics','Keyboard',60.00),
(13,'Home','Kettle',30.00),(14,'Home','Vacuum',150.00),
(15,'Books','Novel',12.00);

INSERT INTO order_items VALUES
(101,11,2,40.00),(101,13,1,30.00),
(102,14,1,150.00),(102,15,2,12.00),
(103,12,1,60.00),
(104,15,4,12.00),
(105,14,2,150.00),
(106,13,2,30.00);

----LIVE CODING 
--- ĐỀ 1: Tính Doanh Thu Theo Tháng Và % Tăng Trưởng So Với Tháng Trước 
---------Bước 1: Gom nhóm orders theo tháng, tính tổng revenue mỗi tháng
---------Bước 2: Dùng LAG() lấy revenue tháng trước, tính % tăng trưởng
with monthly as 
(
  select 
     DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1) as month_start -- chuẩn hóa về ngày 1 của tháng
     ,sum(amount) as revenue                                             
  from orders
  group by DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1)
)
select
   month_start
   , revenue
   , ROUND(100.0 * (revenue - LAG(revenue) over (order by month_start)) / NULLIF(LAG(revenue) over (order by month_start), 0), 2) as month_growth_pct -- tính chênh lệch so vơí tháng trước / chia revenu tháng trước (nullif: tránh lỗi chia cho 0)

from monthly;
----=> kết quả của month_growth_pct (âm: revenue giảm) (dương: revenue tăng)

---ĐỀ 2: Tìm Sản Phẩm Có Doanh Thu Cao Nhất Trong Mỗi Danh Mục (Category) 
---------Bước 1: JOIN order_items với products, tính revenue (qty*price) mối sản phẩm the category
---------Bước 2: Dùng row_number() partition by category đã xếp hạng trong từng category
---------Bước 3: Lọc rank = 1 => lấy sản phẩm doanh thu cao nhất mỗi category 
with product_re as (
  select 
    p.category
    , p.product_id
    , p.product_name
    , SUM(oi.qty * oi.price) as revenue --- revenue = qty* price
from order_items oi 
join products p on oi.product_id = p.product_id
group by p.category, p.product_id, p.product_name
),
ranked as (
  select *
      , ROUND(ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue), 2) as rank --- xếp hạng giảm dần tbeo revenue
  from product_re
)
select 
  category
  , product_name
  , revenue
from ranked
where rank = 1; --- chỉ lấy top 1 category

---ĐỀ 3: Tỷ Lệ Khách Hàng Quay Lại, Khách Hàng Có >= 2 Đơn Hàng.
---------Bước 1: Đếm số đơn hàng của mỗi khách hàng
---------Bước 2: Tính % khách có từ 2 đơn trở lên / tổng số khách
with order_cnt as (
  select 
   customer_id
   , COUNT(*) as cnt --- tổng số đơn hàng mỗi khách
from orders 
group by customer_id
)
select 
   ROUND(100.0 *SUM(CASE WHEN cnt >= 2 THEN 1 ELSE 0 END) / COUNT(*), 2) as repeat_rate_pct -- đếm khách hàng có >= 2 đơn / tổng khách hàng
from order_cnt;

---ĐỀ 4: Tính SỐ Ngày Trung BÌnh Giữa Các Lần Mua Hàng Liên Tiếp Của Mỗi Khách Hàng, Tgian Trung Bình Của 2 Đơn Hàng Liên Tiếp
---------Bước 1: Dùng Lag() lấy ngày mua hàng trước của cùng khách hàng
---------Bước 2: Tính khoảng cách ngày (DateDiff) giữa 2 đơn liên tiếp 
---------Bước 3: Tính trung bình khoảng cách đó theo từng khách
with ords as (
  select 
    customer_id
    , order_date 
    , LAG(order_date) OVER(PARTITION BY customer_id ORDER BY order_date) as prev_date -- ngaỳ mua trước đó
from orders
),
diffs as (
  select 
     customer_id
     , DATEDIFF(DAY, prev_date, order_date) as day_diff -- số ngày giữa 2 lần mua liên tiếp
  from ords 
  where prev_date IS NOT NULL -- bỏ đơn đầu tiên (không có prev)
)
select 
   customer_id
   , AVG(day_diff) as avg 
from diffs
group by customer_id;
----=> Ý nghĩa: AVG càng cao -> mua thưa -> nguy cơ churn cao 
----=> Trung Bình khách hàng số 1 mua hàng mỗi 26 ngày 1ln => TB càng cao thì tỷ lệ churn càng cao vì mua hàng thưa thớt.

---ĐỀ 5: Tính Khách Hàng Churn, Tìm Khách Hàng Dẫ từng Mua Nhưng Không Mua trong 60days gần Nhất.
--------Bước 1: Tìm ngày mua hàng gần nhất (MAX order_date) của mối khách
--------Bước 2: Só sánh ngướng = hôm nay - 60 ngày
--------Bước 3: Lọc khách có last_date < ngưỡng => được coi là đã churn
with lats_ord as (
  select 
   customer_id
   , MAX(order_date) as last_date --- lần mua gần nhất
from orders
group by customer_id
)
select 
   c.customer_id 
   , c.name
   , l.last_date
from customers c 
join lats_ord l on c.customer_id= l.customer_id
WHERE l.last_date < DATEADD(DAY, -60, CAST(GETDATE() AS date)) --- không mua trong vòng 60 ngày qua
order by l.last_date; --- sắp xếp từ churn lâu nhất