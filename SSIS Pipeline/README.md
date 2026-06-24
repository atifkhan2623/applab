# SSIS Customer Data Pipeline

## 📌 Overview
This project implements an SSIS (SQL Server Integration Services) package to process customer data from a JSON file and load it into a PostgreSQL database. The pipeline performs data extraction, transformation, validation, and error handling.

## 📂 Source Data

Input file: `customer_data.json`

Sample structure:
```json
[
  {
    "customer_id": "C001",
    "customer_name": "John Smith",
    "email": "user@example.com",
    "region": null,
    "join_date": "2024-06-20",
    "loyalty_points": 840
  }
]

## 📂 Destination Data

Table: `customer`

CREATE TABLE customer (
    customer_id VARCHAR(256),
    customer_name VARCHAR(256),
    email VARCHAR(256),
    region VARCHAR(256),
    join_date VARCHAR(256),
    loyalty_points VARCHAR(256)
);