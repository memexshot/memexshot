# memeXshot Documentation

## 📚 Documentation Structure

### Development Phases
1. **[Phase 1: Automation Plan](phase1_automation_plan.md)** - Initial automation setup
2. **[Phase 2: Supabase Integration](phase2_supabase_integration.md)** - Cloud database setup
3. **[Phase 3: Dynamic Images](phase3_plan.md)** - Photo sync service
4. **[Phase 4: Twitter Bot](phase4_plan.md)** - Twitter integration
5. **[Phase 5: Testing](phase5_testing.md)** - Full system testing
6. **[Phase 6: Dashboard](phase6_dashboard.md)** - Real-time web dashboard

### Reference Documents
- **[Twitter API Limits](twitter_api_limits.md)** - Rate limits and quotas
- **[Twitter Bot Documentation](phase4_twitter_bot.md)** - Detailed bot implementation

### System Architecture
- **[Complete Flow](../README.md)** - Full system overview
- **[Service Components](#)** - Individual service documentation

## 🔄 Current System Flow

```
Twitter → Bot → Queue → Worker → Coins → Photo Sync → Automation → Moonshot
```

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Start All Services**
   ```bash
   python3 start_all_services.py
   ```

3. **Monitor System**
   ```bash
   python3 debug_check.py
   ```

## 📊 Service Status

| Service | Purpose | Status |
|---------|---------|--------|
| Twitter Bot | Monitors mentions | ✅ Active |
| Queue Worker | Processes queue | ✅ Active |
| Photo Sync | Downloads images | ✅ Active |
| Supabase Listener | Triggers automation | ✅ Active |
| Moonshot Automation | Creates tokens | ✅ Active |

## 🔧 Configuration

All configuration is managed through environment variables and test mode settings.
See [TEST_MODE_CHANGES.md](../tests/TEST_MODE_CHANGES.md) for current test configurations.

## 📈 Next Steps

- [ ] Complete Phase 6 Dashboard
- [ ] Production deployment
- [ ] Monitoring setup
- [ ] User documentation