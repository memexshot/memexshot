-- Phase 3: Dynamic Image Management Schema Updates

-- Add image-related columns to coins table
ALTER TABLE coins ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);
ALTER TABLE coins ADD COLUMN IF NOT EXISTS image_filename VARCHAR(255);
ALTER TABLE coins ADD COLUMN IF NOT EXISTS image_synced BOOLEAN DEFAULT FALSE;
ALTER TABLE coins ADD COLUMN IF NOT EXISTS image_sync_timestamp TIMESTAMP WITH TIME ZONE;
ALTER TABLE coins ADD COLUMN IF NOT EXISTS twitter_user VARCHAR(50);
ALTER TABLE coins ADD COLUMN IF NOT EXISTS tweet_id VARCHAR(50);

-- Create index for faster image sync queries
CREATE INDEX IF NOT EXISTS idx_coins_image_synced ON coins(image_synced);

-- View to see pending image syncs
CREATE OR REPLACE VIEW pending_image_syncs AS
SELECT id, ticker, name, image_url, image_filename, created_at
FROM coins
WHERE image_url IS NOT NULL 
  AND image_synced = FALSE
  AND status = 'pending'
ORDER BY created_at ASC;