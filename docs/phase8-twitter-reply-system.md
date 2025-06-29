# Phase 8: Twitter Reply System

## Overview
Phase 8 implements an automated Twitter reply system that responds to users after their tokens are successfully created. The system will send congratulatory messages with links to the created tokens on Moonshot, managing multiple Twitter accounts to bypass API rate limits.

## System Architecture

### 1. Core Components

#### Reply Bot Service
- Monitors Supabase for successful token creations
- Waits 1 minute after token creation before replying
- Manages reply queue and scheduling
- Handles multiple Twitter accounts rotation

#### Moonshot Integration
- Fetches token page URL from Moonshot
- Extracts token contract address
- Builds shareable links
- Handles API errors and retries

#### Multi-Account Management
- 3 Twitter accounts for 300 daily tweets capacity
- Round-robin account selection
- Rate limit tracking per account
- Account health monitoring

### 2. Database Schema

#### twitter_accounts table
```sql
CREATE TABLE twitter_accounts (
  id SERIAL PRIMARY KEY,
  account_name VARCHAR(255) NOT NULL,
  api_key VARCHAR(255) NOT NULL,
  api_secret VARCHAR(255) NOT NULL,
  access_token VARCHAR(255) NOT NULL,
  access_token_secret VARCHAR(255) NOT NULL,
  daily_tweet_count INTEGER DEFAULT 0,
  last_reset_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### reply_queue table
```sql
CREATE TABLE reply_queue (
  id SERIAL PRIMARY KEY,
  coin_id INTEGER REFERENCES coins(id),
  tweet_id VARCHAR(255) NOT NULL,
  twitter_user VARCHAR(255) NOT NULL,
  ticker VARCHAR(10) NOT NULL,
  moonshot_url VARCHAR(255),
  scheduled_at TIMESTAMP NOT NULL,
  status VARCHAR(50) DEFAULT 'pending', -- pending, sent, failed
  twitter_account_id INTEGER REFERENCES twitter_accounts(id),
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### 3. Reply Message Template

**English Template:**
```
🎉 Congratulations! You've created a free token on @moonshotdotcc!

🚀 $[TICKER] is now live!
👉 [MOONSHOT_URL]

Created with ❤️ by memeXshot - Free token creation for the Solana community
```

### 4. Implementation Flow

1. **Token Creation Success Trigger**
   - Supabase webhook on coins table when status = 'completed'
   - Extract coin details and original tweet information
   - Schedule reply for created_at + 1 minute

2. **Moonshot URL Fetching**
   - Use token contract address to build Moonshot URL
   - Pattern: `https://moonshot.money/token/solana/[CONTRACT_ADDRESS]`
   - Verify URL accessibility before posting

3. **Account Selection Algorithm**
   ```javascript
   function selectTwitterAccount() {
     // Reset daily counts if needed
     // Select account with lowest usage today
     // Return null if all accounts at limit
   }
   ```

4. **Reply Posting**
   - Select available Twitter account
   - Post reply to original tweet
   - Update reply_queue status
   - Increment account daily counter

5. **Error Handling**
   - Retry failed replies with exponential backoff
   - Switch accounts on rate limit errors
   - Log all errors for monitoring

### 5. Rate Limit Management

#### Daily Reset Logic
- Reset counters at UTC midnight
- Store last reset timestamp per account
- Prevent double-counting on restarts

#### Account Rotation
- Priority queue based on usage count
- Skip accounts at daily limit (100)
- Alert when approaching global limit (300)

### 6. Monitoring & Analytics

#### Metrics to Track
- Daily replies sent per account
- Success/failure rates
- Average response time
- Moonshot URL fetch success rate

#### Alerts
- Account approaching limit (90 tweets)
- All accounts at limit
- High failure rate (>10%)
- Moonshot API issues

### 7. Configuration

#### Environment Variables
```env
# Twitter Account 1
TWITTER_1_API_KEY=
TWITTER_1_API_SECRET=
TWITTER_1_ACCESS_TOKEN=
TWITTER_1_ACCESS_TOKEN_SECRET=

# Twitter Account 2
TWITTER_2_API_KEY=
TWITTER_2_API_SECRET=
TWITTER_2_ACCESS_TOKEN=
TWITTER_2_ACCESS_TOKEN_SECRET=

# Twitter Account 3
TWITTER_3_API_KEY=
TWITTER_3_API_SECRET=
TWITTER_3_ACCESS_TOKEN=
TWITTER_3_ACCESS_TOKEN_SECRET=

# Moonshot Configuration
MOONSHOT_BASE_URL=https://moonshot.money/token/solana/

# Reply Configuration
REPLY_DELAY_MINUTES=1
MAX_RETRIES=3
RETRY_DELAY_SECONDS=30
```

### 8. Security Considerations

- Encrypt Twitter API credentials in database
- Use environment variables for sensitive data
- Implement request signing for webhooks
- Rate limit webhook endpoints
- Monitor for abuse patterns

### 9. Deployment Strategy

#### Supabase Edge Functions
- Deploy reply scheduler as edge function
- Triggered by database changes
- Handles scheduling and queuing

#### Worker Service
- Separate service for posting replies
- Polls reply_queue for pending items
- Manages Twitter API interactions

### 10. Testing Strategy

- Mock Twitter API responses
- Test account rotation logic
- Verify rate limit handling
- Test Moonshot URL generation
- Simulate various failure scenarios

## Technical Requirements

### Dependencies
- Twitter API v2 SDK
- Supabase client
- Node.js scheduled jobs (node-cron)
- Retry mechanism (p-retry)
- URL validation library

### Infrastructure
- Supabase database
- Edge functions
- Worker service (Node.js)
- Monitoring service
- Error tracking (Sentry)

## Success Metrics

- 95%+ reply success rate
- <2 minute average reply time
- Zero rate limit violations
- 100% Moonshot URL accuracy
- <1% user complaint rate

## Future Enhancements

- Add language detection for multi-language replies
- Include token performance metrics in replies
- Add GIF/image attachments
- Implement A/B testing for reply templates
- Add referral tracking links

## Status: READY TO IMPLEMENT 🚀

Phase 8 documentation complete. Ready to begin implementation of the Twitter reply system with multi-account support and Moonshot integration.