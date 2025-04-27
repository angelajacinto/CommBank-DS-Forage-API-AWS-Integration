import os
import json
import requests
import boto3
import logging
from datetime import datetime

# Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Get credentials from environment variables
    bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')

    if not bearer_token:
        logger.error("TWITTER_BEARER_TOKEN not set")
        return {
            'statusCode': 500,
            'body': 'TWITTER_BEARER_TOKEN not set'
        }
    
    # Define request parameters
    handle = "CommBank"
    url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{handle}&tweet.fields=created_at&expansions=author_id&user.fields=created_at&max_results=100"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    
    logger.info("Making API request to Twitter")

    # Make API request
    try:
        response = requests.get(url, headers=headers)
        logger.info(f"Response status code: {response.status_code}")
        tweets_data = response.json()
    except Exception as e:
        logger.error(f"Error making request: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error making request: {str(e)}'
        }

    # Store in S3
    if 'data' in tweets_data:
        logger.info(f"Retrieved {len(tweets_data['data'])} tweets")
        s3_bucket = os.environ.get('S3_BUCKET_NAME')
        if not s3_bucket:
            logger.error("S3_BUCKET_NAME not set")
            return {
                'statusCode': 500,
                'body': 'S3_BUCKET_NAME not set'
            }
        
        try:
            s3 = boto3.client('s3')
        
            # Generate a filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"commbank_tweets_{timestamp}.json"

            logger.info(f"Uploading to S3 bucket: {s3_bucket}, key: {filename}")
        
            # Upload JSON to S3
            s3.put_object(
                Bucket=os.environ.get('S3_BUCKET_NAME'),
                Key=filename,
                Body=json.dumps(tweets_data),
                ContentType='application/json'
            )

            logger.info("Upload successful")
        
            return {
                'statusCode': 200,
                'body': f'Successfully processed {len(tweets_data["data"])} tweets and saved to S3'
            }
        except Exception as e:
            logger.error(f"Error uploading to S3: {str(e)}")
            return {
                'statusCode': 500,
                'body': f'Error uploading to S3: {str(e)}'
            }
    else:
        logger.warning(f"No data in response: {json.dumps(tweets_data)}")
        return {
            'statusCode': 400,
            'body': 'Failed to retrieve tweets: ' + json.dumps(tweets_data)
        }
