#!/usr/bin/env python3
"""
Twitter Bot Service for memeXshot
Monitors tweets with "Launch $ticker @memeXshot" format
"""

import os
import sys
import time
import re
import tweepy
from datetime import datetime
from dotenv import load_dotenv

# Add moonshot_automation root directory to path (go up 2 levels from scripts/services/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from supabase import create_client
from config.supabase_config import SUPABASE_URL, SUPABASE_KEY

# Load environment variables
load_dotenv()

class TwitterBot:
    def __init__(self):
        # Initialize Supabase
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Twitter credentials
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        # Bot config
        self.bot_username = os.getenv('BOT_USERNAME', 'memeXshot')
        self.search_keyword = os.getenv('SEARCH_KEYWORD', 'Launch')
        self.max_daily_per_user = int(os.getenv('MAX_DAILY_PER_USER', '3'))  # Daily limit per user
        self.min_followers = int(os.getenv('MIN_FOLLOWERS', '0'))  # Minimum follower requirement
        
        # Coin creation config
        self.coin_twitter_handle = os.getenv('COIN_TWITTER_HANDLE', '@memexshot')
        self.coin_website_type = os.getenv('COIN_WEBSITE_URL', 'tweet_url')
        
        # Initialize Twitter client
        self.client = self.setup_twitter_client()
        
        # Track processed tweets
        self.processed_tweets = set()
        self.load_processed_tweets()
        
        # Track last seen tweet ID for pagination
        self.last_seen_id = None
        self.load_last_seen_id()
        
    def setup_twitter_client(self):
        """Setup Twitter API v2 client"""
        try:
            client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            
            # Test connection
            me = client.get_me()
            if me.data:
                self.log(f"✅ Connected to Twitter as @{me.data.username}")
            
            return client
            
        except Exception as e:
            self.log(f"❌ Failed to setup Twitter client: {e}")
            sys.exit(1)
    
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def load_processed_tweets(self):
        """Load already processed tweet IDs from database"""
        try:
            result = self.supabase.table('tweet_queue')\
                .select('tweet_id')\
                .execute()
            
            for record in result.data:
                self.processed_tweets.add(record['tweet_id'])
                
            self.log(f"📋 Loaded {len(self.processed_tweets)} processed tweets")
            
        except Exception as e:
            self.log(f"⚠️  Error loading processed tweets: {e}")
    
    def load_last_seen_id(self):
        """Load last seen tweet ID from database"""
        try:
            # Get the most recent tweet from queue
            result = self.supabase.table('tweet_queue')\
                .select('tweet_id')\
                .order('created_at', desc=True)\
                .limit(1)\
                .execute()
            
            if result.data:
                self.last_seen_id = result.data[0]['tweet_id']
                self.log(f"📍 Last seen tweet ID: {self.last_seen_id}")
            else:
                self.log("📍 No previous tweets found, starting fresh")
                
        except Exception as e:
            self.log(f"⚠️  Error loading last seen ID: {e}")
    
    def parse_tweet(self, tweet_text):
        """Parse tweet for Launch command
        Format: Launch $TICKER @memeXshot
        """
        # Remove extra spaces and newlines
        text = ' '.join(tweet_text.split())
        
        # Pattern to match: @memeXshot KEYWORD $TICKER or KEYWORD $TICKER @memeXshot
        # Try both patterns
        pattern1 = rf'@{self.bot_username}\s+{self.search_keyword}\s+\$?([A-Za-z0-9]+)'
        pattern2 = rf'{self.search_keyword}\s+\$?([A-Za-z0-9]+)\s+@{self.bot_username}'
        # Try first pattern: @memeXshot KEYWORD $TICKER
        match = re.search(pattern1, text, re.IGNORECASE)
        
        # If not found, try second pattern: KEYWORD $TICKER @memeXshot
        if not match:
            match = re.search(pattern2, text, re.IGNORECASE)
        
        if match:
            ticker = match.group(1).upper()
            # Validate ticker (3-10 characters)
            if 3 <= len(ticker) <= 10:
                return ticker
        
        return None
    
    def get_tweet_image(self, tweet, includes=None):
        """Extract image URL from tweet"""
        try:
            # Check if tweet has media
            if hasattr(tweet, 'attachments') and tweet.attachments:
                media_keys = tweet.attachments.get('media_keys', [])
                
                if media_keys and includes and 'media' in includes:
                    for media in includes['media']:
                        if media.media_key in media_keys and media.type == 'photo':
                            return media.url
            
            return None
            
        except Exception as e:
            self.log(f"⚠️  Error extracting image: {e}")
            return None
    
    def check_rate_limit(self, username):
        """Check if user has reached daily limit"""
        try:
            # Call Supabase function
            result = self.supabase.rpc('check_rate_limit', {'username': username}).execute()
            return result.data if result.data is not None else False
            
        except Exception as e:
            self.log(f"⚠️  Error checking rate limit: {e}")
            return False
    
    def add_to_queue(self, tweet, ticker, author=None, followers_count=0, includes=None, profile_image_url=None, name=None):
        """Add tweet to processing queue"""
        try:
            # Get tweet URL
            tweet_url = f"https://twitter.com/{author or tweet.author_id}/status/{tweet.id}"
            
            # Get image URL
            image_url = self.get_tweet_image(tweet, includes)
            
            if not image_url:
                self.log(f"⚠️  No image found in tweet {tweet.id}")
                return False
            
            # Production data
            queue_data = {
                'tweet_id': str(tweet.id),
                'twitter_user': author or tweet.author_id,
                'ticker': ticker,
                'name': name or ticker,  # Use Twitter display name or ticker
                'description': 'This coin was created via memeXshot',
                'website': tweet_url if self.coin_website_type == 'tweet_url' else self.coin_website_type,
                'twitter': self.coin_twitter_handle,
                'image_url': image_url,
                'profile_image_url': profile_image_url,
                'followers_count': followers_count,
                'status': 'queued'
            }
            
            # Insert to queue
            result = self.supabase.table('tweet_queue').insert(queue_data).execute()
            
            if result.data:
                self.log(f"✅ Added to queue: {ticker} from tweet {tweet.id}")
                self.processed_tweets.add(str(tweet.id))
                
                # Update rate limit
                self.supabase.table('twitter_rate_limits')\
                    .upsert({
                        'twitter_user': tweet.author_id,
                        'daily_count': 1,
                        'total_tokens': 1
                    }, on_conflict='twitter_user')\
                    .execute()
                
                return True
            
        except Exception as e:
            self.log(f"❌ Error adding to queue: {e}")
            return False
    
    def add_to_queue_rejected(self, tweet, ticker, author, followers_count, profile_image_url=None, name=None):
        """Add tweet to queue with rejected status (insufficient followers)"""
        try:
            tweet_url = f"https://twitter.com/{author}/status/{tweet.id}"
            image_url = self.get_tweet_image(tweet, None)
            
            # Production data for rejected tweets
            queue_data = {
                'tweet_id': str(tweet.id),
                'twitter_user': author,
                'ticker': ticker,
                'name': name or ticker,
                'description': 'This coin was created via memeXshot',
                'website': tweet_url if self.coin_website_type == 'tweet_url' else self.coin_website_type,
                'twitter': self.coin_twitter_handle,
                'image_url': image_url or 'NO_IMAGE',
                'profile_image_url': profile_image_url,
                'followers_count': followers_count,
                'status': 'rejected',
                'error_message': f'Insufficient followers: {followers_count} (min: {self.min_followers})'
            }
            
            self.supabase.table('tweet_queue').insert(queue_data).execute()
            self.log(f"📝 Added to queue as rejected: {ticker} from @{author}")
            
        except Exception as e:
            self.log(f"⚠️  Error adding rejected tweet: {e}")
    
    def search_tweets(self):
        """Search for new Launch tweets using optimized parameters"""
        try:
            # Production search query - @username first, then keyword
            query = f'@{self.bot_username} {self.search_keyword} -is:retweet has:images'
            self.log(f"🔎 Searching with query: {query}")
            
            # Search parameters
            search_params = {
                'query': query,
                'max_results': 25,  # Get last 25 tweets
                'tweet_fields': ['created_at', 'author_id', 'attachments'],
                'expansions': ['attachments.media_keys', 'author_id'],
                'media_fields': ['url', 'type'],
                'user_fields': ['username', 'public_metrics', 'profile_image_url', 'name']
            }
            
            # Add since_id if we have a last seen ID
            if self.last_seen_id:
                search_params['since_id'] = self.last_seen_id
                self.log(f"🔍 Searching for tweets newer than {self.last_seen_id}")
            
            # Search tweets
            tweets = self.client.search_recent_tweets(**search_params)
            
            if not tweets.data:
                self.log("📭 No new tweets found in this search")
                return
            
            self.log(f"🔍 Found {len(tweets.data)} new tweets")
            
            # Update last seen ID to the newest tweet
            if tweets.data:
                newest_id = tweets.data[0].id
                self.last_seen_id = str(newest_id)
                self.log(f"📍 Updated last seen ID: {self.last_seen_id}")
            
            # Process each tweet (in reverse order - oldest first)
            for tweet in reversed(tweets.data):
                # Skip if already processed
                if str(tweet.id) in self.processed_tweets:
                    continue
                
                # Parse ticker
                ticker = self.parse_tweet(tweet.text)
                if not ticker:
                    self.log(f"⚠️  Invalid format in tweet {tweet.id}")
                    continue
                
                # Get author info
                author = None
                followers_count = 0
                profile_image_url = None
                name = None
                if hasattr(tweets, 'includes') and 'users' in tweets.includes:
                    for user in tweets.includes['users']:
                        if user.id == tweet.author_id:
                            author = user.username
                            followers_count = user.public_metrics.get('followers_count', 0)
                            profile_image_url = getattr(user, 'profile_image_url', None)
                            name = getattr(user, 'name', None)
                            break
                
                if not author:
                    self.log(f"⚠️  Could not find author for tweet {tweet.id}")
                    continue
                
                # Check minimum followers
                if followers_count < self.min_followers:
                    self.log(f"❌ @{author} has only {followers_count} followers (min: {self.min_followers})")
                    self.processed_tweets.add(str(tweet.id))
                    # Still add to queue but with rejected status
                    self.add_to_queue_rejected(tweet, ticker, author, followers_count, profile_image_url, name)
                    continue
                
                # Check rate limit
                if not self.check_rate_limit(author):
                    self.log(f"⏳ Rate limit reached for @{author}")
                    self.processed_tweets.add(str(tweet.id))
                    continue
                
                # Add to queue with user info and includes
                self.add_to_queue(tweet, ticker, author, followers_count, 
                                tweets.includes if hasattr(tweets, 'includes') else None,
                                profile_image_url, name)
                
        except Exception as e:
            self.log(f"❌ Error searching tweets: {e}")
    
    def run(self):
        """Main bot loop"""
        self.log("🚀 Starting Twitter Bot")
        self.log(f"🔍 Monitoring for: @{self.bot_username} {self.search_keyword} $TICKER")
        self.log(f"⚡ Rate limit: {self.max_daily_per_user} per user per day")
        
        while True:
            try:
                # Search for new tweets
                self.search_tweets()
                
                # Wait before next search (30 seconds)
                self.log("💤 Waiting 30 seconds before next search...")
                time.sleep(30)  # 30 seconds
                
            except KeyboardInterrupt:
                self.log("👋 Stopping bot...")
                break
            except Exception as e:
                self.log(f"❌ Unexpected error: {e}")
                time.sleep(60)  # Wait 1 minute on error

if __name__ == "__main__":
    # Check for required environment variables
    required_vars = ['TWITTER_BEARER_TOKEN', 'TWITTER_API_KEY', 'TWITTER_API_SECRET']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("Please update your .env file with Twitter API credentials")
        sys.exit(1)
    
    bot = TwitterBot()
    bot.run()