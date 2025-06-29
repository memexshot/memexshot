#!/usr/bin/env python3
"""
Test Twitter Search - Find tweets with our test pattern
"""

import os
import tweepy
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_search():
    """Test Twitter search for Perfecto pattern"""
    
    print("🔍 TWITTER SEARCH TEST")
    print("="*60)
    
    # Setup client
    client = tweepy.Client(
        bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    
    # Search queries to test
    queries = [
        '"Perfecto" "@memeXshot"',  # Exact match
        'Perfecto @memeXshot',       # Without quotes
        'Perfecto memeXshot',        # Without @
        '@memeXshot Perfecto',       # Different order
        'to:memeXshot Perfecto'      # Direct mention
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        print("-"*60)
        
        try:
            # Search with different parameters
            tweets = client.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=['created_at', 'author_id', 'text'],
                expansions=['author_id'],
                user_fields=['username', 'public_metrics']
            )
            
            if tweets.data:
                print(f"✅ Found {len(tweets.data)} tweets!")
                
                # Get user data
                users = {}
                if hasattr(tweets, 'includes') and 'users' in tweets.includes:
                    for user in tweets.includes['users']:
                        users[user.id] = user
                
                for tweet in tweets.data:
                    author = users.get(tweet.author_id)
                    username = author.username if author else "unknown"
                    followers = author.public_metrics.get('followers_count', 0) if author else 0
                    
                    print(f"\n  Tweet ID: {tweet.id}")
                    print(f"  From: @{username} ({followers} followers)")
                    print(f"  Text: {tweet.text[:100]}...")
                    print(f"  Created: {tweet.created_at}")
            else:
                print("❌ No tweets found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test our specific pattern
    print("\n" + "="*60)
    print("🎯 TESTING EXACT PATTERN")
    print("="*60)
    
    exact_query = '"Perfecto" "@memeXshot" -is:retweet has:images'
    print(f"Query: {exact_query}")
    
    try:
        tweets = client.search_recent_tweets(
            query=exact_query,
            max_results=10,
            tweet_fields=['created_at', 'author_id', 'text', 'attachments'],
            expansions=['attachments.media_keys', 'author_id'],
            media_fields=['url', 'type'],
            user_fields=['username', 'public_metrics']
        )
        
        if tweets.data:
            print(f"\n✅ Found {len(tweets.data)} tweets with our pattern!")
            
            for tweet in tweets.data:
                print(f"\n  Full text: {tweet.text}")
                has_image = hasattr(tweet, 'attachments') and tweet.attachments
                print(f"  Has image: {'✅' if has_image else '❌'}")
        else:
            print("\n❌ No tweets found with exact pattern")
            print("\nPossible reasons:")
            print("1. Tweet is too new (API has ~10-30 second delay)")
            print("2. Tweet doesn't have an image")
            print("3. Account is private or tweet was deleted")
            print("4. Case sensitivity or spacing issues")
            
    except Exception as e:
        print(f"\n❌ Search error: {e}")

if __name__ == "__main__":
    test_search()