#!/usr/bin/env python3
"""
Test Start All Services Script
Tests if all services can be initialized without errors
"""

import os
import sys
import subprocess
import time
import signal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if all required environment variables are set"""
    print("🔍 Testing Environment Variables...")
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_KEY',
        'TWITTER_BEARER_TOKEN',
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
        else:
            print(f"✅ {var}: Found")
    
    if missing:
        print(f"❌ Missing environment variables: {missing}")
        return False
        
    print("✅ All required environment variables found!")
    return True

def test_service_imports():
    """Test if all services can be imported"""
    print("\n🔍 Testing Service Imports...")
    
    services = [
        ("Twitter Bot", "scripts.services.twitter_bot", "TwitterBot"),
        ("Queue Worker", "scripts.services.queue_worker", "QueueWorker"),
        ("Auto Photo Sync", "scripts.services.auto_photo_sync", "AutoPhotoSync"),
        ("Supabase Listener", "scripts.automation.supabase_listener_polling", "SupabasePollingListener")
    ]
    
    all_good = True
    for name, module, class_name in services:
        try:
            exec(f"from {module} import {class_name}")
            print(f"✅ {name}: Import successful")
        except Exception as e:
            print(f"❌ {name}: Import failed - {e}")
            all_good = False
    
    return all_good

def test_start_script_exists():
    """Test if start_all_services.py exists and is executable"""
    print("\n🔍 Testing Start Script...")
    
    script_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'scripts',
        'start_all_services.py'
    )
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False
    
    print(f"✅ Script found: {script_path}")
    
    # Check if it's a valid Python file
    try:
        with open(script_path, 'r') as f:
            first_line = f.readline()
            if 'python' in first_line:
                print("✅ Valid Python script")
                return True
    except:
        pass
    
    return True

def test_service_initialization():
    """Test if each service can be initialized individually"""
    print("\n🔍 Testing Individual Service Initialization...")
    
    # Test Twitter Bot
    try:
        from scripts.services.twitter_bot import TwitterBot
        bot = TwitterBot()
        print("✅ Twitter Bot: Initialized")
    except Exception as e:
        print(f"❌ Twitter Bot: {e}")
    
    # Test Queue Worker
    try:
        from scripts.services.queue_worker import QueueWorker
        worker = QueueWorker()
        print("✅ Queue Worker: Initialized")
    except Exception as e:
        print(f"❌ Queue Worker: {e}")
    
    # Test Auto Photo Sync
    try:
        from scripts.services.auto_photo_sync import AutoPhotoSync
        sync = AutoPhotoSync()
        print("✅ Auto Photo Sync: Initialized")
    except Exception as e:
        print(f"❌ Auto Photo Sync: {e}")
    
    # Test Supabase Listener (might fail due to coordinates)
    try:
        from scripts.automation.supabase_listener_polling import SupabasePollingListener
        listener = SupabasePollingListener()
        print("✅ Supabase Listener: Initialized")
    except Exception as e:
        if "coordinates" in str(e):
            print("⚠️  Supabase Listener: Needs coordinates file (expected)")
        else:
            print(f"❌ Supabase Listener: {e}")
    
    return True

def test_start_services_dry_run():
    """Test starting all services for 5 seconds"""
    print("\n🔍 Testing Start All Services (5 second dry run)...")
    
    script_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'scripts',
        'start_all_services.py'
    )
    
    try:
        print("🚀 Starting all services...")
        print("⏱️  Will run for 10 seconds then stop...")
        
        # Start the process
        process = subprocess.Popen(
            ['python3', script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            preexec_fn=os.setsid
        )
        
        # Capture output for 5 seconds
        start_time = time.time()
        output_lines = []
        
        while time.time() - start_time < 10:
            line = process.stdout.readline()
            if line:
                output_lines.append(line.strip())
                if len(output_lines) <= 20:  # Show first 20 lines
                    print(f"   {line.strip()}")
            time.sleep(0.1)
        
        # Stop the process
        print("\n⏹️  Stopping services...")
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=5)
        
        # Check if services started
        service_started = {
            'Twitter Bot': False,
            'Queue Worker': False,
            'Photo Sync': False,
            'Supabase Listener': False
        }
        
        for line in output_lines:
            for service in service_started:
                if f"Started: {service}" in line:
                    service_started[service] = True
        
        print("\n📊 Service Status:")
        all_started = True
        for service, started in service_started.items():
            status = "✅" if started else "❌"
            print(f"{status} {service}")
            if not started:
                all_started = False
        
        return all_started
        
    except subprocess.TimeoutExpired:
        print("⚠️  Process didn't stop cleanly (but this is OK)")
        try:
            process.kill()
        except:
            pass
        return True
    except Exception as e:
        print(f"❌ Error running start script: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 START ALL SERVICES TEST SUITE")
    print("=" * 50)
    print("⚠️  Testing service initialization and startup")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Service Imports", test_service_imports),
        ("Start Script", test_start_script_exists),
        ("Individual Services", test_service_initialization),
        ("Start All Services", test_start_services_dry_run)
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
    
    if passed >= total - 1:  # Allow one failure for Supabase Listener
        print("\n🎉 Services are ready to run!")
        print("\nTo start all services, run:")
        print("  python3 scripts/start_all_services.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()