#!/usr/bin/env python3
"""
Debug script to check system status
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client
from config.supabase_config import SUPABASE_URL, SUPABASE_KEY

def check_system():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("🔍 SYSTEM STATUS CHECK")
    print("="*50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Check tweet_queue
    print("\n📋 TWEET QUEUE:")
    queue = supabase.table('tweet_queue').select('*').order('created_at', desc=True).limit(5).execute()
    if queue.data:
        for item in queue.data:
            print(f"  • {item['ticker']} from @{item['twitter_user']} - Status: {item['status']}")
            print(f"    Tweet ID: {item['tweet_id']}")
            print(f"    Created: {item['created_at']}")
    else:
        print("  ❌ No tweets in queue")
    
    # Check coins table
    print("\n💰 COINS TABLE:")
    coins = supabase.table('coins').select('*').order('created_at', desc=True).limit(5).execute()
    if coins.data:
        for coin in coins.data:
            print(f"  • {coin['ticker']} - Status: {coin['status']}, Image Synced: {coin['image_synced']}")
            print(f"    Created: {coin['created_at']}")
    else:
        print("  ❌ No coins in table")
    
    # Check Twitter bot search
    print("\n🐦 TWITTER BOT TEST:")
    print("  Search pattern: 'Perfecto' '@memeXshot' -is:retweet has:images")
    print("  Min followers: 0 (disabled for test)")
    
    # Test tweet parsing
    from services.twitter_bot import TwitterBot
    bot = TwitterBot()
    test_tweets = [
        "Perfecto $LABALUBA @memeXshot",
        "perfecto $test @memexshot",
        "Perfecto $MOON @memeXshot to the moon!"
    ]
    
    print("\n  Testing tweet parsing:")
    for text in test_tweets:
        ticker = bot.parse_tweet(text)
        print(f"    '{text}' → {f'${ticker}' if ticker else 'NO MATCH'}")

if __name__ == "__main__":
    check_system()