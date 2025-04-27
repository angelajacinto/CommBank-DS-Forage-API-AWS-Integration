# CommBank-DS-Forage-API-AWS-Integration
Commonwealth Bank Data Science Virtual Experience

# AWS Twitter Data Pipeline
This project implements a serverless Twitter data pipeline using AWS services:

## Architecture
![Architecture Diagram](AWS%20Lambda%20Functions/model-architecture.drawio.png)

## AWS Lambda
- **Function 1**: Collects tweets from Twitter API and stores in S3
- **Function 2**: Processes tweets from S3 and loads into RDS

## Amazon S3
- Serves as data lake for raw Twitter JSON data
- Provides event triggers for the processing Lambda

## Amazon RDS (PostgreSQL)
- Implements a 12-table relational schema
- Stores structured Twitter data for analysis
- Optimized with indexes for common query patterns

## Deployment Instructions
See [deployment_instructions.md](AWS%20Lambda%20Functions/deployment_instructions.md)
