# Phase 5: Full System Testing

## 🎯 Amaç
Tüm otomasyonun baştan sona sorunsuz çalıştığını doğrulamak. Birden fazla hesaptan tweet atarak sistemin dayanıklılığını test etmek.

## 📊 Sistem Mimarisi

### Akış Diyagramı
```
Twitter → Twitter Bot → tweet_queue → Queue Worker → coins → Photo Sync → Supabase Listener → Moonshot Automation
```

### Detaylı Akış
1. **Twitter'da Tweet Atılır**: `Perfecto $TICKER @memeXshot` + görsel
2. **Twitter Bot (30 saniye)**: Tweet'i yakalar → `tweet_queue` tablosuna ekler
3. **Queue Worker (10 saniye)**: Queue'dan alır → `coins` tablosuna taşır
4. **Photo Sync (sürekli)**: Görseli indirir → Photos Library'ye ekler → `image_synced=true`
5. **Supabase Listener (5 saniye)**: `status=pending AND image_synced=true` olanları bulur
6. **Moonshot Automation**: Token oluşturur → `status=completed`

## 🚀 Servisleri Başlatma

### Tek Komutla Başlatma
```bash
python3 start_all_services.py
```

### Servisler (4 adet)
1. **Twitter Bot** (`services/twitter_bot.py`)
   - Search pattern: "Perfecto" "@memeXshot"
   - Poll interval: 30 saniye
   - Min followers: 0 (test mode)
   - Daily limit: 99 (test mode)

2. **Queue Worker** (`services/queue_worker.py`)
   - Check interval: 10 saniye
   - Follower check: Disabled (test mode)
   - Process: tweet_queue → coins

3. **Photo Sync** (`services/auto_photo_sync.py`)
   - Check interval: Continuous
   - Downloads to: `downloads/` folder
   - Import to: Photos Library

4. **Supabase Listener** (`automation/supabase_listener_polling.py`)
   - Poll interval: 5 saniye
   - Auto-start: Yes (test mode)
   - Triggers: moonshot_automation.py

## 📋 Test Senaryoları

### 1. Tekil Tweet Testi
- Tek tweet at
- Format: `Perfecto $TEST1 @memeXshot` + görsel
- Beklenen: ~2-3 dakikada token oluşturulmalı

### 2. Ardışık Tweet Testi
- 3 tweet ard arda at (farklı ticker'lar)
- Beklenen: Sırayla işlenmeli (paralel değil)

### 3. Aynı Kullanıcı Çoklu Tweet
- Aynı hesaptan 5+ tweet
- Beklenen: Hepsi işlenmeli (limit 99)

### 4. Farklı Hesaplar Testi
- 3-5 farklı hesaptan tweet
- Beklenen: Hepsi sırayla işlenmeli

### 5. Edge Case'ler
- Görselsiz tweet → Reddedilmeli
- 11+ karakter ticker → Reddedilmeli
- Yanlış format → Yakalanmamalı

## 🔍 Monitoring

### Log İzleme
```bash
# Ana servisler
[Twitter Bot] 🔍 Found X new tweets
[Queue Worker] 📨 Processing queued tweet: TICKER
[Photo Sync] 🖼️ Syncing image for $TICKER
[Supabase Listener] 🆕 Found 1 new coin(s) to process
```

### Database Kontrol
```bash
python3 debug_check.py
```

### Manuel Kontroller
- Supabase Dashboard'dan tabloları izle
- Photos Library'de görseller
- Moonshot app'te oluşan token'lar

## ⚠️ Test Mode Ayarları

### Aktif Değişiklikler
1. **Search Pattern**: "Launch" → "Perfecto"
2. **Min Followers**: 500 → 0
3. **Daily Limit**: 3 → 99
4. **Auto Start**: Manuel → Otomatik
5. **Token Data**: Gerçek → Test değerleri

### Geri Alma
Test bitince `tests/TEST_MODE_CHANGES.md` dosyasındaki talimatlara göre geri al.

## 🎯 Başarı Kriterleri

### ✅ Sistem Başarılı Sayılır:
- [ ] 10+ tweet'in %90'ı başarıyla işlendi
- [ ] Ortalama işlem süresi < 3 dakika
- [ ] Sıralama doğru (görsel indikten sonra token)
- [ ] Hata durumlarında sistem durmadı
- [ ] Database tutarlı kaldı

### ❌ Dikkat Edilecek Sorunlar:
- Twitter API rate limit
- Photos Library sync gecikmesi
- Moonshot app focus kaybı
- Database connection timeout

## 📝 Test Prosedürü

1. **Hazırlık**
   - Moonshot app açık ve ana ekranda
   - Database temiz (`python3 debug_check.py`)
   - Test hesapları hazır

2. **Başlatma**
   ```bash
   python3 start_all_services.py
   ```

3. **Test Tweet Formatı**
   ```
   Perfecto $TICKER @memeXshot
   ```
   + Görsel (zorunlu)
   + Ticker 3-10 karakter

4. **İzleme**
   - Terminal logları
   - Database durumu
   - Moonshot app'te token oluşumu

5. **Sonuçları Kaydet**
   - Başarılı/başarısız oranı
   - Ortalama süre
   - Karşılaşılan hatalar

## 🔧 Troubleshooting

### Tweet Yakalanmıyor
- Twitter Bot loglarını kontrol et
- API credentials doğru mu?
- Rate limit'e takıldın mı?

### Görsel İndirilmiyor
- Photo Sync loglarını kontrol et
- İnternet bağlantısı?
- Photos Library izinleri?

### Token Oluşturulmuyor
- Moonshot app açık mı?
- Koordinatlar doğru mu?
- macOS şifresi doğru mu?

## 🎉 Test Tamamlandı!

Test başarılıysa:
1. Production ayarlarına geri dön
2. Gerçek kullanıma geç
3. Rate limit'leri ayarla

---

**Not**: Bu test phase'i en az 1 saat sürmeli ve farklı senaryolar denenmelidir.