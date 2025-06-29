#!/usr/bin/env python3
"""
Moonshot App Coordinate Capture Tool - Click Version
Captures mouse coordinates when user clicks
"""

import time
import json
import os
from datetime import datetime
from pynput import mouse
import threading

class ClickCoordinateCapture:
    def __init__(self):
        self.coordinates = []
        self.current_step = 0
        self.steps = [
            "Create button (bottom menu)",
            "Create coin button (above create button)",
            "Ticker input field",
            "Name input field", 
            "Add image button (top left)",
            "Choose from library button",
            "First image in gallery",
            "Done button (bottom right)",
            "Description input field",
            "Website input field",
            "Twitter input field",
            "Swipe to create button (swipe right)",
            "macOS password dialog (click after entering password)",
            "Close button (X - top right)",
            "Create button again (bottom menu - cycle complete)"
        ]
        self.click_detected = False
        self.last_x = 0
        self.last_y = 0
        self.listener = None
        
    def on_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        if pressed and button == mouse.Button.left:
            self.last_x = int(x)
            self.last_y = int(y)
            self.click_detected = True
            return False  # Stop listener after click
    
    def capture_step(self, step_index):
        """Capture coordinates for a single step"""
        step_name = self.steps[step_index]
        
        print(f"\n{'='*60}")
        print(f"Step {step_index + 1}/{len(self.steps)}")
        print(f"Action: {step_name}")
        print(f"{'='*60}")
        
        # Preparation countdown
        print("\nPrepare to click in:")
        for i in range(5, 0, -1):
            print(f"  {i}...", end='', flush=True)
            time.sleep(1)
        
        print("\n\n🎯 CLICK on the target element now!")
        
        # Reset click detection
        self.click_detected = False
        
        # Start mouse listener
        with mouse.Listener(on_click=self.on_click) as listener:
            # Wait for click (max 10 seconds)
            start_time = time.time()
            while not self.click_detected and (time.time() - start_time) < 10:
                time.sleep(0.1)
        
        if self.click_detected:
            coordinate_data = {
                "step": step_index + 1,
                "name": step_name,
                "x": self.last_x,
                "y": self.last_y,
                "timestamp": datetime.now().isoformat()
            }
            
            self.coordinates.append(coordinate_data)
            print(f"\n✅ Captured: {step_name}")
            print(f"   Coordinates: ({self.last_x}, {self.last_y})")
            return True
        else:
            print("\n⏭️  No click detected within 10 seconds, skipping...")
            return False
    
    def save_coordinates(self):
        """Save captured coordinates to JSON file"""
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        filename = os.path.join(data_dir, f"moonshot_coordinates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        output = {
            "app": "Moonshot",
            "capture_date": datetime.now().isoformat(),
            "total_steps": len(self.coordinates),
            "coordinates": self.coordinates
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Coordinates saved to: {filename}")
        
        # Also print summary
        print("\n📋 Captured Coordinates Summary:")
        print("="*60)
        for coord in self.coordinates:
            print(f"{coord['step']:2d}. {coord['name']:<40} ({coord['x']}, {coord['y']})")
        
        return filename
    
    def start(self):
        """Start the coordinate capture process"""
        print("🎯 Moonshot Coordinate Capture Tool - Click Version")
        print("="*60)
        print("This tool captures mouse coordinates when you click.")
        print("\nHOW IT WORKS:")
        print("1. You'll have 5 seconds to prepare for each step")
        print("2. Click on the target element when prompted")
        print("3. The tool will automatically move to the next step")
        print("\nIMPORTANT:")
        print("- Make sure Moonshot app is open and visible")
        print("- Click directly on the target element")
        print("- You have 10 seconds to click after the prompt")
        print("="*60)
        
        input("\nPress Enter to start capturing coordinates...")
        
        # Capture each step
        for i in range(len(self.steps)):
            self.capture_step(i)
            
            # Small delay between steps
            if i < len(self.steps) - 1:
                time.sleep(1)
        
        print("\n🎉 Capture session complete!")
        
        if self.coordinates:
            return self.save_coordinates()
        else:
            print("\n⚠️  No coordinates were captured")
            return None

if __name__ == "__main__":
    capture = ClickCoordinateCapture()
    capture.start()