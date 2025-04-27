import json
import boto3
import psycopg2
import os
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function triggered by S3 events that processes Twitter data and loads it into RDS.
    This function is triggered when a new Twitter data file is uploaded to S3.
    """
    logger.info("S3 to RDS processing function started")
    
    # Get the S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    logger.info(f"Processing file {key} from bucket {bucket}")
    
    try:
        # Get the file from S3
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=key)
        twitter_data = json.loads(response['Body'].read().decode('utf-8'))
        logger.info(f"Successfully loaded JSON data with {len(twitter_data.get('data', []))} tweets")
        
        # Get database credentials from environment variables
        db_host = os.environ.get('DB_HOST')
        db_name = os.environ.get('DB_NAME')
        db_user = os.environ.get('DB_USER')
        db_password = os.environ.get('DB_PASSWORD')
        db_port = os.environ.get('DB_PORT', '5432')
        
        # Validate that all required environment variables are set
        if not all([db_host, db_name, db_user, db_password]):
            error_msg = "Missing required database environment variables"
            logger.error(error_msg)
            return {
                'statusCode': 500,
                'body': json.dumps(error_msg)
            }
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        logger.info("Successfully connected to PostgreSQL")
        
        # Process the Twitter data
        process_twitter_data(conn, twitter_data)
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed {len(twitter_data.get("data", []))} tweets from {key}')
        }
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing file: {str(e)}')
        }

def process_twitter_data(conn, twitter_data):
    """Process Twitter data and insert into PostgreSQL database."""
    try:
        cur = conn.cursor()
        
        # Process users
        if 'includes' in twitter_data and 'users' in twitter_data['includes']:
            process_users(cur, twitter_data['includes']['users'])
        
        # Process tweets
        if 'data' in twitter_data:
            process_tweets(cur, twitter_data['data'])
            process_mentions(cur, twitter_data['data'])
            process_hashtags(cur, twitter_data['data'])
            process_urls(cur, twitter_data['data'])
        
        # Commit the transaction
        conn.commit()
        logger.info("Successfully committed data to PostgreSQL")
    
    except Exception as e:
        conn.rollback()
        logger.error(f"Error in process_twitter_data: {str(e)}")
        raise e
    
    finally:
        if conn:
            cur.close()
            conn.close()
            logger.info("Database connection closed")

def process_users(cur, users):
    """Insert or update users in the database."""
    logger.info(f"Processing {len(users)} users")
    
    for user in users:
        # Check if user exists
        cur.execute("SELECT 1 FROM users WHERE user_id = %s", (user['id'],))
        user_exists = cur.fetchone() is not None
        
        if not user_exists:
            # Insert new user
            cur.execute("""
                INSERT INTO users (
                    user_id, username, display_name, created_at, is_commbank
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                user['id'],
                user['username'],
                user['name'],
                user['created_at'],
                user['username'].lower() == 'commbank'
            ))
            logger.info(f"Inserted new user: {user['username']}")

def process_tweets(cur, tweets):
    """Insert tweets into the database."""
    logger.info(f"Processing {len(tweets)} tweets")
    
    for tweet in tweets:
        # Check if tweet exists
        cur.execute("SELECT 1 FROM tweets WHERE tweet_id = %s", (tweet['id'],))
        tweet_exists = cur.fetchone() is not None
        
        if not tweet_exists:
            # Check for links and media
            has_link = 'https://' in tweet['text'] or 'http://' in tweet['text']
            has_media = False  # Would need media entities from the Twitter API
            is_retweet = tweet['text'].startswith('RT @')
            
            # Insert tweet
            cur.execute("""
                INSERT INTO tweets (
                    tweet_id, user_id, content, created_at, 
                    has_link, has_media, is_retweet
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                tweet['id'],
                tweet['author_id'],
                tweet['text'],
                tweet['created_at'],
                has_link,
                has_media,
                is_retweet
            ))
            logger.info(f"Inserted tweet: {tweet['id']}")

def process_mentions(cur, tweets):
    """Extract and insert user mentions from tweets."""
    for tweet in tweets:
        # Simple mention extraction using regex-like approach
        words = tweet['text'].split()
        mention_index = 0
        
        for word in words:
            if word.startswith('@') and len(word) > 1:
                username = word[1:].rstrip('.:,;!?')
                
                # First, check if we know this user
                cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                result = cur.fetchone()
                
                if result:
                    user_id = result[0]
                else:
                    # Create placeholder user if not found
                    cur.execute("""
                        INSERT INTO users (user_id, username, is_commbank)
                        VALUES (%s, %s, %s)
                        RETURNING user_id
                    """, (
                        f"placeholder_{username}",
                        username,
                        False
                    ))
                    user_id = cur.fetchone()[0]
                
                # Insert mention
                cur.execute("""
                    INSERT INTO mentions (tweet_id, user_id, mention_index)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    tweet['id'],
                    user_id,
                    mention_index
                ))
                mention_index += 1

def process_hashtags(cur, tweets):
    """Extract and insert hashtags from tweets."""
    for tweet in tweets:
        # Simple hashtag extraction
        words = tweet['text'].split()
        
        for word in words:
            if word.startswith('#') and len(word) > 1:
                hashtag_text = word[1:].lower().rstrip('.:,;!?')
                
                if hashtag_text:
                    # Insert or get hashtag
                    cur.execute("""
                        INSERT INTO hashtags (hashtag_text)
                        VALUES (%s)
                        ON CONFLICT (hashtag_text) DO UPDATE SET hashtag_text = EXCLUDED.hashtag_text
                        RETURNING hashtag_id
                    """, (hashtag_text,))
                    hashtag_id = cur.fetchone()[0]
                    
                    # Link hashtag to tweet
                    cur.execute("""
                        INSERT INTO tweet_hashtags (tweet_id, hashtag_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                    """, (
                        tweet['id'],
                        hashtag_id
                    ))

def process_urls(cur, tweets):
    """Extract and insert URLs from tweets."""
    for tweet in tweets:
        # Very simple URL extraction
        words = tweet['text'].split()
        
        for word in words:
            if word.startswith('http://') or word.startswith('https://'):
                url = word.rstrip('.:,;!?')
                
                # Try to extract domain
                domain = url.split('/')[2] if len(url.split('/')) > 2 else ''
                is_commbank_domain = 'commbank' in domain.lower()
                
                # Insert URL
                cur.execute("""
                    INSERT INTO urls (tweet_id, expanded_url, domain, is_commbank_domain)
                    VALUES (%s, %s, %s, %s)
                """, (
                    tweet['id'],
                    url,
                    domain,
                    is_commbank_domain
                ))