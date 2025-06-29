-- Moonshot Automation Database Schema for Supabase

-- Create coins table
CREATE TABLE IF NOT EXISTS coins (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    twitter VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    processed_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Create index for faster queries
CREATE INDEX idx_coins_status ON coins(status);
CREATE INDEX idx_coins_created_at ON coins(created_at DESC);

-- Enable Row Level Security
ALTER TABLE coins ENABLE ROW LEVEL SECURITY;

-- Create policy for public access (adjust as needed)
CREATE POLICY "Enable all operations for all users" ON coins
    FOR ALL USING (true);

-- Create trigger to update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_coins_updated_at BEFORE UPDATE ON coins
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable Realtime for coins table
ALTER PUBLICATION supabase_realtime ADD TABLE coins;