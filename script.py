import tweepy
from textblob import TextBlob
import pandas as pd
import time
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace with your Bearer Token
# Get your Bearer Token from https://developer.twitter.com/
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAOrs2QEAAAAA4G82iP05YgAsgHfHtF%2BbGJGru4Q%3Dbw9gSZhXzVIZrEJM4UyKk4h4D62rqF2aWMisET7ya6gUlVoN38'

# Set up Tweepy client with wait_on_rate_limit=True
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

# Function to load existing tweets from CSV to avoid duplicates
def load_existing_tweets(csv_file):
    if os.path.exists(csv_file):
        try:
            existing_df = pd.read_csv(csv_file)
            logger.info(f"Loaded {len(existing_df)} existing tweets from {csv_file}")
            return existing_df
        except Exception as e:
            logger.warning(f"Error loading existing CSV: {e}")
            return pd.DataFrame()
    else:
        logger.info(f"No existing CSV file found at {csv_file}")
        return pd.DataFrame()

# Function to append new tweets to CSV
def append_tweets_to_csv(new_df, csv_file, existing_df=None):
    if existing_df is None:
        existing_df = load_existing_tweets(csv_file)
    
    if len(existing_df) > 0:
        # Remove duplicates based on tweet text
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        # Drop duplicates based on text content
        combined_df = combined_df.drop_duplicates(subset=['Text'], keep='first')
        new_tweets_added = len(combined_df) - len(existing_df)
        logger.info(f"Added {new_tweets_added} new unique tweets (removed {len(new_df) - new_tweets_added} duplicates)")
    else:
        combined_df = new_df
        logger.info(f"Created new CSV with {len(combined_df)} tweets")
    
    # Add timestamp for when data was collected
    if 'Collection_Time' not in combined_df.columns:
        combined_df['Collection_Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save to CSV
    combined_df.to_csv(csv_file, index=False)
    logger.info(f"Saved {len(combined_df)} total tweets to {csv_file}")
    
    return combined_df

# Function to search recent tweets by keyword with rate limiting
def fetch_tweets(keyword, max_results=100):
    tweet_data = []
    tweets_collected = 0
    next_token = None
    
    # Twitter API v2 allows max 100 tweets per request for search_recent_tweets
    # We'll paginate to get the desired number of tweets
    while tweets_collected < max_results:
        try:
            # Calculate how many tweets to request in this batch
            batch_size = min(100, max_results - tweets_collected)
            
            logger.info(f"Fetching batch of {batch_size} tweets... (Total collected: {tweets_collected})")
            
            #API request
            response = client.search_recent_tweets(
                query=keyword, 
                max_results=batch_size, 
                tweet_fields=["created_at", "lang"],
                next_token=next_token
            )
            
            # Check if we got any tweets
            if not response.data:
                logger.info("No more tweets available")
                break
            
            # Process tweets
            for tweet in response.data:
                if tweet.lang == "en":
                    text = tweet.text
                    sentiment = TextBlob(text).sentiment.polarity
                    sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
                    tweet_data.append({
                        "Text": text, 
                        "Sentiment": sentiment_label,
                        "Created_At": tweet.created_at if hasattr(tweet, 'created_at') else None
                    })
            
            tweets_collected += len(response.data)
            
            # Check if there are more tweets to fetch
            if 'next_token' in response.meta:
                next_token = response.meta['next_token']
            else:
                logger.info("No more tweets available (no next_token)")
                break
                
            # Add a small delay between requests to be respectful
            time.sleep(1)
            
        except tweepy.errors.TooManyRequests as e:
            logger.warning("Rate limit exceeded. Waiting...")
            # If wait_on_rate_limit doesn't work, manually wait
            time.sleep(900)  # Wait 15 minutes
            continue
            
        except Exception as e:
            logger.error(f"Error fetching tweets: {e}")
            break
    
    logger.info(f"Total tweets collected: {len(tweet_data)}")
    return pd.DataFrame(tweet_data)

# Configuration
KEYWORD = "AI"
CSV_FILE = "tweets_sentiment.csv"
MAX_RESULTS = 10  # Start small due to rate limits
SLEEP_INTERVAL = 300  # Sleep for 5 minutes between cycles (300 seconds)

def main_loop():
    """Main loop that runs continuously until keyboard interrupt"""
    cycle_count = 0
    
    print("Starting continuous tweet collection...")
    print(f"Keyword: {KEYWORD}")
    print(f"Max results per cycle: {MAX_RESULTS}")
    print(f"Sleep interval: {SLEEP_INTERVAL} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            cycle_count += 1
            print(f"\n{'='*50}")
            print(f"CYCLE {cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*50}")
            
            # Load existing data
            existing_df = load_existing_tweets(CSV_FILE)
            print(f"Currently have {len(existing_df)} tweets in the dataset")
            
            # Fetch new tweets
            print(f"Fetching up to {MAX_RESULTS} new tweets for keyword: {KEYWORD}")
            new_df = fetch_tweets(KEYWORD, max_results=MAX_RESULTS)
            
            if len(new_df) > 0:
                print(f"Fetched {len(new_df)} new tweets")
                print("Sample of new tweets:")
                print(new_df.head())
                
                # Append to existing data
                combined_df = append_tweets_to_csv(new_df, CSV_FILE, existing_df)
                
                print(f"\n=== CYCLE {cycle_count} SUMMARY ===")
                print(f"Total tweets in dataset: {len(combined_df)}")
                print(f"New tweets added this cycle: {len(combined_df) - len(existing_df)}")
                print(f"Saved to: {CSV_FILE}")
                
                # Show sentiment distribution
                if 'Sentiment' in combined_df.columns:
                    print(f"\nSentiment distribution:")
                    print(combined_df['Sentiment'].value_counts())
            else:
                print("No new tweets fetched this cycle")
            
            # Sleep before next cycle
            print(f"\nSleeping for {SLEEP_INTERVAL} seconds before next cycle...")
            print(f"Next cycle will start at: {datetime.fromtimestamp(time.time() + SLEEP_INTERVAL).strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(SLEEP_INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*50}")
        print("STOPPING - Keyboard interrupt received")
        print(f"{'='*50}")
        print(f"Total cycles completed: {cycle_count}")
        
        # Show final statistics
        final_df = load_existing_tweets(CSV_FILE)
        print(f"Final dataset contains {len(final_df)} tweets")
        if len(final_df) > 0 and 'Sentiment' in final_df.columns:
            print(f"\nFinal sentiment distribution:")
            print(final_df['Sentiment'].value_counts())
        
        print(f"\nData saved in: {CSV_FILE}")
        print("Script terminated gracefully.")
    
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        logger.error(f"Unexpected error in main loop: {e}")
        print("Script terminated due to error.")

if __name__ == "__main__":
    main_loop()
