-- Phase 4: Twitter Queue System

-- Tweet queue table
CREATE TABLE IF NOT EXISTS tweet_queue (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tweet_id VARCHAR(50) UNIQUE NOT NULL,
    twitter_user VARCHAR(50) NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT DEFAULT 'This token was created in Moonshot via @memeXshot',
    website VARCHAR(500), -- Tweet URL
    twitter VARCHAR(50), -- Tweet atan kullanıcı
    image_url VARCHAR(500),
    followers_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'rejected')),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- Add column if table already exists
ALTER TABLE tweet_queue ADD COLUMN IF NOT EXISTS followers_count INTEGER DEFAULT 0;
ALTER TABLE tweet_queue DROP CONSTRAINT IF EXISTS tweet_queue_status_check;
ALTER TABLE tweet_queue ADD CONSTRAINT tweet_queue_status_check 
    CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'rejected'));

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tweet_queue_status ON tweet_queue(status);
CREATE INDEX IF NOT EXISTS idx_tweet_queue_created ON tweet_queue(created_at);
CREATE INDEX IF NOT EXISTS idx_tweet_queue_tweet_id ON tweet_queue(tweet_id);

-- User rate limiting
CREATE TABLE IF NOT EXISTS twitter_rate_limits (
    twitter_user VARCHAR(50) PRIMARY KEY,
    daily_count INTEGER DEFAULT 0,
    last_reset DATE DEFAULT CURRENT_DATE,
    total_tokens INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Function to check and update rate limits
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