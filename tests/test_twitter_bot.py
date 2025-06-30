#!/usr/bin/env python3
"""
Test Twitter Bot Service
Tests API connection, authentication, and search functionality
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.services.twitter_bot import TwitterBot
import tweepy

def test_twitter_credentials():
    """Test if Twitter credentials are properly loaded"""
    print("🔍 Testing Twitter Credentials...")
    
    # Check environment variables
    required_vars = [
        'TWITTER_BEARER_TOKEN',
        'TWITTER_API_KEY', 
        'TWITTER_API_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
        else:
            print(f"✅ {var}: Found")
    
    if missing:
        print(f"❌ Missing credentials: {missing}")
        return False
    
    print("✅ All credentials found!")
    return True

def test_twitter_api_connection():
    """Test Twitter API v2 connection"""
    print("\n🔍 Testing Twitter API Connection...")
    
    try:
        # Create client with v2 API
        client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        
        # Test with get_me() to verify credentials
        me = client.get_me()
        if me and me.data:
            print(f"✅ Connected as: @{me.data.username} (ID: {me.data.id})")
            return True
        else:
            print("❌ Could not verify credentials")
            return False
            
    except Exception as e:
        print(f"❌ API Connection Error: {e}")
        return False

def test_search_tweets():
    """Test searching for tweets (without processing)"""
    print("\n🔍 Testing Tweet Search...")
    
    try:
        client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            wait_on_rate_limit=True
        )
        
        # Search for recent tweets mentioning the bot
        bot_username = os.getenv('BOT_USERNAME', 'memeXshot')
        query = f"@{bot_username} Launch"
        
        print(f"📝 Search query: '{query}'")
        
        # Search for tweets (max 10 for testing)
        tweets = client.search_recent_tweets(
            query=query,
            max_results=10,
            tweet_fields=['created_at', 'author_id', 'text']
        )
        
        if tweets and tweets.data:
            print(f"✅ Found {len(tweets.data)} tweets")
            for i, tweet in enumerate(tweets.data[:3], 1):  # Show first 3
                print(f"\n   Tweet {i}:")
                print(f"   Text: {tweet.text[:100]}...")
                print(f"   ID: {tweet.id}")
        else:
            print("✅ No tweets found (this is OK for testing)")
            
        return True
        
    except Exception as e:
        print(f"❌ Search Error: {e}")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🔍 Testing Supabase Connection...")
    
    try:
        from supabase import create_client
        
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            print("❌ Missing Supabase credentials")
            return False
            
        # Create client
        supabase = create_client(url, key)
        
        # Test with a simple query
        result = supabase.table('coins').select('id').limit(1).execute()
        print("✅ Supabase connection successful!")
        
        # Check tables
        tables = ['coins', 'tweet_queue', 'twitter_rate_limits']
        for table in tables:
            try:
                result = supabase.table(table).select('*').limit(1).execute()
                print(f"✅ Table '{table}' accessible")
            except Exception as e:
                print(f"⚠️  Table '{table}' error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase Error: {e}")
        return False

def test_twitter_bot_initialization():
    """Test TwitterBot class initialization"""
    print("\n🔍 Testing TwitterBot Initialization...")
    
    try:
        bot = TwitterBot()
        print("✅ TwitterBot initialized successfully!")
        
        # Check attributes
        print(f"   Bot Username: @{bot.bot_username}")
        print(f"   Search Keyword: {bot.search_keyword}")
        print(f"   Daily Limit: {bot.max_daily_per_user}")
        print(f"   Min Followers: {bot.min_followers}")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 TWITTER BOT TEST SUITE")
    print("=" * 50)
    print("⚠️  Running in TEST MODE - No tweets will be processed")
    print("=" * 50)
    
    tests = [
        ("Credentials", test_twitter_credentials),
        ("API Connection", test_twitter_api_connection),
        ("Tweet Search", test_search_tweets),
        ("Supabase", test_supabase_connection),
        ("Bot Init", test_twitter_bot_initialization)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*50}")
        success = test_func()
        results.append((name, success))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY:")
    print("="*50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Twitter Bot is ready to run.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()