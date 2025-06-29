#!/usr/bin/env python3
"""
Twitter Bot Logic Test Suite
Tests bot parsing and processing logic without real API calls
"""

import os
import sys
import re
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MockTweet:
    """Mock tweet object for testing"""
    def __init__(self, id, text, author_id, author_username, followers_count, has_image=True):
        self.id = id
        self.text = text
        self.author_id = author_id
        self.created_at = datetime.now()
        self.attachments = {'media_keys': ['mock_media']} if has_image else None
        
        # Mock author data
        self.author = MockUser(author_id, author_username, followers_count)

class MockUser:
    """Mock user object for testing"""
    def __init__(self, id, username, followers_count):
        self.id = id
        self.username = username
        self.public_metrics = {
            'followers_count': followers_count,
            'following_count': 100,
            'tweet_count': 50
        }

class TwitterBotLogicTester:
    def __init__(self):
        self.bot_username = 'memeXshot'
        self.min_followers = 500
        self.results = []
    
    def log_test(self, category, test_case, expected, actual, passed):
        """Log test results"""
        status = "✅" if passed else "❌"
        self.results.append({
            'category': category,
            'test': test_case,
            'passed': passed
        })
        
        print(f"{status} {test_case}")
        print(f"   Expected: {expected}")
        print(f"   Actual: {actual}")
        if not passed:
            print("   ^ MISMATCH ^")
        print()
    
    def parse_tweet(self, tweet_text):
        """Parse tweet for Launch command (from actual bot logic)"""
        # Remove extra spaces and newlines
        text = ' '.join(tweet_text.split())
        
        # Pattern to match: Launch TICKER @memeXshot
        pattern = rf'Launch\s+\$?([A-Za-z0-9]+)\s+@{self.bot_username}'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            ticker = match.group(1).upper()
            # Validate ticker (3-10 characters)
            if 3 <= len(ticker) <= 10:
                return ticker
        
        return None
    
    def test_tweet_parsing(self):
        """Test tweet text parsing logic"""
        print("=" * 60)
        print("TEST: Tweet Parsing Logic")
        print("=" * 60 + "\n")
        
        test_cases = [
            # Format: (tweet_text, expected_ticker)
            ("Launch $MOON @memeXshot", "MOON"),
            ("Launch $BTC @memeXshot with some extra text", "BTC"),
            ("launch $doge @memeXshot", "DOGE"),  # Case insensitive
            ("Launch PEPE @memeXshot", "PEPE"),  # Without $
            ("LAUNCH $ETH @MEMEXSHOT", "ETH"),  # All caps
            ("  Launch    $SHIB    @memeXshot  ", "SHIB"),  # Extra spaces
            ("Launch $MOON@memeXshot", None),  # No space before @
            ("Launch $AB @memeXshot", None),  # Too short
            ("Launch $VERYLONGTOKEN @memeXshot", None),  # Too long
            ("Buy $MOON @memeXshot", None),  # Wrong keyword
            ("Launch $MOON @wrongbot", None),  # Wrong bot
            ("RT: Launch $MOON @memeXshot", "MOON"),  # Retweet text
            ("Launch $123 @memeXshot", "123"),  # Numbers allowed
            ("Launch $TEST123 @memeXshot", "TEST123"),  # Alphanumeric
        ]
        
        for tweet_text, expected in test_cases:
            result = self.parse_tweet(tweet_text)
            passed = result == expected
            self.log_test(
                "Parsing",
                tweet_text,
                f"${expected}" if expected else "None",
                f"${result}" if result else "None",
                passed
            )
    
    def test_follower_validation(self):
        """Test follower count validation"""
        print("\n" + "=" * 60)
        print("TEST: Follower Validation")
        print("=" * 60 + "\n")
        
        test_cases = [
            # Format: (followers_count, should_process)
            (1000, True),    # Above minimum
            (500, True),     # Exactly minimum
            (499, False),    # Just below minimum
            (100, False),    # Well below minimum
            (0, False),      # No followers
            (50000, True),   # High follower count
        ]
        
        for followers, should_process in test_cases:
            # Simulate follower check
            passed_check = followers >= self.min_followers
            passed = passed_check == should_process
            
            self.log_test(
                "Followers",
                f"User with {followers} followers",
                "Process" if should_process else "Reject",
                "Process" if passed_check else "Reject",
                passed
            )
    
    def test_mock_tweet_processing(self):
        """Test complete tweet processing flow with mock data"""
        print("\n" + "=" * 60)
        print("TEST: Mock Tweet Processing")
        print("=" * 60 + "\n")
        
        # Create mock tweets
        mock_tweets = [
            MockTweet(
                "1001", 
                "Launch $MOON @memeXshot", 
                "user1", 
                "cryptowhale", 
                5000, 
                has_image=True
            ),
            MockTweet(
                "1002", 
                "Launch $PEPE @memeXshot", 
                "user2", 
                "smalltrader", 
                100,  # Too few followers
                has_image=True
            ),
            MockTweet(
                "1003", 
                "Launch $DOGE @memeXshot", 
                "user3", 
                "normaluser", 
                750,
                has_image=False  # No image
            ),
            MockTweet(
                "1004", 
                "Check out $BTC @memeXshot", 
                "user4", 
                "wrongformat", 
                1000,
                has_image=True
            ),
        ]
        
        for tweet in mock_tweets:
            print(f"Processing Tweet ID: {tweet.id}")
            print(f"From: @{tweet.author.username} ({tweet.author.public_metrics['followers_count']} followers)")
            print(f"Text: '{tweet.text}'")
            print(f"Has Image: {tweet.attachments is not None}")
            
            # Parse ticker
            ticker = self.parse_tweet(tweet.text)
            
            # Check all conditions
            conditions = {
                "Valid format": ticker is not None,
                "Has image": tweet.attachments is not None,
                "Enough followers": tweet.author.public_metrics['followers_count'] >= self.min_followers
            }
            
            should_process = all(conditions.values())
            
            print("Checks:")
            for check, passed in conditions.items():
                print(f"  {'✅' if passed else '❌'} {check}")
            
            print(f"Result: {'✅ PROCESS' if should_process else '❌ REJECT'}")
            
            if should_process:
                print(f"  → Would add ${ticker} to queue")
            else:
                fail_reasons = [check for check, passed in conditions.items() if not passed]
                print(f"  → Rejected due to: {', '.join(fail_reasons)}")
            
            print("-" * 40 + "\n")
    
    def test_rate_limit_logic(self):
        """Test rate limiting logic"""
        print("=" * 60)
        print("TEST: Rate Limit Logic")
        print("=" * 60 + "\n")
        
        # Simulate user posting history
        user_posts = {
            "user1": {"posts_today": 2, "last_post": "2024-01-01 10:00"},
            "user2": {"posts_today": 3, "last_post": "2024-01-01 11:00"},  # At limit
            "user3": {"posts_today": 0, "last_post": None},  # New user
        }
        
        max_daily = 3
        
        for username, data in user_posts.items():
            can_post = data["posts_today"] < max_daily
            
            print(f"User: @{username}")
            print(f"Posts today: {data['posts_today']}/{max_daily}")
            print(f"Can post: {'✅ Yes' if can_post else '❌ No (limit reached)'}")
            
            if can_post:
                print(f"  → Would allow token creation")
            else:
                print(f"  → Would reject with rate limit message")
            
            print("-" * 40 + "\n")
    
    def run_all_tests(self):
        """Run all logic tests"""
        print("\n" + "🧪 TWITTER BOT LOGIC TEST SUITE 🧪".center(60, "="))
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60 + "\n")
        
        # Run all test categories
        self.test_tweet_parsing()
        self.test_follower_validation()
        self.test_mock_tweet_processing()
        self.test_rate_limit_logic()
        
        # Summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        
        # Group by category
        categories = {}
        for r in self.results:
            cat = r['category']
            if cat not in categories:
                categories[cat] = {'passed': 0, 'failed': 0}
            if r['passed']:
                categories[cat]['passed'] += 1
            else:
                categories[cat]['failed'] += 1
        
        print("\nBy Category:")
        for cat, stats in categories.items():
            print(f"  {cat}: {stats['passed']} passed, {stats['failed']} failed")
        
        if failed == 0:
            print("\n🎉 All logic tests passed!")
        else:
            print("\n⚠️  Some tests failed. Check the implementation.")

if __name__ == "__main__":
    tester = TwitterBotLogicTester()
    tester.run_all_tests()