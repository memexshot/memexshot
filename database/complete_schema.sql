-- ================================================
-- Moonshot Automation Complete Database Schema
-- ================================================
-- This file combines all tables and their final states
-- from all SQL files in the database directory.
-- Can be run on a fresh Supabase instance.
-- ================================================

-- ================================================
-- SECTION 1: TABLES
-- ================================================

-- --------------------------------
-- 1.1 COINS TABLE
-- --------------------------------
-- Main table for storing coin/token information
CREATE TABLE IF NOT EXISTS coins (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    twitter VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    error_message TEXT,
    
    -- Phase 3: Image management columns
    image_url VARCHAR(500),
    image_filename VARCHAR(255),
    image_synced BOOLEAN DEFAULT FALSE,
    image_sync_timestamp TIMESTAMP WITH TIME ZONE,
    twitter_user VARCHAR(50),
    tweet_id VARCHAR(50),
    
    -- Profile image support
    profile_image_url VARCHAR(500),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    processed_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- --------------------------------
-- 1.2 TWEET QUEUE TABLE
-- --------------------------------
-- Queue system for processing tweets that request token creation
CREATE TABLE IF NOT EXISTS tweet_queue (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tweet_id VARCHAR(50) UNIQUE NOT NULL,
    twitter_user VARCHAR(50) NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT DEFAULT 'This token was created in Moonshot via @memeXshot',
    website VARCHAR(500), -- Tweet URL
    twitter VARCHAR(50), -- Tweet author username
    image_url VARCHAR(500),
    profile_image_url VARCHAR(500),
    followers_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'rejected')),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- --------------------------------
