#!/usr/bin/env python3
"""
Moonshot App Coordinate Capture Tool - Simple Version
Captures mouse position when user presses Enter
"""

import time
import json
import os
from datetime import datetime
import Quartz

class SimpleCoordinateCapture:
    def __init__(self):
        self.coordinates = []
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
        
    def get_mouse_position(self):
        """Get current mouse position"""
        event = Quartz.CGEventCreate(None)
        location = Quartz.CGEventGetLocation(event)
        return int(location.x), int(location.y)
    
    def capture_step(self, step_index):
        """Capture coordinates for a single step"""
        step_name = self.steps[step_index]
        
        print(f"\n{'='*60}")
        print(f"Step {step_index + 1}/{len(self.steps)}")
        print(f"Action: {step_name}")
        print(f"{'='*60}")
        
        # Instructions
        print("\n📍 Position your mouse over the target element")
        print("   then press ENTER to capture the coordinates...")
        
        # Wait for Enter key
        input()
        
        # Capture current position
        x, y = self.get_mouse_position()
        
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
        
        # Small delay before next step
        time.sleep(0.5)
    
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
        print("🎯 Moonshot Coordinate Capture Tool - Simple Version")
        print("="*60)
        print("This tool captures mouse coordinates for each form element.")
        print("\nHOW IT WORKS:")
        print("1. Position your mouse over the target element")
        print("2. Press ENTER to capture the coordinates")
        print("3. Move to the next element and repeat")
        print("\nIMPORTANT:")
        print("- Make sure Moonshot app is open and visible")
        print("- Take your time to position the mouse accurately")
        print("="*60)
        
        input("\nPress Enter to start capturing coordinates...")
        
        # Capture each step
        for i in range(len(self.steps)):
            self.capture_step(i)
        
        print("\n🎉 Capture session complete!")
        
        if self.coordinates:
            return self.save_coordinates()
        else:
            print("\n⚠️  No coordinates were captured")
            return None

if __name__ == "__main__":
    capture = SimpleCoordinateCapture()
    capture.start()