# Phase 6: Real-time Dashboard Website

## 🎯 Amaç
memeXshot otomasyonunun tüm verilerini gösteren, gerçek zamanlı, modern bir dashboard web sitesi oluşturmak.

## 🏗️ Teknoloji Stack

### Frontend
- **Framework**: React 18 + Vite (hızlı development)
- **Styling**: Tailwind CSS (modern, responsive)
- **Animasyon**: Framer Motion (smooth, profesyonel)
- **Charts**: Recharts (veri görselleştirme)
- **Real-time**: Supabase Realtime (canlı güncellemeler)
- **Icons**: Heroicons + Lucide React

### Backend/Data
- **Database**: Supabase (mevcut)
- **Blockchain**: Solana Web3.js (Moonshot verileri)
- **API**: Supabase REST API
- **Real-time**: Supabase Channels

## 📊 Dashboard Bölümleri

### 1. **Header**
- Logo + memeXshot branding
- Live status indicator (🟢 Active / 🔴 Inactive)
- Last update timestamp
- Admin announcements banner

### 2. **Stats Overview** (Hero Section)
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Total Coins │ 24h Coins   │ Active Users│ Success Rate│
│    156      │     24      │     89      │    94.2%    │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### 3. **Real-time Activity Feed**
- Son 50 işlem (auto-scroll)
- Format: `[12:34] @user launched $TICKER ✅`
- Status indicators: ⏳ Processing, ✅ Success, ❌ Failed
- Smooth fade-in animasyonları

### 4. **Token Gallery**
- Grid layout (responsive)
- Her token için:
  - Ticker & Name
  - Creator (@twitter)
  - Moonshot link
  - Price (from blockchain)
  - 24h change
  - Thumbnail image

### 5. **Charts Section**
- **Hourly Activity**: Son 24 saat (line chart)
- **Top Creators**: En çok token oluşturanlar (bar chart)
- **Success/Fail Ratio**: Pie chart
- **Popular Tickers**: Word cloud

### 6. **System Status**
```
┌─────────────────────────────────────┐
│ Service Status                      │
├─────────────────────────────────────┤
│ 🟢 Twitter Bot     | Active        │
│ 🟢 Queue Worker    | Active        │
│ 🟢 Photo Sync      | Active        │
│ 🟢 Automation      | Active        │
│ ⚡ Queue Length    | 3 items       │
│ 🕐 Avg Process Time| 2m 34s        │
└─────────────────────────────────────┘
```

### 7. **Logs Viewer**
- Filterable by service
- Search functionality
- Severity levels (info, warning, error)
- Collapsible details
- Auto-refresh toggle

### 8. **Footer**
- Links: Twitter, GitHub, Docs
- API status
- Version info
- Copyright

## 🎨 Design Principles

### Color Scheme
```css
--primary: #8B5CF6;     /* Purple - memeXshot brand */
--success: #10B981;     /* Green - successful */
--warning: #F59E0B;     /* Amber - processing */
--error: #EF4444;       /* Red - failed */
--background: #0F172A;  /* Dark blue */
--surface: #1E293B;     /* Lighter blue */
--text: #F1F5F9;        /* Off-white */
```

### Animations
- Subtle fade-ins for new data
- Smooth number transitions
- Gentle hover effects
- Loading skeletons
- NO excessive movement

### Responsive Design
- Mobile: Single column
- Tablet: 2 columns
- Desktop: Full grid
- Adaptive font sizes
- Touch-friendly interactions

## 🔧 Technical Implementation

### File Structure
```
website/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── StatsOverview.jsx
│   │   ├── ActivityFeed.jsx
│   │   ├── TokenGallery.jsx
│   │   ├── Charts.jsx
│   │   ├── SystemStatus.jsx
│   │   ├── LogsViewer.jsx
│   │   └── Footer.jsx
│   ├── hooks/
│   │   ├── useSupabaseRealtime.js
│   │   ├── useBlockchainData.js
│   │   └── useStats.js
│   ├── utils/
│   │   ├── supabase.js
│   │   ├── blockchain.js
│   │   └── formatters.js
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── vite.config.js
└── tailwind.config.js
```

### Key Features

