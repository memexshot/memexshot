#!/usr/bin/env python3
"""
Supabase Polling Listener for Moonshot Automation
Polls for new coin entries and triggers automation
"""

import os
import sys
import time
import json
from datetime import datetime
from supabase import create_client, Client

# Add moonshot_automation root directory to path (go up 2 levels from scripts/automation/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.supabase_config import (
    SUPABASE_URL, SUPABASE_KEY, COINS_TABLE,
    STATUS_PENDING, STATUS_PROCESSING, STATUS_COMPLETED, STATUS_FAILED
)

# Import the automation module (proprietary in full version)
try:
    from scripts.automation.moonshot_automation import MoonshotAutomation
    AUTOMATION_AVAILABLE = True
except (ImportError, NotImplementedError):
    AUTOMATION_AVAILABLE = False
    print("⚠️  Note: Running without the proprietary automation module")

class SupabasePollingListener:
    def __init__(self):
        # Initialize Supabase client
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("❌ Missing Supabase credentials! Please set SUPABASE_URL and SUPABASE_KEY in .env file")
            sys.exit(1)
            
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.automation = None
        self.processed_ids = set()
        
        # Initialize automation if available
        if AUTOMATION_AVAILABLE:
            self.setup_automation()
        
    def setup_automation(self):
        """Setup automation with latest coordinates"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        
        # Find the latest coordinates file
        coord_files = [f for f in os.listdir(data_dir) if f.startswith('moonshot_coordinates_')]
        if not coord_files:
            print("❌ No coordinates file found! Run coordinate_capture_click.py first.")
            sys.exit(1)
        
        coord_files.sort()
        latest_coords = os.path.join(data_dir, coord_files[-1])
        print(f"Using coordinates file: {latest_coords}")
        
        # Create automation instance
        self.automation = MoonshotAutomation(latest_coords, None)
    
    def process_coin(self, coin_data):
        """Process a single coin"""
        print(f"\n🔄 Processing coin: {coin_data['name']} ({coin_data['ticker']})")
        
        try:
            # Update status to processing
            self.update_coin_status(coin_data['id'], STATUS_PROCESSING)
            
            if not AUTOMATION_AVAILABLE:
                print("⚠️  Cannot create token without proprietary automation module")
                self.update_coin_status(
                    coin_data['id'], 
                    STATUS_FAILED,
                    error_message="Automation module not available"
                )
                return
            
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
            
            # Wait a moment for user to switch to Moonshot
            print("⏱️  Starting in 5 seconds... (Switch to Moonshot app!)")
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
                print(f"✅ Successfully processed: {coin_data['name']}")
            else:
                # Update status to failed
                self.update_coin_status(
                    coin_data['id'], 
                    STATUS_FAILED,
                    error_message="Automation failed"
                )
                print(f"❌ Failed to process: {coin_data['name']}")
                
        except Exception as e:
            print(f"❌ Error processing coin: {str(e)}")
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
            print(f"⚠️  Failed to update status: {str(e)}")
    
    def check_for_new_coins(self):
        """Check for new pending coins"""
        try:
            response = self.supabase.table(COINS_TABLE)\
                .select("*")\
                .eq('status', STATUS_PENDING)\
                .eq('image_synced', True)\
                .order('created_at')\
                .execute()
            
            pending_coins = response.data
            new_coins = [coin for coin in pending_coins if coin['id'] not in self.processed_ids]
            
            if new_coins:
                print(f"\n🆕 Found {len(new_coins)} new coin(s) to process")
                
                for i, coin in enumerate(new_coins):
                    self.processed_ids.add(coin['id'])
                    self.process_coin(coin)
                    
                    # Wait between coins
                    if i < len(new_coins) - 1:
                        print("\n⏱️  Waiting 30 seconds before next coin...")
                        time.sleep(30)
                        
            return len(new_coins) > 0
            
        except Exception as e:
            print(f"❌ Error checking for coins: {str(e)}")
            return False
    
    def start(self):
        """Start polling for new coins"""
        print("🚀 Moonshot Automation - Supabase Polling Listener")
        print("="*60)
        print(f"Connected to: {SUPABASE_URL}")
        print(f"Polling table: {COINS_TABLE}")
        print(f"Poll interval: 5 seconds")
        print("="*60)
        
        # Check for existing pending coins first
        print("\n📋 Checking for existing pending coins...")
        self.check_for_new_coins()
        
        print("\n👂 Polling for new coins...")
        print("Press Ctrl+C to stop")
        
        # Keep polling
        try:
            while True:
                # Check for new coins
                self.check_for_new_coins()
                
                # Wait before next poll
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n👋 Stopping listener...")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    # Check if Moonshot app reminder needed
    if AUTOMATION_AVAILABLE:
        print("\n⚠️  IMPORTANT:")
        print("- Make sure Moonshot app is open")
        print("- The app should be on the main screen")
        print("- macOS password will be entered automatically")
    
    # Start automatically
    print("\n🚀 Starting automatically...")
    
    listener = SupabasePollingListener()
    listener.start()