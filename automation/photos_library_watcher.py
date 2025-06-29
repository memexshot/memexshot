#!/usr/bin/env python3
"""
Photos Library Watcher
Monitors Photos Library for new images and triggers token creation
"""

import os
import sys
import time
import re
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase import create_client
from config.supabase_config import (
    SUPABASE_URL, SUPABASE_KEY, COINS_TABLE,
    STATUS_PENDING, STATUS_PROCESSING, STATUS_COMPLETED, STATUS_FAILED
)
from automation.moonshot_automation import MoonshotAutomation

class PhotosLibraryWatcher:
    def __init__(self):
        # Initialize Supabase client
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("❌ Missing Supabase credentials!")
            sys.exit(1)
            
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.automation = None
        self.processed_images = set()
        
        # Log file
        self.log_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'logs', 
            'library_watcher.log'
        )
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Initialize automation
        self.setup_automation()
    
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def setup_automation(self):
        """Setup automation with latest coordinates"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        
        # Find the latest coordinates file
        coord_files = [f for f in os.listdir(data_dir) if f.startswith('moonshot_coordinates_')]
        if not coord_files:
            self.log("❌ No coordinates file found!")
            sys.exit(1)
        
        coord_files.sort()
        latest_coords = os.path.join(data_dir, coord_files[-1])
        self.log(f"Using coordinates file: {latest_coords}")
        
        # Create automation instance
        self.automation = MoonshotAutomation(latest_coords, None)
    
    def find_coin_by_filename(self, filename):
        """Find coin in Supabase by image filename"""
        try:
            # Extract ticker from filename (format: username_TICKER_timestamp.jpg)
            match = re.match(r'.*_([A-Z]+)_\d+\.jpg', filename)
            if not match:
                return None
            
            ticker = match.group(1)
            
            # Find coin with this ticker and pending status
            result = self.supabase.table(COINS_TABLE)\
                .select('*')\
                .eq('ticker', ticker)\
                .eq('status', STATUS_PENDING)\
                .eq('image_synced', True)\
                .order('created_at', desc=True)\
                .limit(1)\
                .execute()
            
            if result.data:
                return result.data[0]
            
            return None
            
        except Exception as e:
            self.log(f"❌ Error finding coin: {e}")
            return None
    
    def process_coin(self, coin_data):
        """Process a single coin"""
        self.log(f"🔄 Processing coin: {coin_data['name']} ({coin_data['ticker']})")
        
        try:
            # Update status to processing
            self.update_coin_status(coin_data['id'], STATUS_PROCESSING)
            
            # Convert Supabase data to expected format
            coin = {
                'id': coin_data['id'],
                'ticker': coin_data['ticker'],
                'name': coin_data['name'],
                'description': coin_data['description'],
                'website': coin_data['website'],
                'twitter': coin_data['twitter'],
                'status': STATUS_PROCESSING
            }
            
            # Wait for user to switch to Moonshot
            print("\n⏱️  Starting in 5 seconds... (Switch to Moonshot app!)")
            for i in range(5, 0, -1):
                print(f"   {i}...", end='', flush=True)
                time.sleep(1)
            print("\n")
            
            # Process the coin
            success = self.automation.create_coin(coin)
            
            if success:
                # Update status to completed
                self.update_coin_status(
                    coin_data['id'], 
                    STATUS_COMPLETED,
                    processed_at=datetime.now().isoformat()
                )
                self.log(f"✅ Successfully processed: {coin_data['name']}")
            else:
                # Update status to failed
                self.update_coin_status(
                    coin_data['id'], 
                    STATUS_FAILED,
                    error_message="Automation failed"
                )
                self.log(f"❌ Failed to process: {coin_data['name']}")
                
        except Exception as e:
            self.log(f"❌ Error processing coin: {str(e)}")
            self.update_coin_status(
                coin_data['id'], 
                STATUS_FAILED,
                error_message=str(e)
            )
    
    def update_coin_status(self, coin_id, status, **kwargs):
        """Update coin status in Supabase"""
        update_data = {
            'status': status,
            'updated_at': datetime.now().isoformat()
        }
        update_data.update(kwargs)
        
        try:
            self.supabase.table(COINS_TABLE).update(update_data).eq('id', coin_id).execute()
        except Exception as e:
            self.log(f"⚠️  Failed to update status: {str(e)}")
    
    def check_for_new_images(self):
        """Check for new images in Photos Library"""
        # Note: This is a simplified version
        # In a real implementation, you'd need to properly access Photos Library
        
        # For now, let's check for recently synced coins
        try:
            result = self.supabase.table(COINS_TABLE)\
                .select('*')\
                .eq('status', STATUS_PENDING)\
                .eq('image_synced', True)\
                .order('image_sync_timestamp', desc=True)\
                .limit(1)\
                .execute()
            
            if result.data:
                coin = result.data[0]
                
                # Check if we haven't processed this yet
                if coin['id'] not in self.processed_images:
                    self.log(f"🖼️  New image detected for: {coin['ticker']}")
                    self.processed_images.add(coin['id'])
                    
                    # Process the coin
                    self.process_coin(coin)
                    
                    return True
            
            return False
            
        except Exception as e:
            self.log(f"❌ Error checking for images: {e}")
            return False
    
    def run(self):
        """Main watcher loop"""
        self.log("🚀 Starting Photos Library Watcher")
        self.log("👁️  Monitoring for new images...")
        
        # Check for any existing pending coins first
        self.check_for_new_images()
        
        while True:
            try:
                # Check for new images
                self.check_for_new_images()
                
                # Wait before next check
                time.sleep(10)
                
            except KeyboardInterrupt:
                self.log("👋 Stopping watcher...")
                break
            except Exception as e:
                self.log(f"❌ Unexpected error: {e}")
                time.sleep(30)

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT:")
    print("- Make sure Moonshot app is open")
    print("- The app should be on the main screen")
    print("- Photo Sync Service should be running")
    
    input("\nPress Enter to start watcher...")
    
    watcher = PhotosLibraryWatcher()
    watcher.run()