#!/usr/bin/env python3
"""
Full Integration Test - Complete Flow Simulation
Tests: Twitter Bot → Queue → Queue Worker → Coins Table → Photo Sync → Automation
"""

import os
import sys
import time
import random
import threading
from datetime import datetime
from uuid import uuid4

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase import create_client
from config.supabase_config import SUPABASE_URL, SUPABASE_KEY

class MockTweet:
    """Mock tweet for testing"""
    def __init__(self, id, ticker, author_username, followers_count):
        self.id = str(id)
        self.text = f"Launch ${ticker} @memeXshot to the moon! 🚀"
        self.author_id = f"user_{id}"
        self.created_at = datetime.now()
        self.attachments = {'media_keys': [f'media_{id}']}
        
        # Mock includes data
        self.includes = {
            'users': [{
                'id': self.author_id,
                'username': author_username,
                'name': f"{author_username} User",
                'public_metrics': {
                    'followers_count': followers_count
                }
            }],
            'media': [{
                'media_key': f'media_{id}',
                'type': 'photo',
                'url': f'https://pbs.twimg.com/media/test_image_{ticker}.jpg'
            }]
        }

class MockQueueWorker:
    """Simulated Queue Worker"""
    def __init__(self, supabase):
        self.supabase = supabase
        self.running = False
        
    def log(self, message):
        print(f"[Queue Worker] {message}")
        
    def process_queue(self):
        """Process tweets from queue to coins table"""
        while self.running:
            try:
                # Skip busy check for test - process immediately
                
                # Get next queued tweet
                next_tweet = self.supabase.table('tweet_queue')\
                    .select('*')\
                    .eq('status', 'queued')\
                    .gte('followers_count', 500)\
                    .order('created_at')\
                    .limit(1)\
                    .execute()
                
                if not next_tweet.data:
                    time.sleep(2)
                    continue
                
                tweet = next_tweet.data[0]
                self.log(f"📥 Processing ${tweet['ticker']} from queue")
                
                # Update queue status
                self.supabase.table('tweet_queue')\
                    .update({'status': 'processing'})\
                    .eq('id', tweet['id'])\
                    .execute()
                
                # Move to coins table
                coin_data = {
                    'ticker': tweet['ticker'],
                    'name': tweet['name'],
                    'description': tweet['description'],
                    'website': tweet['website'],
                    'twitter': tweet['twitter'],
                    'twitter_user': tweet['twitter_user'],
                    'tweet_id': tweet['tweet_id'],
                    'image_url': tweet['image_url'],
                    'image_synced': False,
                    'status': 'pending'
                }
                
                result = self.supabase.table('coins').insert(coin_data).execute()
                
                if result.data:
                    # Mark as completed
                    self.supabase.table('tweet_queue')\
                        .update({
                            'status': 'completed',
                            'processed_at': datetime.now().isoformat()
                        })\
                        .eq('id', tweet['id'])\
                        .execute()
                    
                    self.log(f"✅ Moved ${tweet['ticker']} to coins table")
                
            except Exception as e:
                self.log(f"❌ Error: {e}")
            
            time.sleep(1)

class MockPhotoSync:
    """Simulated Photo Sync Service"""
    def __init__(self, supabase):
        self.supabase = supabase
        self.running = False
        self.downloads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_downloads')
        os.makedirs(self.downloads_dir, exist_ok=True)
        
    def log(self, message):
        print(f"[Photo Sync] {message}")
        
    def sync_photos(self):
        """Sync photos for coins without images"""
        while self.running:
            try:
                # Get coins needing photo sync
                coins = self.supabase.table('coins')\
                    .select('*')\
                    .eq('image_synced', False)\
                    .eq('status', 'pending')\
                    .execute()
                
                if not coins.data:
                    time.sleep(2)
                    continue
                
                for coin in coins.data:
                    self.log(f"🖼️  Syncing image for ${coin['ticker']}")
                    
                    # Simulate download
                    filename = f"{coin['twitter_user']}_{coin['ticker']}_{int(time.time())}.jpg"
                    filepath = os.path.join(self.downloads_dir, filename)
                    
                    # Create fake image file
                    with open(filepath, 'w') as f:
                        f.write(f"MOCK IMAGE FOR {coin['ticker']}")
                    
                    self.log(f"📥 Downloaded to: {filename}")
                    
                    # Simulate Photos import
                    time.sleep(1)
                    self.log(f"📸 Importing to Photos Library...")
                    time.sleep(1)
                    
                    # Update coin record
                    self.supabase.table('coins')\
                        .update({
                            'image_synced': True,
                            'image_filename': filename
                        })\
                        .eq('id', coin['id'])\
                        .execute()
                    
                    self.log(f"✅ Image synced for ${coin['ticker']}")
                    
            except Exception as e:
                self.log(f"❌ Error: {e}")
            
            time.sleep(2)

