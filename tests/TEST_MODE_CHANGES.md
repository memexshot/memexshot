# TEST MODE CHANGES

## ⚠️ IMPORTANT: These changes are for testing only!

### Modified Files and Parameters:

#### 1. Twitter Bot (`services/twitter_bot.py`)

#### 2. Queue Worker (`services/queue_worker.py`)

**Original Values:**
- Line 60: `.gte('followers_count', 500)` - Minimum 500 followers required

**TEST Values:**
- Line 60: Removed follower check - processes all queued tweets

#### 3. Supabase Listener (`automation/supabase_listener_polling.py`)

**Original Values:**
- Line 190: `input("\nPress Enter to start listener...")` - Waits for user input

**TEST Values:**
- Line 191: `print("\n🚀 Starting automatically (TEST MODE)...")` - Starts automatically

**Original Values:**
- Line 60: `.gte('followers_count', 500)` - Minimum 500 followers required

**TEST Values:**
- Line 60: Removed follower check - processes all queued tweets

**Original Values:**
- Search Pattern: `Launch $TICKER @memeXshot`
- Minimum Followers: 500
- Search Keyword: "Launch"
- Description: 'Bu token memeXshot aracılığı ile Moonshot\'ta create edildi'
- Website: Actual tweet URL
- Twitter: Actual user @handle

**TEST Values:**
- Search Pattern: `Perfecto $TICKER @memeXshot`
- Minimum Followers: 0 (disabled)
- Search Keyword: "Perfecto"
- Description: 'TEST MODE - This is a test token'
- Website: 'https://example.com'
- Twitter: '@testuser'
- Max Daily Per User: 99 (was 3)

**Lines Changed:**
- Line 40: `self.min_followers = 0  # TEST MODE: Disabled follower check`
- Line 123: `pattern = rf'Perfecto\s+\$?([A-Za-z0-9]+)\s+@{self.bot_username}'`
- Line 242: `query = f'"Perfecto" "@{self.bot_username}" -is:retweet has:images'`
- Line 325: `self.log(f"🔍 TEST MODE: Monitoring for: Perfecto @{self.bot_username}")`
- Line 182-184: Test mode dummy data for queue
- Line 224-226: Test mode dummy data for rejected queue

### How to Revert:

```bash
# Option 1: Git revert (if using git)
git checkout services/twitter_bot.py

# Option 2: Manual revert
# Change the following back:
- Line 40: self.min_followers = int(os.getenv('MIN_FOLLOWERS', '500'))
- Line 123: pattern = rf'Launch\s+\$?([A-Za-z0-9]+)\s+@{self.bot_username}'
- Line 242: query = f'"{self.search_keyword}" "@{self.bot_username}" -is:retweet has:images'
- Line 325: self.log(f"🔍 Monitoring for: {self.search_keyword} @{self.bot_username}")
- Line 182: 'description': 'Bu token memeXshot aracılığı ile Moonshot\'ta create edildi',
- Line 183: 'website': tweet_url,
- Line 184: 'twitter': f"@{author or tweet.author_id}",
- Line 224: 'description': 'Bu token memeXshot aracılığı ile Moonshot\'ta create edildi',
- Line 225: 'website': tweet_url,
- Line 226: 'twitter': f"@{author}",
```

### Test Tweet Format:
```
Perfecto $TEST @memeXshot
```
+ Add an image

### Services to Start:
1. `python3 services/twitter_bot.py`
2. `python3 services/queue_worker.py`
3. `python3 services/auto_photo_sync.py`
4. `python3 services/photos_library_watcher.py`

### Database Cleanup Commands:
```sql
-- Clear tweet_queue
DELETE FROM tweet_queue;

-- Clear coins table
DELETE FROM coins;
```