#!/usr/bin/env python3
"""
Moonshot App Automation Script
Automates coin creation using captured coordinates
"""

import time
import json
import os
import sys
import math
from datetime import datetime
import Quartz
import pyperclip
from pynput import mouse, keyboard

class MoonshotAutomation:
    def __init__(self, coordinates_file, coins_data_file=None):
        self.coordinates = self.load_coordinates(coordinates_file)
        self.coins = self.load_coins_data(coins_data_file) if coins_data_file else []
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        
    def load_coordinates(self, filepath):
        """Load coordinates from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Convert list to dict for easier access
        coords_dict = {}
        for coord in data['coordinates']:
            coords_dict[coord['name']] = (coord['x'], coord['y'])
        
        return coords_dict
    
    def load_coins_data(self, filepath):
        """Load coins data from JSON file"""
        if not filepath:
            return []
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data['coins']
    
    def save_coins_data(self, filepath):
        """Save updated coins data"""
        data = {"coins": self.coins}
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def click_at(self, x, y, delay_after=2):
        """Click at specific coordinates"""
        print(f"  Clicking at ({x}, {y})")
        self.mouse_controller.position = (x, y)
        time.sleep(0.5)  # Small delay to ensure mouse is in position
        self.mouse_controller.click(mouse.Button.left)
        time.sleep(delay_after)
    
    def paste_text(self, text):
        """Copy text to clipboard and paste using Cmd+V"""
        pyperclip.copy(text)
        time.sleep(0.2)
        
        # Press Cmd+V
        with self.keyboard_controller.pressed(keyboard.Key.cmd):
            self.keyboard_controller.press('v')
            self.keyboard_controller.release('v')
        time.sleep(0.5)
    
    def clear_field(self):
        """Clear current field using Cmd+A and Delete"""
        # Select all
        with self.keyboard_controller.pressed(keyboard.Key.cmd):
            self.keyboard_controller.press('a')
            self.keyboard_controller.release('a')
        time.sleep(0.2)
        
        # Delete
        self.keyboard_controller.press(keyboard.Key.backspace)
        self.keyboard_controller.release(keyboard.Key.backspace)
        time.sleep(0.2)
    
    def swipe_right(self, start_x, start_y, distance=250):
        """Simulate swipe right gesture with improved motion"""
        print(f"  Swiping right from ({start_x}, {start_y})")
        
        # First click to focus
        self.mouse_controller.position = (start_x, start_y)
        time.sleep(0.5)
        self.mouse_controller.click(mouse.Button.left)
        time.sleep(0.5)
        
        # Position at start of swipe
        self.mouse_controller.position = (start_x, start_y)
        time.sleep(0.5)
        
        # Press and hold
        self.mouse_controller.press(mouse.Button.left)
        time.sleep(0.2)
        
        # Move gradually with acceleration curve
        steps = 30
        for i in range(steps):
            # Ease-in-out motion
            progress = i / steps
            ease_progress = 0.5 - 0.5 * math.cos(progress * math.pi)
            new_x = start_x + (distance * ease_progress)
            self.mouse_controller.position = (new_x, start_y)
            time.sleep(0.02)  # Slower movement
        
        # Hold at end position briefly
        time.sleep(0.3)
        
        # Release
        self.mouse_controller.release(mouse.Button.left)
        time.sleep(2)  # Wait for animation to complete
    
    def create_coin(self, coin):
        """Create a single coin using the automation flow"""
        print(f"\n{'='*60}")
        print(f"Creating coin: {coin['name']} ({coin['ticker']})")
        print(f"{'='*60}")
        
        try:
            # Step 1: Click Create button (with focus check)
            print("\n1. Clicking Create button...")
            x, y = self.coordinates["Create button (bottom menu)"]
            self.click_at(x, y, delay_after=3)
            
            # Focus check: Click again to ensure app is focused
            print("   Ensuring app focus...")
            self.click_at(x, y, delay_after=3)
            
            # Step 2: Click Create coin button
            print("2. Clicking Create coin button...")
            x, y = self.coordinates["Create coin button (above create button)"]
            self.click_at(x, y, delay_after=5)  # Wait for form to load
            
            # Step 3: Fill ticker field
            print("3. Filling ticker field...")
            x, y = self.coordinates["Ticker input field"]
            self.click_at(x, y)
            self.clear_field()
            self.paste_text(coin['ticker'])
            
            # Step 4: Fill name field
            print("4. Filling name field...")
            x, y = self.coordinates["Name input field"]
            self.click_at(x, y)
            self.clear_field()
            self.paste_text(coin['name'])
            
            # Step 5: Add image
            print("5. Adding image...")
            x, y = self.coordinates["Add image button (top left)"]
            self.click_at(x, y, delay_after=3)
            
            # Step 6: Choose from library
            print("6. Choosing from library...")
            x, y = self.coordinates["Choose from library button"]
            self.click_at(x, y, delay_after=5)  # Wait for gallery to load
            
            # Step 7: Select last image in gallery
            print("7. Selecting image from gallery...")
            x, y = self.coordinates["First image in gallery"]
            self.click_at(x, y, delay_after=1)
            
            # Step 8: Click Done button
            print("8. Clicking Done button...")
            x, y = self.coordinates["Done button (bottom right)"]
            self.click_at(x, y, delay_after=3)
            
            # Step 9: Fill description field
            print("9. Filling description field...")
            x, y = self.coordinates["Description input field"]
            self.click_at(x, y)
            self.clear_field()
            self.paste_text(coin['description'])
            
            # Step 10: Fill website field
            print("10. Filling website field...")
            x, y = self.coordinates["Website input field"]
            self.click_at(x, y)
            self.clear_field()
            self.paste_text(coin['website'])
            
            # Step 11: Fill twitter field
            print("11. Filling twitter field...")
            x, y = self.coordinates["Twitter input field"]
            self.click_at(x, y)
            self.clear_field()
            self.paste_text(coin['twitter'])
            
            # Step 12: Swipe to create
            print("12. Swiping to create...")
            x, y = self.coordinates["Swipe to create button (swipe right)"]
            self.swipe_right(x, y)
            
            # Step 13: Enter macOS password automatically
            print("13. Entering macOS password...")
            time.sleep(3)  # Wait for dialog to appear
            
            # Type password
            password = "617259"
            for char in password:
                self.keyboard_controller.press(char)
                self.keyboard_controller.release(char)
                time.sleep(0.1)
            
            # Press Enter
            time.sleep(0.5)
            self.keyboard_controller.press(keyboard.Key.enter)
            self.keyboard_controller.release(keyboard.Key.enter)
            
            # Wait for processing
            print("   Waiting for token creation...")
            time.sleep(12)
            
            # Step 14: Close success screen
            print("14. Closing success screen...")
            x, y = self.coordinates["Close button (X - top right)"]
            self.click_at(x, y, delay_after=3)
            
            # Update coin status
            coin['status'] = 'completed'
            coin['processed_at'] = datetime.now().isoformat()
            
            print(f"\n✅ Successfully created: {coin['name']}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error creating coin: {str(e)}")
            coin['status'] = 'failed'
            coin['error_message'] = str(e)
            return False
    
    def run(self, coins_data_file):
        """Run the automation for all pending coins"""
        print("🚀 Moonshot Automation Starting...")
        print(f"Found {len(self.coins)} coins in database")
        
        # Filter pending coins
        pending_coins = [c for c in self.coins if c['status'] == 'pending']
        print(f"Processing {len(pending_coins)} pending coins")
        
        if not pending_coins:
            print("No pending coins to process!")
            return
        
        print("\n⚠️  IMPORTANT:")
        print("- Make sure Moonshot app is open")
        print("- The app should be on the main screen")
        print("- macOS password will be entered automatically")
        
        input("\nPress Enter to start automation...")
        
        print("\n⏱️  Starting in 5 seconds... (Switch to Moonshot app now!)")
        for i in range(5, 0, -1):
            print(f"   {i}...", end='', flush=True)
            time.sleep(1)
        print("\n")
        
        # Process each coin
        for i, coin in enumerate(pending_coins):
            print(f"\n[{i+1}/{len(pending_coins)}] Processing...")
            
            success = self.create_coin(coin)
            
            # Save progress after each coin
            self.save_coins_data(coins_data_file)
            
            # Delay between coins to avoid rate limiting
            if i < len(pending_coins) - 1:
                print("\n⏱️  Waiting 30 seconds before next coin...")
                time.sleep(30)
        
        # Final summary
        print("\n" + "="*60)
        print("AUTOMATION COMPLETE!")
        print("="*60)
        
        completed = len([c for c in self.coins if c['status'] == 'completed'])
        failed = len([c for c in self.coins if c['status'] == 'failed'])
        
        print(f"✅ Completed: {completed}")
        print(f"❌ Failed: {failed}")
        print(f"⏳ Remaining: {len([c for c in self.coins if c['status'] == 'pending'])}")

def main():
    # Get the latest coordinates file
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    # Find the latest coordinates file
    coord_files = [f for f in os.listdir(data_dir) if f.startswith('moonshot_coordinates_')]
    if not coord_files:
        print("❌ No coordinates file found! Run coordinate_capture_click.py first.")
        sys.exit(1)
    
    # Use the latest file
    coord_files.sort()
    latest_coords = os.path.join(data_dir, coord_files[-1])
    print(f"Using coordinates file: {latest_coords}")
    
    # Coins data file
    coins_file = os.path.join(data_dir, 'coins_data.json')
    if not os.path.exists(coins_file):
        print("❌ No coins_data.json file found!")
        sys.exit(1)
    
    # Create automation instance and run
    automation = MoonshotAutomation(latest_coords, coins_file)
    automation.run(coins_file)

if __name__ == "__main__":
    main()