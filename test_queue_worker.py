#!/usr/bin/env python3
"""Test Queue Worker"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.queue_worker import QueueWorker

# Test queue worker
worker = QueueWorker()

print("Testing Queue Worker...")
print("="*50)

# Check if system is busy
busy = worker.has_active_processing()
print(f"System busy: {busy}")

# Get next tweet
next_tweet = worker.get_next_tweet()
if next_tweet:
    print(f"\nNext tweet: {next_tweet['ticker']} from @{next_tweet['twitter_user']}")
    print(f"Status: {next_tweet['status']}")
    print(f"Followers: {next_tweet['followers_count']}")
else:
    print("\nNo tweets in queue")

print("\nTrying to process...")
if next_tweet and not busy:
    success = worker.move_to_coins(next_tweet)
    print(f"Move to coins: {'Success' if success else 'Failed'}")