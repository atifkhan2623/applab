# SSIS Customer Data Pipeline

## Overview
This SSIS package processes customer_data.json and loads it into SQL Server.

## Design
- Control Flow:
  - Data Flow Task to process JSON
  - Logging via Error Output
  - Checkpoint enabled

- Data Flow:
  - Source: JSON Source (via Script Component)
  - Derived Column: Clean/standardize fields
  - Conditional Split: Valid vs Invalid records
  - Destination: SQL Customers table
  - Error Output -> ErrorLog table

## Features
- Variables for file path and connection
- Checkpoints enabled for restartability
- Logging for failures

## Validation
- NULL checks
- Data type conversion
- Reject invalid records

## Scaling Approach
- Partitioned loads
- Incremental loading
- Parallel data flows

Generated on 2026-06-23 16:49:31.167499
