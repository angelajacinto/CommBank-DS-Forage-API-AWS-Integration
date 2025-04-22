import requests
import pandas as pd
import os
import re
from collections import Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

handle = "CommBank"
url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{handle}&tweet.fields=created_at&expansions=author_id&user.fields=created_at&max_results=100" 
headers = { 
    "Authorization": f"Bearer {BEARER_TOKEN}" 
    } 

# Collect last 100 tweets 
def get_tweets(): 
    response = requests.get(url, headers=headers) 
    
    if response.status_code != 200: 
        print(f"Request failed with status code {response.status_code}") 
        print(response.text) 
        return None 
    
    return response.json() 

# Execute the request 
tweets_data = get_tweets() 

# Display the data 
if tweets_data: 
    print(f"Retrieved {len(tweets_data.get('data', []))} tweets") 

    # Convert to DataFrame for easier analysis 
    tweets_df = pd.DataFrame(tweets_data['data']) 

    # Display first few tweets 
    print(tweets_df.head()) 

    # Save to CSV 
    tweets_df.to_csv(os.path.join('Twitte Data Collection and Analysis', 'commbank_tweets.csv'), index=False) 
    print("Saved tweets to commbank_tweets.csv") 
else: 
    print("Failed to retrieve tweets")