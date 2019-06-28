drop table customer;
create table customer
(
customer_id integer primary key autoincrement,
customer_name varchar(100),
customer_addr varchar(200),
phone_number varchar(50),
email varchar(50),
remark varchar(200),
status integer default 1,
customer_type varchar(50),
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
);

drop table supplier;
create table supplier
(
supplier_id integer primary key autoincrement,
supplier_name varchar(100),
supplier_addr varchar(200),
phone_number varchar(50),
email varchar(50),
remark varchar(200),
status integer default 1,
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
);

drop table storehouse;
create table storehouse
(
sh_id varchar(50) primary key,
sh_name varchar(100),
sh_addr varchar(200),
remark varchar(200),
status integer default 1,
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
);

drop table storehouse_location;
create table storehouse_location
(
sl_id varchar(50) primary key,
sh_id varchar(50),
sl_name varchar(100),
remark varchar(200),
status integer default 1,
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
);

drop table storehouse;
create table storehouse
(
sh_id integer primary key autoincrement,
sh_name varchar(100),
sh_addr varchar(200),
remark varchar(200),
status integer default 1,
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
);

drop table sys_dictionary;
create table sys_dictionary
(
dic_key integer primary key autoincrement,
dic_type varchar(10),
dic_value varchar(100),
remark varchar(200),
status integer default 1,
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50),
father_key integer
);

drop table product;
create table product
(
product_id integer primary key autoincrement,
product_code varchar(100),
product_name varchar(100),
product_desc varchar(100),
product_category integer,
remark varchar(200),
status integer default 1,
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
);

drop table product_attr;
create table product_attr
(
attr_id integer primary key autoincrement,
product_id integer,
attr_name varchar(100),
attr_value varchar(100),
sort_no integer,
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
);

drop table product_images;
create table product_images
(
image_id integer primary key autoincrement,
product_id integer,
image_name varchar(100),
attach_path varchar(100),
remark varchar(200),
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
);

drop table product_attach;
create table product_attach
(
attach_id integer primary key autoincrement,
product_id integer,
attach_name varchar(100),
attach_path varchar(100),
remark varchar(200),
ctime datetime,
cby varchar(50),
utime datetime,
uby varchar(50)
);