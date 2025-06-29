#!/usr/bin/env python3
"""
Integration Test - Simulates Twitter Bot with Mock Data
Tests the complete flow from tweet detection to database insertion
"""

import os
import sys
import time
import random
from datetime import datetime
from uuid import uuid4

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase import create_client
from config.supabase_config import SUPABASE_URL, SUPABASE_KEY

class MockTweet:
    """Mock tweet for testing"""
    def __init__(self, id, text, author_username, followers_count, has_image=True):
        self.id = str(id)
        self.text = text
        self.author_id = f"user_{id}"
        self.created_at = datetime.now()
        self.attachments = {'media_keys': [f'media_{id}']} if has_image else None
        
        # Mock includes data
        self.includes = {
            'users': [{
                'id': self.author_id,
                'username': author_username,
                'name': f"{author_username} User",
                'public_metrics': {
                    'followers_count': followers_count,
                    'following_count': random.randint(100, 1000),
                    'tweet_count': random.randint(50, 5000)
                }
            }],
            'media': [{
                'media_key': f'media_{id}',
                'type': 'photo',
                'url': f'https://pbs.twimg.com/media/mock_image_{id}.jpg'
            }] if has_image else []
        }

class IntegrationTester:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.bot_username = 'memeXshot'
        self.min_followers = 500
        self.processed_tweets = set()
        
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def generate_mock_tweets(self):
        """Generate 15 mock tweets with various scenarios"""
        self.log("🎭 Generating 15 mock tweets...")
        
        tweets = []
        
        # 10 correct tweets (various tickers)
        correct_tickers = ['MOON', 'PEPE', 'DOGE', 'SHIB', 'BTC', 'ETH', 'SOL', 'MATIC', 'LINK', 'UNI']
        for i, ticker in enumerate(correct_tickers):
            tweets.append(MockTweet(
                id=f"1000{i}",
                text=f"Launch ${ticker} @{self.bot_username} to the moon! 🚀",
                author_username=f"crypto_user_{i}",
                followers_count=random.randint(600, 10000),
                has_image=True
            ))
        
        # 5 incorrect tweets
        # 1. Wrong format
        tweets.append(MockTweet(
            id="10010",
            text=f"Check out $FAIL @{self.bot_username}",
            author_username="wrong_format",
            followers_count=1000,
            has_image=True
        ))
        
        # 2. No image
        tweets.append(MockTweet(
            id="10011",
            text=f"Launch $NOIMG @{self.bot_username}",
            author_username="no_image_user",
            followers_count=2000,
            has_image=False
        ))
        
        # 3. Too few followers
        tweets.append(MockTweet(
            id="10012",
            text=f"Launch $POOR @{self.bot_username}",
            author_username="small_account",
            followers_count=100,
            has_image=True
        ))
        
        # 4. Wrong bot mention
        tweets.append(MockTweet(
            id="10013",
            text="Launch $WRONG @someotherbot",
            author_username="confused_user",
            followers_count=1500,
            has_image=True
        ))
        
        # 5. Ticker too short
        tweets.append(MockTweet(
            id="10014",
            text=f"Launch $AB @{self.bot_username}",
            author_username="short_ticker",
            followers_count=3000,
            has_image=True
        ))
        
        # Shuffle to simulate random order
        random.shuffle(tweets)
        
        self.log(f"✅ Generated {len(tweets)} mock tweets")
        return tweets
    
    def parse_tweet(self, tweet_text):
        """Parse tweet for Launch command"""
        import re
        text = ' '.join(tweet_text.split())
        pattern = rf'Launch\s+\$?([A-Za-z0-9]+)\s+@{self.bot_username}'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            ticker = match.group(1).upper()
            if 3 <= len(ticker) <= 10:
                return ticker
        return None
    
    def get_tweet_image(self, tweet):
        """Extract image URL from tweet"""
        try:
            if hasattr(tweet, 'attachments') and tweet.attachments:
                media_keys = tweet.attachments.get('media_keys', [])
                
                if media_keys and hasattr(tweet, 'includes') and 'media' in tweet.includes:
                    for media in tweet.includes['media']:
                        if media['media_key'] in media_keys and media['type'] == 'photo':
                            return media['url']
            return None
        except:
            return None
    
    def process_tweet(self, tweet):
        """Process a single tweet"""
        # Get author info
        author = None
        followers_count = 0
        
        if hasattr(tweet, 'includes') and 'users' in tweet.includes:
            for user in tweet.includes['users']:
                if user['id'] == tweet.author_id:
                    author = user['username']
                    followers_count = user['public_metrics'].get('followers_count', 0)
                    break
        
        if not author:
            self.log(f"⚠️  Could not find author for tweet {tweet.id}")
            return False
        
        # Parse ticker
        ticker = self.parse_tweet(tweet.text)
        if not ticker:
            self.log(f"❌ Invalid format in tweet from @{author}: '{tweet.text}'")
            return False
        
        # Check followers
        if followers_count < self.min_followers:
            self.log(f"❌ @{author} has only {followers_count} followers (min: {self.min_followers})")
            # Add to queue as rejected
            self.add_to_queue_rejected(tweet, ticker, author, followers_count)
            return False
        
        # Check for image
        image_url = self.get_tweet_image(tweet)
        if not image_url:
            self.log(f"❌ No image found in tweet from @{author}")
            return False
        
        # All checks passed - add to queue
        self.log(f"✅ Valid tweet from @{author}: ${ticker} ({followers_count} followers)")
        return self.add_to_queue(tweet, ticker, author, followers_count)
    
    def add_to_queue(self, tweet, ticker, author, followers_count):
        """Add tweet to processing queue"""
        try:
            tweet_url = f"https://twitter.com/{author}/status/{tweet.id}"
            image_url = self.get_tweet_image(tweet)
            
            queue_data = {
                'tweet_id': str(tweet.id),
                'twitter_user': author,
                'ticker': ticker,
                'name': ticker,
                'description': 'Bu token memeXshot aracılığı ile Moonshot\'ta create edildi',
                'website': tweet_url,
                'twitter': f"@{author}",
                'image_url': image_url,
                'followers_count': followers_count,
                'status': 'queued'
            }
            
            result = self.supabase.table('tweet_queue').insert(queue_data).execute()
            
            if result.data:
                self.log(f"  → Added to queue: {ticker} from tweet {tweet.id}")
                self.processed_tweets.add(str(tweet.id))
                return True
                
        except Exception as e:
            self.log(f"  → Error adding to queue: {e}")
            return False
    
    def add_to_queue_rejected(self, tweet, ticker, author, followers_count):
        """Add rejected tweet to queue"""
        try:
            tweet_url = f"https://twitter.com/{author}/status/{tweet.id}"
            
            queue_data = {
                'tweet_id': str(tweet.id),
                'twitter_user': author,
                'ticker': ticker,
                'name': ticker,
                'description': 'Bu token memeXshot aracılığı ile Moonshot\'ta create edildi',
                'website': tweet_url,
                'twitter': f"@{author}",
                'image_url': 'NO_IMAGE',
                'followers_count': followers_count,
                'status': 'rejected',
                'error_message': f'Insufficient followers: {followers_count} (min: {self.min_followers})'
            }
            
            self.supabase.table('tweet_queue').insert(queue_data).execute()
            self.log(f"  → Added to queue as REJECTED")
            
        except Exception as e:
            self.log(f"  → Error adding rejected tweet: {e}")
    
    def simulate_bot_search(self, tweets):
        """Simulate the bot searching and processing tweets"""
        self.log("\n🔍 Bot searching for tweets...")
        self.log(f"Query: \"Launch\" \"@{self.bot_username}\" -is:retweet has:images")
        
        time.sleep(1)  # Simulate search delay
        
        self.log(f"\n📊 Found {len(tweets)} tweets to process")
        
        processed = 0
        rejected = 0
        
        for i, tweet in enumerate(tweets):
            self.log(f"\n--- Processing Tweet {i+1}/{len(tweets)} ---")
            self.log(f"ID: {tweet.id}")
            self.log(f"Text: '{tweet.text}'")
            
            if self.process_tweet(tweet):
                processed += 1
            else:
                rejected += 1
            
            time.sleep(0.5)  # Simulate processing delay
        
        return processed, rejected
    
    def show_database_results(self):
        """Show what was added to the database"""
        self.log("\n📋 DATABASE RESULTS")
        self.log("=" * 60)
        
        try:
            # Get queued items
            queued = self.supabase.table('tweet_queue')\
                .select('*')\
                .eq('status', 'queued')\
                .execute()
            
            # Get rejected items  
            rejected = self.supabase.table('tweet_queue')\
                .select('*')\
                .eq('status', 'rejected')\
                .execute()
            
            self.log(f"\n✅ QUEUED FOR PROCESSING: {len(queued.data)}")
            for item in queued.data:
                self.log(f"  • ${item['ticker']} from @{item['twitter_user']} ({item['followers_count']} followers)")
            
            self.log(f"\n❌ REJECTED: {len(rejected.data)}")
            for item in rejected.data:
                self.log(f"  • ${item['ticker']} from @{item['twitter_user']} - {item['error_message']}")
            
        except Exception as e:
            self.log(f"Error reading database: {e}")
    
    def cleanup_test_data(self):
        """Clean up test data from database"""
        self.log("\n🧹 Cleaning up test data...")
        
        try:
            # Delete all test tweets (ID starts with 100)
            for tweet_id in self.processed_tweets:
                self.supabase.table('tweet_queue')\
                    .delete()\
                    .eq('tweet_id', tweet_id)\
                    .execute()
            
            self.log(f"✅ Cleaned up {len(self.processed_tweets)} test entries")
            
        except Exception as e:
            self.log(f"⚠️  Error during cleanup: {e}")
    
    def run_integration_test(self):
        """Run the complete integration test"""
        self.log("\n" + "🚀 TWITTER BOT INTEGRATION TEST 🚀".center(60, "="))
        self.log("Testing complete flow: Tweet → Bot → Database")
        self.log("=" * 60)
        
        # Generate mock tweets
        tweets = self.generate_mock_tweets()
        
        # Simulate bot processing
        processed, rejected = self.simulate_bot_search(tweets)
        
        # Show results
        self.log(f"\n📈 PROCESSING SUMMARY")
        self.log(f"Total tweets: {len(tweets)}")
        self.log(f"Processed successfully: {processed}")
        self.log(f"Rejected: {rejected}")
        
        # Show database state
        self.show_database_results()
        
        # Ask to cleanup
        self.log("\n" + "=" * 60)
        response = input("Clean up test data from database? (y/n): ")
        if response.lower() == 'y':
            self.cleanup_test_data()
        else:
            self.log("⚠️  Test data left in database for inspection")
        
        self.log("\n✅ Integration test completed!")

if __name__ == "__main__":
    tester = IntegrationTester()
    tester.run_integration_test()