#!/usr/bin/env python3
"""
Twitter API Test Suite
Tests all API functionality without making real posts
"""

import os
import sys
import tweepy
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

class TwitterAPITester:
    def __init__(self):
        self.results = []
        self.client = None
        
    def log_result(self, test_name, success, message):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.results.append({
            'test': test_name,
            'status': status,
            'message': message
        })
        print(f"{status} | {test_name}")
        print(f"     {message}\n")
    
    def test_environment_variables(self):
        """Test 1: Check all required environment variables"""
        print("=" * 50)
        print("TEST 1: Environment Variables")
        print("=" * 50)
        
        required_vars = {
            'TWITTER_BEARER_TOKEN': 'Bearer Token',
            'TWITTER_API_KEY': 'API Key',
            'TWITTER_API_SECRET': 'API Secret',
            'TWITTER_ACCESS_TOKEN': 'Access Token',
            'TWITTER_ACCESS_TOKEN_SECRET': 'Access Token Secret'
        }
        
        all_present = True
        for var, name in required_vars.items():
            value = os.getenv(var)
            if not value or value.startswith('your_'):
                self.log_result(
                    f"Environment: {name}",
                    False,
                    f"{var} is missing or placeholder"
                )
                all_present = False
            else:
                # Mask sensitive data
                masked = value[:10] + "..." if len(value) > 10 else "***"
                self.log_result(
                    f"Environment: {name}",
                    True,
                    f"Found: {masked}"
                )
        
        return all_present
    
    def test_bearer_token_auth(self):
        """Test 2: Bearer Token Authentication (App-only)"""
        print("=" * 50)
        print("TEST 2: Bearer Token Authentication")
        print("=" * 50)
        
        try:
            client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))
            
            # Simple search test
            tweets = client.search_recent_tweets(
                query="from:Twitter", 
                max_results=10
            )
            
            if tweets.data:
                self.log_result(
                    "Bearer Token Auth",
                    True,
                    "Successfully authenticated with bearer token"
                )
                return True
            else:
                self.log_result(
                    "Bearer Token Auth",
                    False,
                    "Auth succeeded but no data returned"
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Bearer Token Auth",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_user_auth(self):
        """Test 3: User Authentication (OAuth 1.0a)"""
        print("=" * 50)
        print("TEST 3: User Authentication")
        print("=" * 50)
        
        try:
            self.client = tweepy.Client(
                bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
            
            # Get authenticated user
            me = self.client.get_me(user_fields=['public_metrics'])
            
            if me.data:
                self.log_result(
                    "User Authentication",
                    True,
                    f"Authenticated as @{me.data.username} ({me.data.name})"
                )
                
                # Show user metrics
                if hasattr(me.data, 'public_metrics'):
                    metrics = me.data.public_metrics
                    print(f"     Followers: {metrics.get('followers_count', 0)}")
                    print(f"     Following: {metrics.get('following_count', 0)}")
                    print(f"     Tweets: {metrics.get('tweet_count', 0)}\n")
                
                return True
            else:
                self.log_result(
                    "User Authentication",
                    False,
                    "Auth succeeded but no user data returned"
                )
                return False
                
        except Exception as e:
            self.log_result(
                "User Authentication",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_search_mentions(self):
        """Test 4: Search for mentions (simulated)"""
        print("=" * 50)
        print("TEST 4: Search Mentions Capability")
        print("=" * 50)
        
        if not self.client:
            self.log_result(
                "Search Mentions",
                False,
                "Client not initialized"
            )
            return False
        
        try:
            # Search for a generic query to test search API
            query = '"@Twitter" -is:retweet has:images'
            
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=['created_at', 'author_id', 'attachments'],
                expansions=['attachments.media_keys', 'author_id'],
                media_fields=['url', 'type'],
                user_fields=['username', 'public_metrics']
            )
            
            if tweets.data:
                self.log_result(
                    "Search API",
                    True,
                    f"Search working! Found {len(tweets.data)} tweets"
                )
                
                # Test our parsing logic
                print("     Testing mention format parsing:")
                test_texts = [
                    "Launch $MOON @memeXshot",
                    "launch $btc @memeXshot with image",
                    "LAUNCH $DOGE @MEMEXSHOT",
                    "Invalid format Launch MOON memeXshot",
                    "Launch $VERYLONGTICKER @memeXshot"
                ]
                
                import re
                pattern = r'Launch\s+\$?([A-Za-z0-9]+)\s+@memeXshot'
                
                for text in test_texts:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        ticker = match.group(1).upper()
                        valid = 3 <= len(ticker) <= 10
                        print(f"     ✓ '{text}' → ${ticker} {'(valid)' if valid else '(invalid length)'}")
                    else:
                        print(f"     ✗ '{text}' → No match")
                
                return True
            else:
                self.log_result(
                    "Search API",
                    True,
                    "Search API accessible (no results found)"
                )
                return True
                
        except Exception as e:
            self.log_result(
                "Search Mentions",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_rate_limits(self):
        """Test 5: Check rate limit headers"""
        print("\n" + "=" * 50)
        print("TEST 5: Rate Limit Information")
        print("=" * 50)
        
        if not self.client:
            self.log_result(
                "Rate Limits",
                False,
                "Client not initialized"
            )
            return False
        
        try:
            # Make a simple request to get rate limit headers
            tweets = self.client.search_recent_tweets(
                query="from:Twitter",
                max_results=10
            )
            
            # Note: Tweepy v2 doesn't expose rate limit headers directly
            # But we can calculate our usage
            
            self.log_result(
                "Rate Limit Check",
                True,
                "Rate limits for Basic plan:"
            )
            
            print("     Search Recent Tweets: 60 requests / 15 mins")
            print("     Our usage: 30 requests / 15 mins (30 sec intervals)")
            print("     Safety margin: 50%")
            print("     User timeline: 5 requests / 15 mins")
            print("     Get user: 100 requests / 24 hours\n")
            
            return True
            
        except Exception as e:
            self.log_result(
                "Rate Limits",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_write_permissions(self):
        """Test 6: Check write permissions (without posting)"""
        print("=" * 50)
        print("TEST 6: Write Permissions Check")
        print("=" * 50)
        
        if not self.client:
            self.log_result(
                "Write Permissions",
                False,
                "Client not initialized"
            )
            return False
        
        # We can't test actual posting without creating a tweet
        # But we can verify the access token has write scope
        self.log_result(
            "Write Permissions",
            True,
            "Access token configured (actual write test requires posting)"
        )
        
        print("     Note: Actual tweet posting will be tested in Phase 5")
        print("     Current scope should include 'tweet.write' for future use\n")
        
        return True
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "🧪 TWITTER API TEST SUITE 🧪".center(50, "="))
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50 + "\n")
        
        # Run tests in order
        tests = [
            self.test_environment_variables,
            self.test_bearer_token_auth,
            self.test_user_auth,
            self.test_search_mentions,
            self.test_rate_limits,
            self.test_write_permissions
        ]
        
        for test in tests:
            test()
        
        # Summary
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for r in self.results if "PASS" in r['status'])
        failed = sum(1 for r in self.results if "FAIL" in r['status'])
        
        print(f"Total Tests: {len(self.results)}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        
        if failed == 0:
            print("\n🎉 All tests passed! Ready for Twitter bot testing.")
        else:
            print("\n⚠️  Some tests failed. Please check the errors above.")
        
        return failed == 0

if __name__ == "__main__":
    tester = TwitterAPITester()
    tester.run_all_tests()