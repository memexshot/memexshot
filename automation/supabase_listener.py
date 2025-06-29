#!/usr/bin/env python3
"""
Supabase Real-time Listener for Moonshot Automation
Listens for new coin entries and triggers automation
"""

import os
import sys
import time
import json
from datetime import datetime
from supabase import create_client, Client

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.supabase_config import (
    SUPABASE_URL, SUPABASE_KEY, COINS_TABLE,
    STATUS_PENDING, STATUS_PROCESSING, STATUS_COMPLETED, STATUS_FAILED
)
from automation.moonshot_automation import MoonshotAutomation

class SupabaseListener:
    def __init__(self):
        # Initialize Supabase client
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("❌ Missing Supabase credentials! Please set SUPABASE_URL and SUPABASE_KEY in .env file")
            sys.exit(1)
            
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.automation = None
        self.channel = None
        
        # Initialize automation
        self.setup_automation()
        
    def setup_automation(self):
        """Setup automation with latest coordinates"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        
        # Find the latest coordinates file
        coord_files = [f for f in os.listdir(data_dir) if f.startswith('moonshot_coordinates_')]
        if not coord_files:
            print("❌ No coordinates file found! Run coordinate_capture_click.py first.")
            sys.exit(1)
        
        coord_files.sort()
        latest_coords = os.path.join(data_dir, coord_files[-1])
        print(f"Using coordinates file: {latest_coords}")
        
        # Create automation instance (we'll pass individual coins instead of file)
        self.automation = MoonshotAutomation(latest_coords, None)
    
    def process_coin(self, coin_data):
        """Process a single coin"""
        print(f"\n🔄 Processing coin: {coin_data['name']} ({coin_data['ticker']})")
        
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
    
    def on_insert(self, payload):
        """Handle new coin insertion"""
        new_coin = payload['new']
        
        # Only process if status is pending
        if new_coin.get('status') == STATUS_PENDING:
            print(f"\n🆕 New coin detected: {new_coin['name']} ({new_coin['ticker']})")
            
            # Wait a moment for Moonshot to be ready
            print("⏱️  Starting in 5 seconds... (Switch to Moonshot app!)")
            for i in range(5, 0, -1):
                print(f"   {i}...", end='', flush=True)
                time.sleep(1)
            print("\n")
            
            # Process the coin
            self.process_coin(new_coin)
    
    def check_pending_coins(self):
        """Check for any pending coins on startup"""
        try:
            response = self.supabase.table(COINS_TABLE)\
                .select("*")\
                .eq('status', STATUS_PENDING)\
                .order('created_at')\
                .execute()
            
            pending_coins = response.data
            if pending_coins:
                print(f"\n📋 Found {len(pending_coins)} pending coins")
                
                for coin in pending_coins:
                    self.process_coin(coin)
                    
                    # Wait between coins
                    if pending_coins.index(coin) < len(pending_coins) - 1:
                        print("\n⏱️  Waiting 30 seconds before next coin...")
                        time.sleep(30)
        except Exception as e:
            print(f"❌ Error checking pending coins: {str(e)}")
    
    def start(self):
        """Start listening for new coins"""
        print("🚀 Moonshot Automation - Supabase Listener")
        print("="*60)
        print(f"Connected to: {SUPABASE_URL}")
        print(f"Listening to table: {COINS_TABLE}")
        print("="*60)
        
        # Check for pending coins first
        self.check_pending_coins()
        
        print("\n👂 Listening for new coins...")
        print("Press Ctrl+C to stop")
        
        # Set up real-time subscription
        try:
            # Create channel and subscribe to insert events
            self.channel = self.supabase.channel('coins-insert')\
                .on('postgres_changes', 
                    event='INSERT', 
                    schema='public', 
                    table=COINS_TABLE, 
                    callback=lambda x: self.on_insert(x['payload']))\
                .subscribe()
            
            # Keep the script running
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n👋 Stopping listener...")
            if self.channel:
                self.channel.unsubscribe()
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    # Check if Moonshot app reminder needed
    print("\n⚠️  IMPORTANT:")
    print("- Make sure Moonshot app is open")
    print("- The app should be on the main screen")
    print("- macOS password will be entered automatically")
    
    input("\nPress Enter to start listener...")
    
    listener = SupabaseListener()
    listener.start()