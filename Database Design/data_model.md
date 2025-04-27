# Twitter Data Model for CommBank Analysis
This document provides an overview of the database structure designed for storing and analyzing Twitter data from CommBank’s account. The schema is organized to reduce redundancy while maintaining data integrity and enabling efficient analysis.

## Main Entities  
### Users
The `users` table stores information about Twitter users, including the CommBank official account and users who interact with it. Key fields include:
- **user_id**: Unique Twitter ID (primary key)
- **username**: Twitter handle 
- **is_commbank**: Flag identifying CommBank's official accounts
- **created_at**: When the account was created

### Tweets
The `tweets` table contains all tweets, including CommBank's posts and their replies. Key fields include:
- **tweet_id**: Unique Twitter ID (primary key)
- **user_id**: Who posted the tweet (foreign key to users)
- **content**: The actual text of the tweet
- **created_at**: When the tweet was posted
- **engagement metrics**: retweet_count, like_count, etc.
- **classification flags**: has_media, has_link, is_retweet

## Relationships and Connections

### Mentions
The `mentions` table tracks when users are mentioned in tweets:
- Links tweets to the users mentioned in them
- Preserves the order of mentions through mention_index
- Enables analysis of which users CommBank mentions most frequently

### Hashtags and Tweet_Hashtags
These tables implement a many-to-many relationship between tweets and hashtags:
- `hashtags` stores unique hashtag texts
- `tweet_hashtags` junction table connects tweets to the hashtags they contain
- Enables trending topic analysis and hashtag effectiveness measurement

### Media and URLs
These tables store rich content within tweets:
- `media` captures images, videos, and GIFs attached to tweets
- `urls` stores links shared in tweets, with special tracking for CommBank domains
- Enables analysis of media engagement and link click-through patterns

## Conversation Tracking

### Conversations and Tweet_Conversations
These tables track threaded conversations:
- `conversations` identifies unique conversation threads
- `tweet_conversations` maps tweets to their conversations with sequence ordering
- Enables analysis of conversation depth, duration, and participant diversity

### Replies
The `replies` table specifically tracks reply relationships:
- Links reply tweets to their parent tweets
- Tracks reply depth (how deep in a thread)
- Enables customer service response time analysis

## Analytics Support

### Engagement_Metrics
This table stores time-series data on tweet engagement:
- Tracks metrics at different points in time
- Enables analysis of how engagement grows over time
- Supports comparative engagement analysis across tweet types

### Sentiment_Analysis
This table stores sentiment analysis results:
- Links each tweet to its sentiment score and key entities
- Stores positive and negative phrases for deeper understanding
- Enables sentiment trend analysis and topic-based sentiment

## Performance Optimization

The schema includes strategic indexes to optimize common query patterns:
- **idx_users_username**: For looking up users by username
- **idx_tweets_created_at**: For time-based queries and feeds
- **idx_hashtags_text**: For hashtag searches
- **idx_replies_parent**: For finding all replies to specific tweets

## Data Flow

1. Twitter API provides raw JSON data
2. Lambda function 1 retrieves and stores this data in S3
3. Lambda function 2 processes the JSON and populates this database
4. Structured data enables complex queries and analysis