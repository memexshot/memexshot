import os
import json
import time
import asyncio
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from solana.rpc.api import Client
from solders.pubkey import Pubkey
import tweepy
from supabase import create_client, Client as SupabaseClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
WALLET_ADDRESS = os.getenv("MONITOR_WALLET_ADDRESS")
HELIUS_RPC = os.getenv("HELIUS_RPC_URL")
METEORA_DBC_PROGRAM = "dbcij3LWUppWqq96dh6gJWwBifmcGfLSB5D4DuSMaqN"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

# Supabase setup
supabase: SupabaseClient = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Solana connection
solana_client = Client(HELIUS_RPC)

# Twitter accounts configuration
TWITTER_ACCOUNTS = []
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")

# Initialize Twitter clients (v2 API)
# Ana hesap
if os.getenv("TWITTER_ACCESS_TOKEN") and os.getenv("TWITTER_ACCESS_TOKEN_SECRET"):
    # Create v2 client
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    
    TWITTER_ACCOUNTS.append({
        "name": "main_account",
        "client": client,
        "daily_limit": 100,
        "daily_count": 0,
        "last_reset": datetime.now().date(),
        "last_tweet_time": None
    })

# Diğer hesaplar
for i in range(1, 3):
    access_token = os.getenv(f"TWITTER_{i}_ACCESS_TOKEN")
    access_secret = os.getenv(f"TWITTER_{i}_ACCESS_TOKEN_SECRET")
    
    if access_token and access_secret:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        TWITTER_ACCOUNTS.append({
            "name": f"account{i}",
            "client": client,
            "daily_limit": 100,
            "daily_count": 0,
            "last_reset": datetime.now().date(),
            "last_tweet_time": None
        })

# Track processed signatures
processed_signatures = set()

