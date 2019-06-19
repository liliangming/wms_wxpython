create table customer
(
customer_id integer primary key autoincrement,
customer_name varchar(100),
customer_addr varchar(200),
phone_number varchar(50),
email varchar(50),
remark varchar(200),
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
)