class MockAutomation:
    """Simulated Moonshot Automation"""
    def __init__(self, supabase):
        self.supabase = supabase
        self.running = False
        
    def log(self, message):
        print(f"[Automation] {message}")
        
    def process_coins(self):
        """Process coins ready for creation"""
        while self.running:
            try:
                # Get coins ready for processing
                coins = self.supabase.table('coins')\
                    .select('*')\
                    .eq('image_synced', True)\
                    .eq('status', 'pending')\
                    .order('created_at')\
                    .execute()
                
                if not coins.data:
                    time.sleep(2)
                    continue
                
                for coin in coins.data:
                    self.log(f"🚀 Creating token: ${coin['ticker']}")
                    
                    # Update status to processing
                    self.supabase.table('coins')\
                        .update({'status': 'processing'})\
                        .eq('id', coin['id'])\
                        .execute()
                    
                    # Simulate automation steps
                    self.log("📱 Opening Moonshot app...")
                    time.sleep(0.5)
                    
                    self.log("🖱️  Clicking Create button...")
                    time.sleep(0.5)
                    
                    self.log(f"⌨️  Typing ticker: {coin['ticker']}")
                    time.sleep(0.5)
                    
                    self.log(f"⌨️  Typing name: {coin['name']}")
                    time.sleep(0.5)
                    
                    self.log("📋 Pasting description...")
                    time.sleep(0.5)
                    
                    self.log("🖼️  Selecting image from Photos...")
                    time.sleep(1)
                    
                    self.log("✅ Clicking final Create button...")
                    time.sleep(1)
                    
                    # Update status to completed
                    self.supabase.table('coins')\
                        .update({
                            'status': 'completed',
                            'moonshot_url': f'https://moonshot.app/token/{coin["ticker"]}',
                            'created_at_moonshot': datetime.now().isoformat()
                        })\
                        .eq('id', coin['id'])\
                        .execute()
                    
                    self.log(f"🎉 Token created successfully: ${coin['ticker']}")
                    self.log(f"🔗 Moonshot URL: https://moonshot.app/token/{coin['ticker']}")
                    
            except Exception as e:
                self.log(f"❌ Error: {e}")
            
            time.sleep(3)

