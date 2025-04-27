-- users table
CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    bio TEXT,
    profile_image_url TEXT,
    verified BOOLEAN DEFAULT FALSE,
    followers_count INTEGER,
    following_count INTEGER,
    created_at TIMESTAMP,
    location VARCHAR(255),
    is_commbank BOOLEAN DEFAULT FALSE
);

-- tweets table
CREATE TABLE tweets (
    tweet_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(user_id),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    source VARCHAR(255),
    retweet_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    reply_count INTEGER DEFAULT 0,
    quote_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    is_retweet BOOLEAN DEFAULT FALSE,
    original_tweet_id VARCHAR(255),
    has_media BOOLEAN DEFAULT FALSE,
    has_link BOOLEAN DEFAULT FALSE,
    sentiment_score FLOAT,
    topic_category VARCHAR(255)
);

-- mentions table
CREATE TABLE mentions (
    mention_id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255) REFERENCES tweets(tweet_id),
    user_id VARCHAR(255) REFERENCES users(user_id),
    mention_index INTEGER NOT NULL
);

-- hashtags table
CREATE TABLE hashtags (
    hashtag_id SERIAL PRIMARY KEY,
    hashtag_text VARCHAR(255) NOT NULL UNIQUE
);

-- tweet_hashtags junction table
CREATE TABLE tweet_hashtags (
    tweet_id VARCHAR(255) REFERENCES tweets(tweet_id),
    hashtag_id INTEGER REFERENCES hashtags(hashtag_id),
    PRIMARY KEY (tweet_id, hashtag_id)
);

-- media table
CREATE TABLE media (
    media_id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255) REFERENCES tweets(tweet_id),
    media_type VARCHAR(50) NOT NULL,
    media_url TEXT NOT NULL,
    alt_text TEXT
);

-- urls table
CREATE TABLE urls (
    url_id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255) REFERENCES tweets(tweet_id),
    expanded_url TEXT NOT NULL,
    display_url VARCHAR(255),
    domain VARCHAR(255),
    is_commbank_domain BOOLEAN DEFAULT FALSE
);

-- conversations table
CREATE TABLE conversations (
    conversation_id VARCHAR(255) PRIMARY KEY,
    initial_tweet_id VARCHAR(255) REFERENCES tweets(tweet_id),
    tweet_count INTEGER DEFAULT 1,
    user_count INTEGER DEFAULT 1,
    last_update_time TIMESTAMP
);

-- tweet_conversations junction table
CREATE TABLE tweet_conversations (
    tweet_id VARCHAR(255) REFERENCES tweets(tweet_id),
    conversation_id VARCHAR(255) REFERENCES conversations(conversation_id),
    sequence_order INTEGER NOT NULL,
    PRIMARY KEY (tweet_id, conversation_id)
);

-- replies table
CREATE TABLE replies (
    reply_id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255) REFERENCES tweets(tweet_id),
    parent_tweet_id VARCHAR(255) REFERENCES tweets(tweet_id),
    reply_depth INTEGER DEFAULT 0
);

-- engagement_metrics table
CREATE TABLE engagement_metrics (
    metric_id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255) REFERENCES tweets(tweet_id),
    timestamp TIMESTAMP NOT NULL,
    retweet_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    reply_count INTEGER DEFAULT 0,
    quote_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0
);

-- sentiment_analysis table
CREATE TABLE sentiment_analysis (
    analysis_id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255) REFERENCES tweets(tweet_id) UNIQUE,
    sentiment_score FLOAT,
    sentiment_magnitude FLOAT,
    positive_phrases TEXT,
    negative_phrases TEXT,
    key_entities TEXT
);

-- indexes for performance optimization
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_tweets_created_at ON tweets(created_at);
CREATE INDEX idx_tweets_user_id ON tweets(user_id);
CREATE INDEX idx_hashtags_text ON hashtags(hashtag_text);
CREATE INDEX idx_conversations_id ON conversations(conversation_id);
CREATE INDEX idx_replies_parent ON replies(parent_tweet_id);