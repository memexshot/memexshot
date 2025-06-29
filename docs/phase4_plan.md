# 🐦 Moonshot Automation - Phase 4 Implementation Plan

## 📋 Phase 4 Overview: Twitter Bot Integration

### 🎯 Goal
Create a Twitter bot that monitors mentions and automatically creates tokens based on user requests.

### 🔄 Architecture Overview

```
Twitter Mention → Bot Parser → Tweet Queue → Coins Table → Photo Sync → Automation
     ↓
Extract: @bot create TOKEN "Name" [image]
```

## 🏗️ System Components

### 1. **Twitter Bot Service** (New)
- **Purpose**: Monitor Twitter mentions and parse requests
- **Location**: `/services/twitter_bot.py`
- **Functionality**:
  - Stream Twitter mentions
  - Parse token creation requests
  - Extract images from tweets
  - Queue management
  - Rate limiting

### 2. **Tweet Queue System** (New)
- **Purpose**: Manage tweet processing queue
- **Tables**:
  - `tweet_queue`: Incoming requests
  - `coins`: Active processing (existing)
- **Benefits**:
  - Prevents overlapping processes
  - Maintains order (FIFO)
  - Handles high volume

## 📊 Database Schema

### Tweet Queue Table
```sql
CREATE TABLE tweet_queue (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tweet_id VARCHAR(50) UNIQUE NOT NULL,
    twitter_user VARCHAR(50) NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    twitter_handle VARCHAR(50),
    image_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'queued',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_tweet_queue_status ON tweet_queue(status);
CREATE INDEX idx_tweet_queue_created ON tweet_queue(created_at);
```

### User Limits Table
```sql
CREATE TABLE user_limits (
    twitter_user VARCHAR(50) PRIMARY KEY,
    daily_count INTEGER DEFAULT 0,
    last_reset DATE DEFAULT CURRENT_DATE,
    total_tokens INTEGER DEFAULT 0
);
```

## 🐦 Twitter Bot Requirements

### 1. **Twitter API Setup**
- Twitter Developer Account
- API v2 Access
- Bearer Token
- Stream Rules

### 2. **Tweet Format**
```
@MoonshotBot create TOKEN "Token Name" 
Description: Your token description
Website: https://example.com
[Attach Image]
```

### Alternative Formats:
```
@MoonshotBot TOKEN | Token Name | Description | website.com
@MoonshotBot #create TOKEN "Token Name" [image]
```

### 3. **Parsing Logic**
```python
# Extract components
- Ticker: Uppercase, alphanumeric, 3-10 chars
- Name: Quoted string or until delimiter
- Description: Optional, after "Description:"
- Website: URL detection
- Image: First media attachment
```

## 🔧 Implementation Steps

### Step 1: Twitter API Integration
```python
# Using Tweepy
import tweepy

class TwitterBot:
    def __init__(self):
        self.client = tweepy.Client(bearer_token=BEARER_TOKEN)
        self.stream = tweepy.StreamingClient(BEARER_TOKEN)
```

### Step 2: Queue Management
```python
# Process flow
1. Receive mention
2. Validate format
3. Check user limits
4. Add to tweet_queue
5. Queue worker moves to coins when ready
```

### Step 3: Rate Limiting
- Per user: 3 tokens/day
- Global: 100 tokens/day
- VIP users: Custom limits

## 🚦 Process Flow

### 1. **Tweet Reception**
```
User tweets → Bot receives → Parse & Validate
                ↓ Invalid
            Reply with error
```

### 2. **Queue Processing**
```
Valid tweet → tweet_queue (status: queued)
                ↓
Queue Worker → Check if coins table has active
                ↓ No active
            Move to coins → Update status: processing
```

### 3. **Success Flow**
```
Token created → Update tweet_queue (status: completed)
                ↓
            Reply to user with success
```

## ⚙️ Configuration

### Environment Variables
```bash
# Twitter API
TWITTER_BEARER_TOKEN=xxx
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
TWITTER_ACCESS_TOKEN=xxx
TWITTER_ACCESS_TOKEN_SECRET=xxx

# Bot Settings
BOT_USERNAME=MoonshotBot
MAX_DAILY_PER_USER=3
MAX_DAILY_GLOBAL=100
```

## 🛡️ Security & Validation

### 1. **Input Validation**
- Ticker: Only A-Z, 0-9
- Name: Max 100 chars
- Description: Max 500 chars
- Image: Max 5MB, JPG/PNG only

### 2. **Spam Prevention**
- Rate limiting
- Duplicate detection
- Blacklist management
- Minimum follower count

### 3. **Error Handling**
- Invalid format → Reply with instructions
- Rate limit → Reply with limit info
- System error → Log and notify admin

## 📈 Monitoring

### Metrics to Track
- Tweets processed/hour
- Success rate
- Average processing time
- User engagement
- Error types

### Logging
```
/logs/twitter_bot.log
/logs/queue_worker.log
/logs/rate_limiter.log
```

## 🚀 Deployment Plan

### Phase 4.1: Basic Bot
- Monitor mentions
- Parse simple format
- Manual queue processing

### Phase 4.2: Advanced Features
- Multiple format support
- Auto-replies
- Statistics command

### Phase 4.3: Scale & Optimize
- Multi-worker support
- Redis queue
- Analytics dashboard

## 📝 Example Interactions

### Success Case
```
@user: @MoonshotBot create GALAXY "Galaxy Token" [image]
@MoonshotBot: ✅ Token creation started for GALAXY! 
              Track progress: [link]
              
[After completion]
@MoonshotBot: 🎉 GALAXY token created successfully!
              View on Moonshot: [link]
```

### Error Cases
```
@user: @MoonshotBot create X
@MoonshotBot: ❌ Invalid format. Use:
              @MoonshotBot create TICKER "Name" [image]
              
@user: @MoonshotBot create MOON "Moon Token" [image]
@MoonshotBot: ⏳ Daily limit reached (3/3). 
              Try again tomorrow!
```

## 🔄 Future Enhancements

1. **Telegram Bot** - Multi-platform support
2. **Web Dashboard** - User token management
3. **NFT Integration** - Automatic NFT minting
4. **Analytics API** - Token performance data
5. **Governance** - Community voting

---

**Phase 4 Start Date**: TBD  
**Estimated Duration**: 1 week  
**Status**: Planning Complete ✅