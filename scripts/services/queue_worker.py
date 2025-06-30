#!/usr/bin/env python3
"""
Queue Worker Service
Processes tweets from queue to main coins table
"""

import os
import sys
import time
from datetime import datetime

# Add moonshot_automation root directory to path (go up 2 levels from scripts/services/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from supabase import create_client
from config.supabase_config import SUPABASE_URL, SUPABASE_KEY

class QueueWorker:
    def __init__(self):
        # Initialize Supabase
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Log file
        self.log_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'logs', 
            'queue_worker.log'
        )
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def has_active_processing(self):
        """Check if there's an active coin being processed"""
        try:
            result = self.supabase.table('coins')\
                .select('id')\
                .in_('status', ['pending', 'processing'])\
                .execute()
            
            return len(result.data) > 0 if result.data else False
            
        except Exception as e:
            self.log(f"❌ Error checking active processing: {e}")
            return True  # Assume busy on error
    
    def get_next_tweet(self):
        """Get next tweet from queue"""
        try:
            result = self.supabase.table('tweet_queue')\
                .select('*')\
                .eq('status', 'queued')\
                .order('created_at')\
                .limit(1)\
                .execute()
            
            return result.data[0] if result.data else None
            
        except Exception as e:
            self.log(f"❌ Error getting next tweet: {e}")
            return None
    
    def move_to_coins(self, tweet):
        """Move tweet from queue to coins table"""
        try:
            # Prepare coin data
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
            
            # Start transaction
            # 1. Update queue status
            self.supabase.table('tweet_queue')\
                .update({'status': 'processing'})\
                .eq('id', tweet['id'])\
                .execute()
            
            # 2. Insert to coins
            result = self.supabase.table('coins').insert(coin_data).execute()
            
            if result.data:
                # 3. Mark queue item as completed
                self.supabase.table('tweet_queue')\
                    .update({
                        'status': 'completed',
                        'processed_at': datetime.now().isoformat()
                    })\
                    .eq('id', tweet['id'])\
                    .execute()
                
                self.log(f"✅ Moved to processing: {tweet['ticker']} from @{tweet['twitter_user']}")
                return True
            
        except Exception as e:
            self.log(f"❌ Error moving tweet: {e}")
            
            # Revert queue status
            self.supabase.table('tweet_queue')\
                .update({'status': 'queued'})\
                .eq('id', tweet['id'])\
                .execute()
            
            return False
    
    def cleanup_old_queue(self):
        """Clean up old completed queue items (older than 24 hours)"""
        try:
            # Calculate 24 hours ago
            cutoff = datetime.now().timestamp() - (24 * 60 * 60)
            cutoff_date = datetime.fromtimestamp(cutoff).isoformat()
            
            # Delete old completed items
            result = self.supabase.table('tweet_queue')\
                .delete()\
                .eq('status', 'completed')\
                .lt('processed_at', cutoff_date)\
                .execute()
            
            if result.data:
                self.log(f"🧹 Cleaned up {len(result.data)} old queue items")
                
        except Exception as e:
            self.log(f"⚠️  Error cleaning queue: {e}")
    
    def run(self):
        """Main worker loop"""
        self.log("🚀 Starting Queue Worker")
        self.log("Processing tweets from queue to coins table...")
        
        # Cleanup counter
        cleanup_counter = 0
        
        while True:
            try:
                # Check if system is busy
                if self.has_active_processing():
                    self.log("⏳ System busy with active processing...")
                else:
                    # Get next tweet from queue
                    next_tweet = self.get_next_tweet()
                    
                    if next_tweet:
                        self.log(f"📨 Processing queued tweet: {next_tweet['ticker']}")
                        self.move_to_coins(next_tweet)
                    else:
                        # No tweets in queue
                        pass
                
                # Cleanup old items every 100 iterations
                cleanup_counter += 1
                if cleanup_counter >= 100:
                    self.cleanup_old_queue()
                    cleanup_counter = 0
                
                # Wait before next check
                time.sleep(10)
                
            except KeyboardInterrupt:
                self.log("👋 Stopping queue worker...")
                break
            except Exception as e:
                self.log(f"❌ Unexpected error: {e}")
                time.sleep(30)

if __name__ == "__main__":
    worker = QueueWorker()
    worker.run()