#### 1. Real-time Updates
```javascript
// Supabase subscription for new coins
const channel = supabase
  .channel('coins-channel')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'coins'
  }, handleNewCoin)
  .subscribe()
```

#### 2. Blockchain Integration
```javascript
// Fetch token price from Moonshot
const getTokenPrice = async (mintAddress) => {
  // Jupiter/Raydium price API
}
```

#### 3. Service Health Check
```javascript
// Ping each service endpoint
const checkServiceHealth = async () => {
  // Return status for each service
}
```

#### 4. Data Aggregation
```javascript
// Calculate stats from Supabase
const getStats = async () => {
  // Total coins, 24h coins, success rate, etc.
}
```

## 🚀 Deployment

### Options
1. **Vercel** (recommended)
   - Easy deployment
   - Automatic SSL
   - Global CDN
   - Free tier sufficient

2. **Netlify**
   - Similar to Vercel
   - Good for static sites

3. **Self-hosted**
   - Nginx + PM2
   - More control

### Environment Variables
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_anon_key
VITE_SOLANA_RPC=your_rpc_endpoint
```

## 📱 Mobile Considerations
- Touch gestures for logs
- Simplified charts on mobile
- Collapsible sections
- Bottom navigation
- Pull-to-refresh

## 🔒 Security
- Read-only Supabase access
- No sensitive data exposed
- Rate limiting on API calls
- CORS properly configured

## 📈 Performance
- Lazy loading for images
- Virtual scrolling for logs
- Debounced search
- Memoized calculations
- Service worker for offline

## 🎯 Success Metrics
- Page load < 2 seconds
- Real-time delay < 500ms
- Mobile responsive
- 99% uptime
- User engagement time > 2 min

## 🛠️ Development Phases - YENI TASARIM

### Phase 1: Temizlik ve Hazırlık ✅
- [x] Mevcut tüm componentleri kaldır
- [x] Yeni tasarım için hazırlık yap

### Phase 2: Header Component
- [ ] Logo (sol üst)
- [ ] Create Free Coin butonu (orta)
  - [ ] Ticker modal/popup
  - [ ] Twitter yönlendirme
  - [ ] Görsel uyarısı
  - [ ] Tweet template: "Perfecto $TICKER @memeXshot"
- [ ] Status List (sağ üst)
  - [ ] Server Status
  - [ ] X Bot Status  
  - [ ] Moonshot Status
  - [ ] Web Status
  - [ ] Online/Offline indicators

### Phase 3: Live Logs Component (Sol - Büyük)
- [ ] İki bölümlü layout
- [ ] Sol Bölüm: İşlenen Token
  - [ ] Real-time token oluşturma durumu
  - [ ] Progress indicator
- [ ] Sağ Bölüm: Kuyruk
  - [ ] Supabase tweet_queue tablosu
  - [ ] Estimated time hesaplama (1.45sn/token)
  - [ ] Sonsuz scroll
  - [ ] Sıralama: En yakın en üstte
- [ ] Info Box (sağ üst)
  - [ ] Başarılı token sayısı
  - [ ] Kuyruktaki token sayısı
  - [ ] Başarısız token sayısı

### Phase 4: Live Feed Component (Sağ - Küçük)
- [ ] Real-time yeni tweetler
- [ ] Animasyonlu ekleme (üstten)
- [ ] Zaman göstergesi (5sn önce, 1dk önce)
- [ ] Max 10 tweet göster
- [ ] Otomatik silme (10'dan fazla olunca)
- [ ] Sıralama: En yeni en üstte

### Phase 5: Live Coins Component (Alt - Tam Genişlik)
- [ ] Başarılı coin kartları
- [ ] 20 coin/sayfa
- [ ] Pagination
- [ ] Kart tasarımı
  - [ ] Token adı/ticker
  - [ ] Oluşturan kullanıcı
  - [ ] Oluşturulma zamanı
  - [ ] Token görseli

### Phase 6: Supabase Real-time Entegrasyonu
- [ ] tweet_queue subscription
- [ ] coins subscription
- [ ] Real-time updates
- [ ] Connection management

### Phase 7: Animasyonlar ve Polish
- [ ] Smooth transitions
- [ ] Loading states
- [ ] Error states
- [ ] Responsive design

---

**Başlangıç**: Önce mevcut componentleri temizle ve yeni layout'u oluştur!