-- 1.3 TWITTER RATE LIMITS TABLE
-- --------------------------------
-- Track daily rate limits for Twitter users (3 tokens per day)
CREATE TABLE IF NOT EXISTS twitter_rate_limits (
    twitter_user VARCHAR(50) PRIMARY KEY,
    daily_count INTEGER DEFAULT 0,
    last_reset DATE DEFAULT CURRENT_DATE,
    total_tokens INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- --------------------------------
-- 1.4 TWITTER REPLY QUEUE TABLE
-- --------------------------------
-- Queue for automatic Twitter replies after token creation
CREATE TABLE IF NOT EXISTS twitter_reply_queue (
    id SERIAL PRIMARY KEY,
    coin_id UUID REFERENCES coins(id),
    tweet_id VARCHAR(255) NOT NULL,
    twitter_user VARCHAR(255) NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    tx_signature VARCHAR(255) NOT NULL,
    token_mint VARCHAR(255),
    scheduled_at TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    twitter_account_used VARCHAR(255),
    replied_at TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ================================================
-- SECTION 2: INDEXES
-- ================================================

-- Coins table indexes
CREATE INDEX IF NOT EXISTS idx_coins_status ON coins(status);
CREATE INDEX IF NOT EXISTS idx_coins_created_at ON coins(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_coins_image_synced ON coins(image_synced);

-- Tweet queue indexes
CREATE INDEX IF NOT EXISTS idx_tweet_queue_status ON tweet_queue(status);
CREATE INDEX IF NOT EXISTS idx_tweet_queue_created ON tweet_queue(created_at);
CREATE INDEX IF NOT EXISTS idx_tweet_queue_tweet_id ON tweet_queue(tweet_id);

-- Twitter reply queue indexes
CREATE INDEX IF NOT EXISTS idx_reply_queue_status ON twitter_reply_queue(status);
CREATE INDEX IF NOT EXISTS idx_reply_queue_scheduled ON twitter_reply_queue(scheduled_at);

-- ================================================
-- SECTION 3: VIEWS
-- ================================================

-- View for pending image syncs
CREATE OR REPLACE VIEW pending_image_syncs AS
SELECT id, ticker, name, image_url, image_filename, created_at
FROM coins
WHERE image_url IS NOT NULL 
  AND image_synced = FALSE
  AND status = 'pending'
ORDER BY created_at ASC;

-- ================================================
-- SECTION 4: FUNCTIONS AND TRIGGERS
-- ================================================

-- --------------------------------
-- 4.1 UPDATE TIMESTAMP FUNCTION
-- --------------------------------
-- Automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- --------------------------------
-- 4.2 CHECK RATE LIMIT FUNCTION
-- --------------------------------
-- Check if a Twitter user has exceeded their daily limit (3 tokens)
CREATE OR REPLACE FUNCTION check_rate_limit(username VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    current_count INTEGER;
    last_reset_date DATE;
BEGIN
    -- Get or create user record
    INSERT INTO twitter_rate_limits (twitter_user)
    VALUES (username)
    ON CONFLICT (twitter_user) DO NOTHING;
    
    -- Get current values
    SELECT daily_count, last_reset INTO current_count, last_reset_date
    FROM twitter_rate_limits
    WHERE twitter_user = username;
    
    -- Reset if new day
    IF last_reset_date < CURRENT_DATE THEN
        UPDATE twitter_rate_limits
        SET daily_count = 0, last_reset = CURRENT_DATE
        WHERE twitter_user = username;
        current_count := 0;
    END IF;
    
    -- Check limit (3 per day)
    RETURN current_count < 3;
END;
$$ LANGUAGE plpgsql;

-- --------------------------------
-- 4.3 CHECK TWITTER RATE LIMIT FUNCTION
-- --------------------------------
-- Alternative function name for rate limit checking
-- (Creates same functionality with different name for compatibility)
CREATE OR REPLACE FUNCTION check_twitter_rate_limit(username VARCHAR)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN check_rate_limit(username);
END;
$$ LANGUAGE plpgsql;

-- --------------------------------
-- 4.4 TRIGGERS
-- --------------------------------

-- Update timestamp trigger for coins table
CREATE TRIGGER update_coins_updated_at 
    BEFORE UPDATE ON coins
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Update timestamp trigger for twitter_reply_queue table
CREATE TRIGGER update_twitter_reply_queue_updated_at 
    BEFORE UPDATE ON twitter_reply_queue
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ================================================
-- SECTION 5: ROW LEVEL SECURITY (RLS)
-- ================================================

-- Enable RLS for coins table
ALTER TABLE coins ENABLE ROW LEVEL SECURITY;

-- Create policy for public access to coins
-- NOTE: Adjust this policy based on your security requirements
CREATE POLICY "Enable all operations for all users" ON coins
    FOR ALL USING (true);

-- ================================================
-- SECTION 6: REALTIME SUBSCRIPTIONS
-- ================================================

-- Enable Realtime for coins table
ALTER PUBLICATION supabase_realtime ADD TABLE coins;

-- ================================================
-- SECTION 7: HELPER FUNCTIONS (OPTIONAL)
-- ================================================

-- Function to increment user's daily token count
CREATE OR REPLACE FUNCTION increment_user_token_count(username VARCHAR)
RETURNS VOID AS $$
BEGIN
    UPDATE twitter_rate_limits
    SET 
        daily_count = daily_count + 1,
        total_tokens = total_tokens + 1
    WHERE twitter_user = username;
END;
$$ LANGUAGE plpgsql;

-- Function to get user's remaining daily tokens
CREATE OR REPLACE FUNCTION get_remaining_tokens(username VARCHAR)
RETURNS INTEGER AS $$
DECLARE
    current_count INTEGER;
    last_reset_date DATE;
BEGIN
    -- Ensure user exists in rate limits table
    INSERT INTO twitter_rate_limits (twitter_user)
    VALUES (username)
    ON CONFLICT (twitter_user) DO NOTHING;
    
    -- Get current values
    SELECT daily_count, last_reset INTO current_count, last_reset_date
    FROM twitter_rate_limits
    WHERE twitter_user = username;
    
    -- Reset if new day
    IF last_reset_date < CURRENT_DATE THEN
        current_count := 0;
    END IF;
    
    -- Return remaining tokens (3 - current_count)
    RETURN GREATEST(0, 3 - current_count);
END;
$$ LANGUAGE plpgsql;

-- ================================================
-- END OF SCHEMA
-- ================================================