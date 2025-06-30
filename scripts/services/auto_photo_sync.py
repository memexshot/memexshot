#!/usr/bin/env python3
"""
Auto Photo Sync Service
Syncs images from Supabase to macOS Photos Library
"""

import os
import sys
import time
import requests
import subprocess
from datetime import datetime

# Add moonshot_automation root directory to path (go up 2 levels from scripts/services/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from supabase import create_client
from config.supabase_config import SUPABASE_URL, SUPABASE_KEY, COINS_TABLE

class AutoPhotoSync:
    def __init__(self):
        # Initialize Supabase client
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("❌ Missing Supabase credentials!")
            sys.exit(1)
            
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Create import folder
        self.import_folder = os.path.expanduser("~/Pictures/MoonshotAutoImport")
        os.makedirs(self.import_folder, exist_ok=True)
        print(f"📁 Import folder: {self.import_folder}")
        
        # Track coins currently being processed to avoid duplicates
        self.processing_coins = set()
        # Track processed image URLs to avoid downloading same image multiple times
        self.processed_image_urls = set()
        
        # Log file
        self.log_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'logs', 
            'photo_sync.log'
        )
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def download_image(self, url, filepath):
        """Download image from URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            self.log(f"❌ Failed to download image: {e}")
            return False
    
    def import_to_photos(self, image_path):
        """Import image to Photos using AppleScript"""
        try:
            # AppleScript to import image
            script = f'''
            tell application "Photos"
                activate
                delay 1
                import POSIX file "{image_path}"
                delay 3
            end tell
            '''
            
            # Run AppleScript
            process = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                self.log(f"⚠️  AppleScript error: {process.stderr}")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to import to Photos: {e}")
            return False
    
    def sync_image(self, coin):
        """Sync a single image from Supabase to Photos"""
        try:
            self.log(f"🖼️  Syncing image for {coin['ticker']} - {coin['name']}")
            
            # Check if this image URL was already processed
            image_url = coin.get('image_url')
            if image_url in self.processed_image_urls:
                self.log(f"⚠️  Image URL already processed: {image_url[:50]}...")
                # Still mark as synced in database
                self.supabase.table(COINS_TABLE).update({
                    'image_synced': True,
                    'image_sync_timestamp': datetime.now().isoformat(),
                    'image_filename': f"shared_image_{coin['ticker']}_{int(time.time())}.jpg"
                }).eq('id', coin['id']).execute()
                return True
            
            # Generate filename
            if coin['image_filename']:
                filename = coin['image_filename']
            else:
                # Create filename from twitter_user_ticker_timestamp
                timestamp = int(time.time())
                twitter_user = coin.get('twitter_user', 'user').replace('@', '')
                filename = f"{twitter_user}_{coin['ticker']}_{timestamp}.jpg"
            
            # Download image
            local_path = os.path.join(self.import_folder, filename)
            if not self.download_image(coin['image_url'], local_path):
                return False
            
            self.log(f"✅ Downloaded to: {local_path}")
            
            # Import to Photos
            if not self.import_to_photos(local_path):
                # Cleanup on failure
                if os.path.exists(local_path):
                    os.remove(local_path)
                return False
            
            self.log(f"✅ Imported to Photos")
            
            # Wait a bit for Photos to process
            time.sleep(5)
            
            # Cleanup local file
            if os.path.exists(local_path):
                os.remove(local_path)
            
            # Add to processed URLs
            self.processed_image_urls.add(image_url)
            
            # Update Supabase - mark as synced but keep status as pending
            self.supabase.table(COINS_TABLE).update({
                'image_synced': True,
                'image_sync_timestamp': datetime.now().isoformat(),
                'image_filename': filename
                # Don't change status - let Supabase Listener handle that
            }).eq('id', coin['id']).execute()
            
            self.log(f"✅ Sync completed for {coin['ticker']}")
            return True
            
        except Exception as e:
            self.log(f"❌ Error syncing image: {e}")
            return False
    
    def check_pending_images(self):
        """Check for images that need syncing"""
        try:
            # Query for unsynced images - include all active statuses
            result = self.supabase.table(COINS_TABLE)\
                .select('*')\
                .eq('image_synced', False)\
                .not_.is_('image_url', 'null')\
                .eq('status', 'pending')\
                .order('created_at')\
                .execute()
            
            if result.data:
                self.log(f"📋 Found {len(result.data)} images to sync")
                # Show all coins found
                for i, coin in enumerate(result.data):
                    self.log(f"  [{i+1}] {coin['ticker']} - ID: {coin['id'][:8]}... - URL: {coin.get('image_url', '')[:40]}...")
                
                for coin in result.data:
                    # Skip if already processing
                    if coin['id'] in self.processing_coins:
                        self.log(f"  ⏭️  Skipping {coin['ticker']} - Already being processed")
                        continue
                        
                    self.log(f"  🪙 {coin['ticker']} - Status: {coin.get('status')} - Image URL: {coin.get('image_url', 'None')[:50]}...")
                    
                    # Add to processing set
                    self.processing_coins.add(coin['id'])
                    
                    # Sync the image
                    success = self.sync_image(coin)
                    
                    # Remove from processing set after completion
                    if success:
                        # Keep in set to avoid re-processing in same session
                        pass
                    else:
                        # Remove on failure to allow retry
                        self.processing_coins.discard(coin['id'])
                    
                    # Wait between syncs
                    time.sleep(10)
            else:
                # Debug: Show recent coins
                debug_result = self.supabase.table(COINS_TABLE)\
                    .select('ticker, status, image_url, image_synced')\
                    .order('created_at', desc=True)\
                    .limit(5)\
                    .execute()
                
                if debug_result.data:
                    self.log("🔍 DEBUG - Recent coins:")
                    for coin in debug_result.data:
                        self.log(f"   {coin['ticker']}: status={coin['status']}, image_synced={coin['image_synced']}, has_image={bool(coin['image_url'])}")
            
        except Exception as e:
            self.log(f"❌ Error checking pending images: {e}")
    
    def run(self):
        """Main service loop"""
        self.log("🚀 Starting Auto Photo Sync Service")
        self.log(f"📡 Connected to: {SUPABASE_URL}")
        self.log("👂 Monitoring for new images...")
        
        check_count = 0
        while True:
            try:
                check_count += 1
                if check_count % 10 == 1:  # Log every 10th check
                    self.log(f"🔄 Check #{check_count} for pending images...")
                
                self.check_pending_images()
                
                # Wait before next check
                time.sleep(30)
                
            except KeyboardInterrupt:
                self.log("👋 Stopping service...")
                break
            except Exception as e:
                self.log(f"❌ Unexpected error: {e}")
                time.sleep(60)  # Wait longer on error

if __name__ == "__main__":
    service = AutoPhotoSync()
    service.run()