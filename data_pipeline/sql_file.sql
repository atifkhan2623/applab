CREATE TABLE sales_data (
    transaction_id VARCHAR(20) PRIMARY KEY,
    customer_id    VARCHAR(20),
    product_id     VARCHAR(20),
    product_name   VARCHAR(100),
    category       VARCHAR(50),
    price          DOUBLE PRECISION,
    quantity       INTEGER,
    discount       DOUBLE PRECISION,
    total_amount   DOUBLE PRECISION,
    date           TIMESTAMP,
    region         VARCHAR(20)
);