class FullIntegrationTest:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.test_tweet_ids = []
        self.test_coin_ids = []
        
    def log(self, message):
        print(f"\n{'='*60}")
        print(f"[MAIN] {message}")
        print(f"{'='*60}\n")
        
    def generate_test_tweets(self):
        """Generate 5 valid test tweets"""
        self.log("🎭 Generating test tweets...")
        
        test_data = [
            ("MOON", "moonwhale", 5000),
            ("PEPE", "pepelord", 2500),
            ("DOGE", "shibafan", 8000),
            ("MEME", "cryptodev", 1200),
            ("WOJAK", "degentrader", 750)
        ]
        
        tweets = []
        for i, (ticker, username, followers) in enumerate(test_data):
            tweet = MockTweet(f"200{i}", ticker, username, followers)
            tweets.append(tweet)
            
        return tweets
    
    def add_tweets_to_queue(self, tweets):
        """Add tweets to queue"""
        self.log("📝 Adding tweets to queue...")
        
        for tweet in tweets:
            try:
                # Get tweet data
                author = tweet.includes['users'][0]
                image_url = tweet.includes['media'][0]['url']
                
                queue_data = {
                    'tweet_id': tweet.id,
                    'twitter_user': author['username'],
                    'ticker': tweet.text.split('$')[1].split()[0],
                    'name': tweet.text.split('$')[1].split()[0],
                    'description': 'Bu token memeXshot aracılığı ile Moonshot\'ta create edildi',
                    'website': f"https://twitter.com/{author['username']}/status/{tweet.id}",
                    'twitter': f"@{author['username']}",
                    'image_url': image_url,
                    'followers_count': author['public_metrics']['followers_count'],
                    'status': 'queued'
                }
                
                result = self.supabase.table('tweet_queue').insert(queue_data).execute()
                if result.data:
                    self.test_tweet_ids.append(result.data[0]['id'])
                    print(f"  ✅ Added ${queue_data['ticker']} from @{author['username']}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
    
    def monitor_progress(self, duration=30):
        """Monitor the progress of all services"""
        self.log(f"📊 Monitoring progress for {duration} seconds...")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                # Get queue status
                queue_stats = self.supabase.table('tweet_queue')\
                    .select('status')\
                    .in_('tweet_id', [f"200{i}" for i in range(5)])\
                    .execute()
                
                # Get coins status
                coins_stats = self.supabase.table('coins')\
                    .select('ticker, status, image_synced')\
                    .in_('tweet_id', [f"200{i}" for i in range(5)])\
                    .execute()
                
                # Count statuses
                queue_counts = {}
                for item in queue_stats.data:
                    status = item['status']
                    queue_counts[status] = queue_counts.get(status, 0) + 1
                
                print(f"\r[{int(time.time() - start_time)}s] Queue: {queue_counts} | ", end="")
                
                if coins_stats.data:
                    print(f"Coins: ", end="")
                    for coin in coins_stats.data:
                        print(f"${coin['ticker']}({coin['status']},img:{coin['image_synced']}) ", end="")
                
                # Check if all completed
                completed = sum(1 for c in coins_stats.data if c and c.get('status') == 'completed')
                if completed == 5:
                    print("\n\n🎉 All tokens created successfully!")
                    break
                
                time.sleep(1)
                
            except Exception as e:
                print(f"\n❌ Monitor error: {e}")
                
        print("\n")
    
    def show_final_results(self):
        """Show final results"""
        self.log("📋 FINAL RESULTS")
        
        # Get all test data
        queue_data = self.supabase.table('tweet_queue')\
            .select('*')\
            .in_('tweet_id', [f"200{i}" for i in range(5)])\
            .execute()
        
        coins_data = self.supabase.table('coins')\
            .select('*')\
            .in_('tweet_id', [f"200{i}" for i in range(5)])\
            .execute()
        
        print("QUEUE STATUS:")
        for item in queue_data.data:
            print(f"  ${item['ticker']} - {item['status']}")
        
        print("\nCOINS STATUS:")
        for coin in coins_data.data:
            self.test_coin_ids.append(coin['id'])
            status_icon = "✅" if coin['status'] == 'completed' else "⏳"
            img_icon = "🖼️" if coin['image_synced'] else "❌"
            print(f"  {status_icon} ${coin['ticker']} - Status: {coin['status']} | Image: {img_icon}")
            if coin.get('moonshot_url'):
                print(f"     → {coin['moonshot_url']}")
    
    def cleanup(self):
        """Clean up test data"""
        self.log("🧹 Cleaning up test data...")
        
        try:
            # Delete from tweet_queue
            for tweet_id in [f"200{i}" for i in range(5)]:
                self.supabase.table('tweet_queue')\
                    .delete()\
                    .eq('tweet_id', tweet_id)\
                    .execute()
            
            # Delete from coins
            for coin_id in self.test_coin_ids:
                self.supabase.table('coins')\
                    .delete()\
                    .eq('id', coin_id)\
                    .execute()
            
            # Delete test files
            downloads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_downloads')
            if os.path.exists(downloads_dir):
                for file in os.listdir(downloads_dir):
                    os.remove(os.path.join(downloads_dir, file))
                os.rmdir(downloads_dir)
            
            print("✅ Cleanup completed")
            
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")
    
    def run_test(self):
        """Run the full integration test"""
        print("\n" + "🚀 FULL INTEGRATION TEST 🚀".center(60, "="))
        print("Testing: Twitter → Queue → Worker → Photos → Automation")
        print("="*60 + "\n")
        
        # Generate and add test tweets
        tweets = self.generate_test_tweets()
        self.add_tweets_to_queue(tweets)
        
        # Initialize services
        queue_worker = MockQueueWorker(self.supabase)
        photo_sync = MockPhotoSync(self.supabase)
        automation = MockAutomation(self.supabase)
        
        # Start services in threads
        self.log("🔧 Starting services...")
        
        queue_worker.running = True
        photo_sync.running = True
        automation.running = True
        
        worker_thread = threading.Thread(target=queue_worker.process_queue)
        photo_thread = threading.Thread(target=photo_sync.sync_photos)
        auto_thread = threading.Thread(target=automation.process_coins)
        
        worker_thread.start()
        print("  ✅ Queue Worker started")
        time.sleep(0.5)
        
        photo_thread.start()
        print("  ✅ Photo Sync started")
        time.sleep(0.5)
        
        auto_thread.start()
        print("  ✅ Automation started")
        
        # Monitor progress
        self.monitor_progress(duration=30)
        
        # Stop services
        self.log("🛑 Stopping services...")
        queue_worker.running = False
        photo_sync.running = False
        automation.running = False
        
        worker_thread.join(timeout=2)
        photo_thread.join(timeout=2)
        auto_thread.join(timeout=2)
        
        # Show results
        self.show_final_results()
        
        # Cleanup automatically
        self.log("Cleaning up test data...")
        self.cleanup()
        
        self.log("✅ Test completed!")

if __name__ == "__main__":
    test = FullIntegrationTest()
    test.run_test()