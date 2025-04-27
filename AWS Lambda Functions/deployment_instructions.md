# Setting Up Environment Variables for Lambda Functions

This document explains how to configure the environment variables required for both Lambda functions in our Twitter data pipeline.

## Environment Variables Overview

The Twitter data pipeline uses two Lambda functions:
1. **Twitter Collector**: Retrieves tweets from the Twitter API and stores them in S3
2. **S3 to RDS Processor**: Processes the tweets from S3 and inserts them into PostgreSQL RDS

Each function requires specific environment variables to operate correctly.

## Lambda Function 1: Twitter Collector

### Required Variables

| Variable Name | Description |
|---------------|-------------|
| `API_KEY` | Twitter API Key (from developer portal) |
| `API_KEY_SECRET` | Twitter API Key Secret (from developer portal) |
| `BEARER_TOKEN` | Twitter API Bearer Token (from developer portal) |
| `S3_BUCKET_NAME` | Name of the S3 bucket where tweets will be stored |

### Setting Up in AWS Lambda Console

1. Navigate to the Lambda function in the AWS Console
2. Select the "Configuration" tab
3. Click on "Environment variables"
4. Click "Edit"
5. Add each variable with its corresponding value:
   - Key: `BEARER_TOKEN`, Value: [your Twitter bearer token]
   - Key: `S3_BUCKET_NAME`, Value: [your S3 bucket name]
6. Click "Save"

## Lambda Function 2: S3 to RDS Processor

### Required Variables

| Variable Name | Description | Default |
|---------------|-------------|---------|
| `DB_HOST` | PostgreSQL RDS endpoint | - |
| `DB_NAME` | Database name | - |
| `DB_USER` | Database username | - |
| `DB_PASSWORD` | Database password | - |
| `DB_PORT` | Database port | 5432 |

### Setting Up in AWS Lambda Console

1. Navigate to the Lambda function in the AWS Console
2. Select the "Configuration" tab
3. Click on "Environment variables"
4. Click "Edit"
5. Add each variable with its corresponding value:
   - Key: `DB_HOST`, Value: [your RDS endpoint]
   - Key: `DB_NAME`, Value: [your database name]
   - Key: `DB_USER`, Value: [your database username]
   - Key: `DB_PASSWORD`, Value: [your database password]
   - Key: `DB_PORT`, Value: 5432
6. Click "Save"