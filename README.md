# MemeXshot - Automated Token Creation Pipeline

An open-source automated token creation pipeline for Solana blockchain, featuring Twitter integration, real-time queue management, and automated image processing.

## 🚀 Overview

MemeXshot automates the process of creating meme tokens by:
- Monitoring Twitter for token creation requests
- Processing and validating token metadata
- Managing creation queues with real-time updates
- Automatically downloading and syncing token images
- Integrating with blockchain networks for token deployment

## 📋 Features

### ✅ Twitter Bot Integration
- Monitors mentions and hashtags
- Parses token creation requests
- Validates user permissions and rate limits
- Extracts metadata and images from tweets

### ✅ Queue Management System
- Real-time Supabase integration
- Status tracking (pending → processing → completed)
- Automatic retry mechanisms
- Priority queue support

### ✅ Image Processing Pipeline
- Automatic image download from URLs
- Photos app integration for macOS
- Image validation and formatting
- Duplicate detection

### ✅ Blockchain Integration
- Solana wallet monitoring
- Token creation transaction handling
- Real-time blockchain event tracking
- Reply bot for transaction confirmations

## 🛠️ Technology Stack

- **Backend**: Python 3.9+
- **Database**: Supabase (PostgreSQL)
- **Queue**: Real-time polling system
- **Blockchain**: Solana Web3
- **APIs**: Twitter API v2
- **Logging**: Comprehensive event tracking

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/memexshot-opensource.git
cd memexshot-opensource
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Initialize the database:
```bash
python -m scripts.database.setup
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Twitter API
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret

# Bot Configuration
BOT_USERNAME=memeXshot
SEARCH_KEYWORD=olala
MAX_DAILY_PER_USER=5
MIN_FOLLOWERS=100

# Blockchain
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
HELIUS_API_KEY=your_helius_key
```

### Database Schema

The system uses a PostgreSQL database with the following main tables:
- `coins` - Token creation requests and metadata
- `users` - Twitter user information and limits
- `transactions` - Blockchain transaction records

## 🚀 Usage

### Starting All Services

```bash
python scripts/start_all_services.py
```

This starts:
- Twitter Bot (monitors mentions)
- Queue Worker (processes pending tokens)
- Photo Sync Service (downloads images)
- Supabase Listener (monitors database changes)

### Individual Services

```bash
# Twitter Bot only
python scripts/services/twitter_bot.py

# Queue Worker only
python scripts/services/queue_worker.py

# Photo Sync only
python scripts/services/auto_photo_sync.py

# Database Listener only
python scripts/automation/supabase_listener_polling.py
```

## 📊 Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Twitter Bot   │────▶│    Supabase DB   │────▶│ Queue Processor │
│   (Listener)    │     │    (Real-time)   │     │   (Worker)      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                         │
         ▼                       ▼                         ▼
   ┌──────────┐           ┌──────────┐             ┌──────────┐
   │  Image   │           │  Status  │             │  Token   │
   │  Sync    │           │ Updates  │             │ Creation │
   └──────────┘           └──────────┘             └──────────┘
```

## 🔒 Security

- API keys are stored in environment variables
- Rate limiting prevents abuse
- User verification through follower count
- Secure database connections with row-level security

## 📝 API Documentation

### Creating a Token via API

```bash
curl -X POST 'YOUR_SUPABASE_URL/rest/v1/coins' \
  -H "apikey: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "MOON",
    "name": "Moon Token",
    "description": "To the moon!",
    "twitter_user": "@user",
    "image_url": "https://example.com/image.png"
  }'
```

### Monitoring Queue Status

```bash
curl 'YOUR_SUPABASE_URL/rest/v1/coins?status=eq.pending' \
  -H "apikey: YOUR_KEY"
```

## 🧪 Testing

Run the test suite:

```bash
# All tests
python -m pytest tests/

# Specific service tests
python tests/test_twitter_bot.py
python tests/test_queue_worker.py
python tests/test_supabase_listener.py
```

## 📊 Monitoring

The system includes comprehensive logging:
- `logs/master.log` - Important events only
- `logs/detailed.log` - All debug information
- `logs/events.json` - Structured event data
- Service-specific logs in `logs/[service_name].log`

View real-time logs:
```bash
python scripts/view_logs.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Important Note

This open-source version includes the complete pipeline for token metadata collection and queue management. The actual token creation automation module is proprietary and not included. 

To use this system for actual token creation, you'll need to implement your own token creation logic in the `scripts/automation/moonshot_automation.py` module.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Supabase for real-time database functionality
- Twitter API v2 for social media integration
- Solana blockchain for token creation
- The open-source community for various libraries and tools

## 📧 Contact

For questions or support, please open an issue on GitHub or contact the maintainers.

---

**Note**: This is the open-source version of MemeXshot. Some proprietary components related to automated GUI interaction have been excluded.