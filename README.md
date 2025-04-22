# CommBank-DS-Forage-API-AWS-Integration
Commonwealth Bank Data Science Virtual Experience

# AWS Lambda Function for Twitter Data Collection
This Lambda function collects tweets from the CommBank Twitter account and stores them in an S3 bucket.

## Configuration
- Runtime: Python 3.12
- Trigger: Manual
- Output: JSON files in S3

## Environment Variables
- TWITTER_BEARER_TOKEN: Twitter API authentication token
- S3_BUCKET_NAME: Name of the S3 bucket for storage

## Implementation Details
The function uses the Twitter API v2 endpoint to collect recent tweets from the @CommBank account.
