# 🚀 Moonshot Automation - Phase 3 Implementation Plan

## 📋 Phase 3 Overview: Dynamic Image Management

### 🎯 Goal
Enable unique images for each token by implementing automatic image synchronization between Twitter/Supabase and macOS Photos Library.

### 🔄 Architecture Overview

```
Twitter API → Supabase → Photo Sync Service → Photos Library → Automation Script → Moonshot App
```

## 🏗️ System Components

### 1. **Photo Sync Service** (New)
- **Purpose**: Monitor Supabase for new images and sync to Photos Library
- **Location**: `/services/auto_photo_sync.py`
- **Functionality**:
  - Poll Supabase every 30 seconds
  - Download new images
  - Import to Photos using AppleScript
  - Update sync status in Supabase

### 2. **Photos Library Watcher** (Modified Automation)
- **Purpose**: Monitor Photos Library for new images and trigger token creation
- **Location**: `/automation/photos_library_watcher.py`
- **Functionality**:
  - Watch Photos Library for changes
  - Detect new images
  - Match with pending coins in Supabase
  - Trigger token creation automation

## 📊 Database Schema Updates

```sql
-- Add image sync fields to coins table
ALTER TABLE coins ADD COLUMN image_url VARCHAR(500);
ALTER TABLE coins ADD COLUMN image_filename VARCHAR(255);
ALTER TABLE coins ADD COLUMN image_synced BOOLEAN DEFAULT FALSE;
ALTER TABLE coins ADD COLUMN image_sync_timestamp TIMESTAMP WITH TIME ZONE;
ALTER TABLE coins ADD COLUMN twitter_user VARCHAR(50);
ALTER TABLE coins ADD COLUMN tweet_id VARCHAR(50);
```

## 🔧 Implementation Steps

### Step 1: Create Photo Sync Service
```python
# /services/auto_photo_sync.py
# - Connect to Supabase
# - Poll for unsynced images
# - Download and import to Photos
# - Update sync status
```

### Step 2: Modify Main Automation
```python
# /automation/photos_library_watcher.py
# - Monitor Photos Library
# - Detect new images
# - Query Supabase for matching coin
# - Execute token creation
```

### Step 3: Update Filename Convention
```
Format: {twitter_user}_{ticker}_{timestamp}.jpg
Example: elonmusk_MOON_1735501234.jpg
```

## 🚦 Process Flow

1. **Twitter Bot Phase**:
   - Parse tweet: ticker, name, image
   - Upload image to Supabase Storage
   - Create coin record with image_url

2. **Sync Phase**:
   - Photo Sync Service detects new image
   - Downloads from Supabase
   - Imports to Photos Library
   - Updates image_synced = true

3. **Automation Phase**:
   - Library Watcher detects new photo
   - Matches filename to coin record
   - Triggers token creation
   - Uses latest image (automatically selected)

## ⚙️ macOS Photos Settings Required

### Critical Settings:
1. **iCloud Photos**: Must be enabled
2. **Optimize Mac Storage**: Should be OFF
3. **Download Originals**: Must be ON
4. **Photos App**: Should run at startup

### Terminal Commands:
```bash
# Check Photos Library location
ls ~/Pictures/Photos\ Library.photoslibrary/

# Ensure Photos agent is running
launchctl list | grep photos

# Force sync (if needed)
killall Photos
open -a Photos
```

## 🚀 Deployment

### Running the System:
```bash
# Terminal 1: Photo Sync Service
cd /Users/baymak/Desktop/mshot6/moonshot_automation
python3 services/auto_photo_sync.py

# Terminal 2: Photos Library Watcher
python3 automation/photos_library_watcher.py
```

### Service Management:
```bash
# Create launchd services for auto-start
# Photo Sync: ~/Library/LaunchAgents/com.moonshot.photosync.plist
# Watcher: ~/Library/LaunchAgents/com.moonshot.watcher.plist
```

## 🔍 Monitoring & Debugging

### Log Files:
- Photo Sync: `/logs/photo_sync.log`
- Library Watcher: `/logs/library_watcher.log`

### Health Checks:
1. Supabase connection status
2. Photos Library accessibility
3. Sync queue length
4. Last successful sync timestamp

## ⚡ Performance Considerations

- Poll interval: 30 seconds (adjustable)
- Image download timeout: 30 seconds
- Photos import delay: 5 seconds
- Max retry attempts: 3

## 🛡️ Error Handling

### Common Issues:
1. **Photos Library Locked**: Wait and retry
2. **iCloud Sync Delay**: Implement timeout
3. **Duplicate Images**: Check by filename
4. **Network Issues**: Exponential backoff

## 📈 Success Metrics

- Image sync success rate: >99%
- Average sync time: <45 seconds
- Zero manual interventions
- Full automation end-to-end

## 🔄 Future Enhancements

1. Real-time sync (webhooks instead of polling)
2. Batch image processing
3. Image optimization before import
4. Automated cleanup of old images

---

**Phase 3 Start Date**: 2025-06-29  
**Estimated Completion**: 2-3 days  
**Status**: Planning Complete ✅