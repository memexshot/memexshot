#!/usr/bin/env python3
"""
Test Wallet Monitor Reply Bot
Tests blockchain connection, wallet monitoring, and Twitter reply functionality
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if all required environment variables are set"""
    print("🔍 Testing Environment Variables...")
    
    required_vars = {
        'Blockchain': ['HELIUS_RPC_URL', 'MONITOR_WALLET_ADDRESS'],
        'Supabase': ['SUPABASE_URL', 'SUPABASE_KEY'],
        'Main Twitter': ['TWITTER_API_KEY', 'TWITTER_API_SECRET'],
        'Reply Bot 1': ['TWITTER_1_ACCESS_TOKEN', 'TWITTER_1_ACCESS_TOKEN_SECRET'],
        'Reply Bot 2': ['TWITTER_2_ACCESS_TOKEN', 'TWITTER_2_ACCESS_TOKEN_SECRET']
    }
    
    all_good = True
    for category, vars in required_vars.items():
        print(f"\n   {category}:")
        for var in vars:
            value = os.getenv(var)
            if value:
                if 'TOKEN' in var or 'SECRET' in var or 'KEY' in var:
                    print(f"   ✅ {var}: {'*' * 10}")
                else:
                    print(f"   ✅ {var}: {value[:50]}...")
            else:
                print(f"   ❌ {var}: Missing")
                all_good = False
    
    return all_good

def test_solana_connection():
    """Test Solana/Helius RPC connection"""
    print("\n🔍 Testing Solana/Helius Connection...")
    
    try:
        from solana.rpc.api import Client
        
        helius_url = os.getenv('HELIUS_RPC_URL')
        if not helius_url:
            print("❌ HELIUS_RPC_URL not found")
            return False
            
        # Create client
        client = Client(helius_url)
        
        # Test connection by getting slot
        result = client.get_slot()
        if result.value:
            print(f"✅ Connected to Helius RPC")
            print(f"   Current slot: {result.value}")
            return True
        else:
            print("❌ Failed to connect to Helius")
            return False
            
    except Exception as e:
        print(f"❌ Solana connection error: {e}")
        return False

def test_wallet_address():
    """Test if wallet address is valid"""
    print("\n🔍 Testing Wallet Address...")
    
    try:
        from solders.pubkey import Pubkey
        
        wallet = os.getenv('MONITOR_WALLET_ADDRESS')
        if not wallet:
            print("❌ MONITOR_WALLET_ADDRESS not found")
            return False
            
        # Try to create pubkey
        pubkey = Pubkey.from_string(wallet)
        print(f"✅ Valid wallet address: {wallet}")
        print(f"   Monitoring this wallet for swaps")
        
        return True
        
    except Exception as e:
        print(f"❌ Invalid wallet address: {e}")
        return False

def test_twitter_accounts():
    """Test Twitter reply bot accounts"""
    print("\n🔍 Testing Twitter Reply Bot Accounts...")
    
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ Main Twitter API credentials missing")
        return False
    
    accounts_tested = 0
    accounts_working = 0
    
    # Test each reply bot account
    for i in range(1, 3):  # Test account 1 and 2
        access_token = os.getenv(f'TWITTER_{i}_ACCESS_TOKEN')
        access_secret = os.getenv(f'TWITTER_{i}_ACCESS_TOKEN_SECRET')
        
        if access_token and access_secret:
            accounts_tested += 1
            try:
                # Create client
                client = tweepy.Client(
                    consumer_key=api_key,
                    consumer_secret=api_secret,
                    access_token=access_token,
                    access_token_secret=access_secret
                )
                
                # Test by getting user info
                me = client.get_me()
                if me and me.data:
                    print(f"✅ Reply Bot {i}: @{me.data.username}")
                    accounts_working += 1
                else:
                    print(f"❌ Reply Bot {i}: Could not verify")
                    
            except Exception as e:
                print(f"❌ Reply Bot {i}: {e}")
        else:
            print(f"⚠️  Reply Bot {i}: Not configured")
    
    print(f"\n   Summary: {accounts_working}/{accounts_tested} accounts working")
    return accounts_working > 0

def test_supabase_tables():
    """Test Supabase tables for reply system"""
    print("\n🔍 Testing Supabase Tables...")
    
    try:
        from supabase import create_client
        
        supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
        
        # Test coins table
        result = supabase.table('coins').select('id').limit(1).execute()
        print("✅ Coins table accessible")
        
        # Test twitter_reply_queue table
        try:
            result = supabase.table('twitter_reply_queue').select('id').limit(1).execute()
            print("✅ Twitter reply queue table accessible")
        except:
            print("⚠️  Twitter reply queue table not found (run complete_schema.sql)")
            
        return True
        
    except Exception as e:
        print(f"❌ Supabase error: {e}")
        return False

def test_wallet_monitor_initialization():
    """Test WalletMonitor initialization"""
    print("\n🔍 Testing Wallet Monitor Initialization...")
    
    try:
        from scripts.services.wallet_monitor_reply_bot import TWITTER_ACCOUNTS
        
        print(f"✅ Wallet Monitor module loaded")
        print(f"   Twitter accounts configured: {len(TWITTER_ACCOUNTS)}")
        
        # Show config
        wallet = os.getenv('MONITOR_WALLET_ADDRESS')
        reply_msg = os.getenv('REPLY_MESSAGE', 'Default message')
        
        print(f"\n   Configuration:")
        print(f"   Monitor wallet: {wallet[:20]}...")
        print(f"   Reply message: {reply_msg[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_reply_dry_run():
    """Test reply functionality without sending"""
    print("\n🔍 Testing Reply Logic (Dry Run)...")
    
    try:
        # Test data
        test_coin = {
            'ticker': 'TEST',
            'twitter_user': 'testuser',
            'tweet_id': '1234567890'
        }
        test_tx = 'ABC123DEF456GHI789'
        
        # Build reply text
        reply_msg = os.getenv('REPLY_MESSAGE', 'Congratulations! You\'ve just created a free meme coin using MoonXshot. Welcome to the launch club.')
        reply_text = f"@{test_coin['twitter_user']} {reply_msg}\n\n📊 solscan.io/tx/{test_tx}"
        
        print("✅ Reply text builder working")
        print(f"\n   Sample reply:")
        print(f"   {'-'*50}")
        print(f"   {reply_text}")
        print(f"   {'-'*50}")
        
        return True
        
    except Exception as e:
        print(f"❌ Reply logic error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 WALLET MONITOR REPLY BOT TEST SUITE")
    print("=" * 50)
    print("⚠️  Running in TEST MODE - No tweets will be sent")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Solana Connection", test_solana_connection),
        ("Wallet Address", test_wallet_address),
        ("Twitter Accounts", test_twitter_accounts),
        ("Supabase Tables", test_supabase_tables),
        ("Monitor Init", test_wallet_monitor_initialization),
        ("Reply Logic", test_reply_dry_run)
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
        print("\n🎉 All tests passed! Wallet Monitor Reply Bot is ready to run.")
        print("\nTo start the bot, run:")
        print("  python3 scripts/services/wallet_monitor_reply_bot.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()