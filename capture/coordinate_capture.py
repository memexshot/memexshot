#!/usr/bin/env python3
"""
Moonshot App Coordinate Capture Tool
Captures mouse click coordinates for form automation
"""

import time
import json
import os
from datetime import datetime
import Quartz

class CoordinateCapture:
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
            "macOS password dialog (wait for you to enter)",
            "Close button (X - top right)",
            "Create button again (bottom menu - cycle complete)"
        ]
        
    def get_mouse_position(self):
        """Get current mouse position"""
        event = Quartz.CGEventCreate(None)
        location = Quartz.CGEventGetLocation(event)
        return int(location.x), int(location.y)
    
    def wait_for_click(self, timeout=5):
        """Wait for mouse click with timeout"""
        print("\n🎯 Click on the target element...")
        
        # Get initial position
        initial_x, initial_y = self.get_mouse_position()
        
        # Wait for position change (indicates click)
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_x, current_y = self.get_mouse_position()
            
            # Check if mouse button is pressed
            event = Quartz.CGEventCreate(None)
            if Quartz.CGEventGetIntegerValueField(event, Quartz.kCGMouseEventClickState) > 0:
                return current_x, current_y
            
            time.sleep(0.1)
        
        return None, None
    
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
        
        # Capture click
        x, y = self.wait_for_click()
        
        if x is not None and y is not None:
            coordinate_data = {
                "step": step_index + 1,
                "name": step_name,
                "x": x,
                "y": y,
                "timestamp": datetime.now().isoformat()
            }
            self.coordinates.append(coordinate_data)
            print(f"\n✅ Captured: {step_name}")
            print(f"   Coordinates: ({x}, {y})")
            return True
        else:
            print("\n⏭️  No click detected, skipping this step")
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
    
    def start(self):
        """Start the coordinate capture process"""
        print("🎯 Moonshot Coordinate Capture Tool")
        print("="*60)
        print("This tool will capture mouse click coordinates for each form element.")
        print("Follow the on-screen instructions and click when prompted.")
        print("\nIMPORTANT:")
        print("- Make sure Moonshot app is open and visible")
        print("- Terminal needs Accessibility permissions")
        print("- You'll have 5 seconds to prepare for each click")
        print("- Then 5 seconds to perform the click")
        print("="*60)
        
        # Check for accessibility permissions
        if not self.check_accessibility():
            print("\n❌ Terminal does not have Accessibility permissions!")
            print("\nTo grant permissions:")
            print("1. Go to System Settings > Privacy & Security > Privacy")
            print("2. Select Accessibility from the left panel")
            print("3. Add Terminal to the list and enable it")
            print("4. You may need to restart Terminal")
            return
        
        input("\nPress Enter to start capturing coordinates...")
        
        # Capture each step
        for i in range(len(self.steps)):
            self.capture_step(i)
            
            # Small delay between steps
            if i < len(self.steps) - 1:
                time.sleep(1)
        
        print("\n🎉 Capture session complete!")
        
        if self.coordinates:
            self.save_coordinates()
        else:
            print("\n⚠️  No coordinates were captured")
    
    def check_accessibility(self):
        """Check if we have accessibility permissions"""
        # This is a basic check - we try to create an event
        try:
            event = Quartz.CGEventCreate(None)
            return event is not None
        except:
            return False

if __name__ == "__main__":
    capture = CoordinateCapture()
    capture.start()