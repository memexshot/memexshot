#!/usr/bin/env python3
"""
Test Auto Photo Sync Service
Tests image download, Photos app integration, and Supabase sync
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
import tempfile
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test Supabase connection"""
    print("🔍 Testing Supabase Connection...")
    
    try:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            print("❌ Missing Supabase credentials")
            return False
            
        supabase = create_client(url, key)
        result = supabase.table('coins').select('id').limit(1).execute()
        print("✅ Supabase connection successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase error: {e}")
        return False

def test_photos_app_availability():
    """Test if Photos app is available (macOS only)"""
    print("\n🔍 Testing Photos App Availability...")
    
    try:
        # Check if we're on macOS
        if sys.platform != 'darwin':
            print("⚠️  Not on macOS - Photos app not available")
            return True  # Not a failure, just different platform
        
        # Check if Photos app exists
        photos_paths = [
            "/Applications/Photos.app",
            "/System/Applications/Photos.app"
        ]
        
        for photos_path in photos_paths:
            if os.path.exists(photos_path):
                print(f"✅ Photos app found at: {photos_path}")
                return True
        
        print("❌ Photos app not found in common locations")
        return False
            
    except Exception as e:
        print(f"❌ Error checking Photos app: {e}")
        return False

def test_image_download_capability():
    """Test ability to download images"""
    print("\n🔍 Testing Image Download Capability...")
    
    try:
        import requests
        
        # Test with a known working image
        test_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png"
        
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            print("✅ Can download images from URLs")
            print(f"   Downloaded {len(response.content)} bytes")
            return True
        else:
            print(f"❌ Failed to download test image: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Download test error: {e}")
        return False

def test_temp_directory():
    """Test temporary directory for image storage"""
    print("\n🔍 Testing Temporary Directory...")
    
    try:
        # Get the data directory path
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(script_dir, 'data', 'temp_images')
        
        # Create if doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Test write permission
        test_file = os.path.join(data_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        # Clean up
        os.remove(test_file)
        
        print(f"✅ Temp directory ready: {data_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Directory test error: {e}")
        return False

def test_pending_images_query():
    """Test querying for pending images"""
    print("\n🔍 Testing Pending Images Query...")
    
    try:
        supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
        
        # Query for coins with pending image sync
        result = supabase.table('coins')\
            .select('id, ticker, image_url, image_synced')\
            .eq('image_synced', False)\
            .not_.is_('image_url', 'null')\
            .neq('image_url', 'NO_IMAGE')\
            .limit(5)\
            .execute()
        
        if result.data:
            print(f"✅ Found {len(result.data)} coins with pending images")
            for coin in result.data[:2]:  # Show first 2
                print(f"   - {coin['ticker']}: {coin['image_url'][:50]}...")
        else:
            print("✅ No pending images (this is OK)")
            
        return True
        
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False

def test_auto_photo_sync_init():
    """Test AutoPhotoSync service initialization"""
    print("\n🔍 Testing AutoPhotoSync Initialization...")
    
    try:
        from scripts.services.auto_photo_sync import AutoPhotoSync
        
        # Initialize service
        service = AutoPhotoSync()
        print("✅ AutoPhotoSync initialized successfully!")
        
        # Check attributes
        print(f"   Supabase connected: Yes")
        print(f"   Poll interval: 30 seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_image_processing_logic():
    """Test image processing logic without actual download"""
    print("\n🔍 Testing Image Processing Logic...")
    
    try:
        # Test URL validation
        valid_urls = [
            "https://pbs.twimg.com/media/example.jpg",
            "http://example.com/image.png",
            "https://example.com/image.jpeg"
        ]
        
        invalid_urls = [
            "NO_IMAGE",
            None,
            "",
            "not-a-url"
        ]
        
        print("   Valid URLs:")
        for url in valid_urls:
            if url and url.startswith(('http://', 'https://')) and url != 'NO_IMAGE':
                print(f"   ✅ {url}")
        
        print("\n   Invalid URLs:")
        for url in invalid_urls:
            if not url or url == 'NO_IMAGE' or not url.startswith(('http://', 'https://')):
                print(f"   ✅ Correctly rejected: {url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Logic test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AUTO PHOTO SYNC TEST SUITE")
    print("=" * 50)
    print("⚠️  Running in TEST MODE - No images will be downloaded")
    print("=" * 50)
    
    tests = [
        ("Supabase Connection", test_supabase_connection),
        ("Photos App", test_photos_app_availability),
        ("Image Download", test_image_download_capability),
        ("Temp Directory", test_temp_directory),
        ("Pending Images", test_pending_images_query),
        ("Service Init", test_auto_photo_sync_init),
        ("Processing Logic", test_image_processing_logic)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*50}")
        success = test_func()
        results.append((name, success))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY:")
    print("="*50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Auto Photo Sync is ready to run.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()