def check_if_meteora_swap(tx_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check if transaction is a Meteora swap with 5 USDC"""
    try:
        # Check if Meteora program is involved
        has_meteora = False
        if 'transaction' in tx_dict and 'message' in tx_dict['transaction']:
            # Check account keys
            account_keys = tx_dict['transaction']['message'].get('accountKeys', [])
            for key in account_keys:
                if isinstance(key, str) and key == METEORA_DBC_PROGRAM:
                    has_meteora = True
                    break
                elif isinstance(key, dict) and key.get('pubkey') == METEORA_DBC_PROGRAM:
                    has_meteora = True
                    break
            
            # Check instructions
            instructions = tx_dict['transaction']['message'].get('instructions', [])
            for inst in instructions:
                if isinstance(inst, dict) and inst.get('programId') == METEORA_DBC_PROGRAM:
                    has_meteora = True
                    break
        
        if not has_meteora:
            return None
        
        # Check for 5 USDC swap in inner instructions
        swap_info = None
        if 'meta' in tx_dict and 'innerInstructions' in tx_dict['meta']:
            for inner_group in tx_dict['meta']['innerInstructions']:
                if isinstance(inner_group, dict) and 'instructions' in inner_group:
                    for inner_inst in inner_group['instructions']:
                        if isinstance(inner_inst, dict) and 'parsed' in inner_inst:
                            parsed = inner_inst['parsed']
                            if isinstance(parsed, dict) and parsed.get('type') == 'transferChecked':
                                info = parsed.get('info', {})
                                amount = info.get('tokenAmount', {}).get('uiAmount')
                                mint = info.get('mint')
                                
                                if mint == USDC_MINT and amount and 4.9 < float(amount) < 5.1:
                                    swap_info = {
                                        'usdc_amount': float(amount),
                                        'has_5_usdc': True
                                    }
        
        return swap_info
    except Exception as e:
        print(f"Error checking Meteora swap: {e}")
        return None

def extract_moon_token_from_swap(tx_dict: Dict[str, Any], block_time: int) -> Optional[Dict[str, Any]]:
    """Extract moon token information from Meteora swap transaction"""
    try:
        # Get timestamp
        timestamp = datetime.fromtimestamp(block_time) if block_time else None
        
        # Look for moon tokens in post balances
        moon_tokens = []
        if 'meta' in tx_dict and 'postTokenBalances' in tx_dict['meta']:
            for balance in tx_dict['meta']['postTokenBalances']:
                if balance.get('owner') == WALLET_ADDRESS:
                    mint = balance.get('mint', '')
                    # Check if mint ends with 'moon'
                    if mint.endswith('moon'):
                        amount = balance.get('uiTokenAmount', {}).get('uiAmount', 0)
                        if amount > 0:
                            # Extract ticker from mint address
                            # Mint format: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXmoon
                            # We need to get the token metadata to find the ticker
                            ticker = extract_ticker_from_metadata(tx_dict, mint)
                            
                            moon_tokens.append({
                                'mint': mint,
                                'amount': amount,
                                'timestamp': timestamp,
                                'ticker': ticker
                            })
        
        # Return the first moon token found
        if moon_tokens:
            return moon_tokens[0]
        
        return None
    except Exception as e:
        print(f"Error extracting moon token: {e}")
        return None

def extract_ticker_from_metadata(tx_dict: Dict[str, Any], mint_address: str) -> Optional[str]:
    """Extract ticker from transaction metadata"""
    try:
        # Look in innerInstructions for metadata
        if 'meta' in tx_dict and 'innerInstructions' in tx_dict['meta']:
            for inner_group in tx_dict['meta']['innerInstructions']:
                if isinstance(inner_group, dict) and 'instructions' in inner_group:
                    for inst in inner_group['instructions']:
                        # Look for metadata in logs
                        if 'data' in inst and isinstance(inst['data'], str):
                            # Try to decode base58 data for metadata
                            continue
        
        # Look in logs for ticker information
        if 'meta' in tx_dict and 'logMessages' in tx_dict['meta']:
            for log in tx_dict['meta']['logMessages']:
                # Meteora logs often contain token info
                if 'Token:' in log or 'Symbol:' in log:
                    # Extract ticker from log
                    parts = log.split()
                    for i, part in enumerate(parts):
                        if part in ['Symbol:', 'Ticker:', 'Token:'] and i + 1 < len(parts):
                            ticker = parts[i + 1].strip(',').strip('"').strip("'")
                            if ticker and len(ticker) <= 10:  # Reasonable ticker length
                                return ticker.upper()
        
        # If not found in logs, try to parse from transaction data
        # Look for CreateMetadata instruction
        if 'transaction' in tx_dict and 'message' in tx_dict['transaction']:
            instructions = tx_dict['transaction']['message'].get('instructions', [])
            for inst in instructions:
                if isinstance(inst, dict) and 'parsed' in inst:
                    parsed = inst['parsed']
                    if isinstance(parsed, dict) and parsed.get('type') == 'createMetadataAccounts':
                        info = parsed.get('info', {})
                        symbol = info.get('symbol')
                        if symbol:
                            return symbol.upper()
        
        # If still not found, use Helius API to get metadata
        ticker = get_token_metadata_from_helius(mint_address)
        if ticker:
            return ticker.upper()
        
        return None
    except Exception as e:
        print(f"Error extracting ticker: {e}")
        return None

def get_token_metadata_from_helius(mint_address: str) -> Optional[str]:
    """Get token metadata from Helius API"""
    try:
        api_key = HELIUS_RPC.split('api-key=')[-1] if 'api-key=' in HELIUS_RPC else None
        if not api_key:
            return None
        
        url = f"https://api.helius.xyz/v0/token-metadata?api-key={api_key}"
        
        payload = {
            "mintAccounts": [mint_address],
            "includeOffChain": True,
            "disableCache": False
        }
        
        response = requests.post(url, json=payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                metadata = data[0]
                # First try onChainMetadata
                on_chain = metadata.get('onChainMetadata', {})
                if on_chain:
                    symbol = on_chain.get('metadata', {}).get('data', {}).get('symbol')
                    if symbol:
                        return symbol.strip()
                
                # Then try offChainMetadata
                off_chain = metadata.get('offChainMetadata', {})
                if off_chain:
                    symbol = off_chain.get('metadata', {}).get('symbol')
                    if symbol:
                        return symbol.strip()
        
        return None
    except Exception as e:
        print(f"Error getting metadata from Helius: {e}")
        return None

def reset_daily_counters():
    """Reset daily counters for all accounts"""
    today = datetime.now().date()
    
    for account in TWITTER_ACCOUNTS:
        if account["last_reset"] != today:
            account["daily_count"] = 0
            account["last_reset"] = today
            print(f"📅 Reset daily counter for {account['name']}")

def get_available_account() -> Optional[Dict]:
    """Get an available Twitter account that hasn't reached daily limit and waited 1 minute"""
    reset_daily_counters()
    
    now = datetime.now()
    
    for account in TWITTER_ACCOUNTS:
        # Check daily limit
        if account["daily_count"] >= account["daily_limit"]:
            continue
        
        # Check if 1 minute passed since last tweet
        if account["last_tweet_time"]:
            time_since_last = now - account["last_tweet_time"]
            if time_since_last < timedelta(minutes=1):
                continue
        
        return account
    
    return None

def build_reply_text(ticker: str, tx_signature: str) -> str:
    """Build the reply text for the tweet"""
    
    # Get custom message from env or use default
    reply_message = os.getenv("REPLY_MESSAGE", "Congratulations! You've just created a free meme coin using MoonXshot. Welcome to the launch club.")
    
    return f"""{reply_message}

📊 solscan.io/tx/{tx_signature}"""

async def send_twitter_reply(coin_data: Dict[str, Any], tx_signature: str):
    """Send Twitter reply for token creation"""
    
    # TEST MODE CHECK - Commented out to enable real tweets
    # test_mode = os.path.exists('tests/TEST_MODE_CHANGES.md')
    # if test_mode:
    #     print("\n⚠️  TEST MODE - Not sending actual tweet")
    #     print(f"📝 Would reply to: @{coin_data.get('twitter_user')} - Tweet {coin_data['tweet_id']}")
    #     print(f"🎯 Token: ${coin_data['ticker']}")
    #     return True, None
    
    try:
        # Get available account
        account = get_available_account()
        
        if not account:
            print("⚠️ All accounts at daily limit or waiting cooldown")
            return False, "No available account"
        
        # Build reply text
        reply_text = build_reply_text(coin_data['ticker'], tx_signature)
        
        print(f"\n📱 Sending reply using {account['name']}")
        print(f"💬 Reply to tweet: {coin_data['tweet_id']}")
        
        # Add username to reply text
        username = coin_data.get('twitter_user', '').replace('@', '')
        if username and not reply_text.startswith(f"@{username}"):
            reply_text = f"@{username} {reply_text}"
        
        print(f"📝 Reply text: {reply_text}")
        
        # Send reply using v2 API
        tweet_id_str = str(coin_data['tweet_id'])
        
        print(f"📝 Full reply text: {reply_text}")
        print(f"🔗 Replying to tweet ID: {tweet_id_str}")
        
        # Create tweet with reply - Basic plan doesn't need to read the original tweet
        response = account["client"].create_tweet(
            text=reply_text,
            in_reply_to_tweet_id=tweet_id_str
        )
        
        if response.data:
            print(f"✅ Reply sent successfully! Tweet ID: {response.data['id']}")
            
            # Update account counters
            account["daily_count"] += 1
            account["last_tweet_time"] = datetime.now()
            
            return True, None
        else:
            error_msg = "No response data from Twitter API"
            print(f"❌ Failed to send reply: {error_msg}")
            return False, error_msg
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error sending reply: {error_msg}")
        print(f"🔍 Error type: {type(e).__name__}")
        return False, error_msg

async def process_moon_token_swap(tx_signature: str, moon_token: Dict[str, Any]):
    """Process moon token swap and send tweet if matching coin found"""
    try:
        print(f"\n🌙 Processing moon token: {moon_token['mint']}")
        
        ticker = moon_token.get('ticker')
        if ticker:
            print(f"  🏷️  Extracted ticker: {ticker}")
        else:
            print(f"  ⚠️  Could not extract ticker from transaction")
            return
        
        # Look for coin by ticker
        print(f"  🔍 Looking for coin with ticker: {ticker}")
        
        result = supabase.table("coins").select("*").eq(
            "ticker", ticker
        ).order("created_at", desc=True).limit(1).execute()
        
        if not result.data:
            print(f"  ❌ No coin found with ticker: {ticker}")
            return
        
        coin = result.data[0]
        print(f"  📌 Found coin: {coin['ticker']} ({coin['name']})")
        print(f"     Status: {coin['status']}")
        print(f"     Tweet: @{coin['twitter_user']} - {coin['tweet_id']}")
        
        # Check if already replied
        existing_reply = supabase.table("twitter_reply_queue").select("*").eq(
            "tweet_id", coin['tweet_id']
        ).execute()
        
        if existing_reply.data:
            print("  ⚠️ Already replied to this tweet")
            return
        
        # Add to reply queue for tracking
        queue_data = {
            "coin_id": coin["id"],
            "tweet_id": coin["tweet_id"],
            "twitter_user": coin["twitter_user"],
            "ticker": coin["ticker"],
            "tx_signature": tx_signature,
            "token_mint": moon_token['mint'],
            "scheduled_at": datetime.now().isoformat(),
            "status": "sending"
        }
        
        queue_result = supabase.table("twitter_reply_queue").insert(queue_data).execute()
        
        # Send reply immediately
        success, error_msg = await send_twitter_reply(coin, tx_signature)
        
        if success:
            # Update queue status
            if queue_result.data:
                supabase.table("twitter_reply_queue").update({
                    "status": "sent",
                    "replied_at": datetime.now().isoformat()
                }).eq("id", queue_result.data[0]["id"]).execute()
        else:
            # Update queue status
            if queue_result.data:
                supabase.table("twitter_reply_queue").update({
                    "status": "failed",
                    "error_message": error_msg or "Failed to send tweet"
                }).eq("id", queue_result.data[0]["id"]).execute()
            
    except Exception as e:
        print(f"❌ Error processing moon token swap: {e}")

async def monitor_wallet():
    """Monitor wallet for Meteora swaps and process them"""
    print(f"🔍 Starting Wallet Monitor & Reply Bot")
    print(f"📍 Monitoring wallet: {WALLET_ADDRESS}")
    print(f"🐦 Twitter accounts loaded: {len(TWITTER_ACCOUNTS)}")
    
    for acc in TWITTER_ACCOUNTS:
        print(f"   ✓ {acc['name']}")
    
    print("\n" + "="*60 + "\n")
    
    global processed_signatures
    check_count = 0
    
    while True:
        try:
            check_count += 1
            if check_count % 10 == 1:  # Log every 10th check
                print(f"\n⏰ Check #{check_count} at {datetime.now().strftime('%H:%M:%S')}")
            
            # Get recent signatures for the wallet
            pubkey = Pubkey.from_string(WALLET_ADDRESS)
            
            # Get last 10 transactions
            signatures_resp = solana_client.get_signatures_for_address(
                pubkey,
                limit=10
            )
            
            # Handle new response format
            signatures = signatures_resp.value if hasattr(signatures_resp, 'value') else signatures_resp
            
            if signatures:
                # Process each transaction (reversed - oldest first)
                for sig_info in reversed(signatures):
                    signature = str(sig_info.signature)
                    
                    # Skip if already processed
                    if signature in processed_signatures:
                        continue
                    
                    # Only process recent transactions (last 30 minutes)
                    if hasattr(sig_info, 'block_time') and sig_info.block_time:
                        tx_time = datetime.fromtimestamp(sig_info.block_time)
                        if datetime.now() - tx_time > timedelta(minutes=30):
                            continue
                    
                    print(f"\n🔄 Checking transaction: {signature[:40]}...")
                    
                    # Get transaction details
                    try:
                        tx_resp = solana_client.get_transaction(
                            sig_info.signature,
                            encoding="jsonParsed",
                            max_supported_transaction_version=0
                        )
                        
                        if tx_resp and tx_resp.value:
                            # Convert to JSON
                            tx_json = tx_resp.value.to_json()
                            tx_dict = json.loads(tx_json)
                            
                            # Check if this is a Meteora swap
                            swap_info = check_if_meteora_swap(tx_dict)
                            if swap_info and swap_info.get('has_5_usdc'):
                                print(f"🎯 5 USDC Meteora swap detected!")
                                
                                # Extract moon token
                                block_time = sig_info.block_time if hasattr(sig_info, 'block_time') else None
                                moon_token = extract_moon_token_from_swap(tx_dict, block_time)
                                
                                if moon_token:
                                    print(f"🌙 Moon token found: {moon_token['mint']}")
                                    await process_moon_token_swap(signature, moon_token)
                                else:
                                    print("❌ No moon token found in swap")
                    except Exception as e:
                        print(f"Error processing transaction: {e}")
                    
                    # Mark as processed
                    processed_signatures.add(signature)
                
                # Memory optimization
                if len(processed_signatures) > 100:
                    processed_signatures = set(list(processed_signatures)[-50:])
            
            # Wait before next check
            await asyncio.sleep(30)  # Check every 30 seconds
            
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            await asyncio.sleep(30)

async def create_reply_queue_table():
    """Create reply queue table if not exists"""
    print("📋 Ensuring twitter_reply_queue table exists...")
    # Table should be created from database/twitter_reply_queue.sql

async def main():
    """Main function"""
    # Ensure reply queue table exists
    await create_reply_queue_table()
    
    # Start monitoring
    await monitor_wallet()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Shutting down Wallet Monitor & Reply Bot...")