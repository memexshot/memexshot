# 🎯 Moonshot Automation System - Planlama Dökümanı

## 🎨 Proje Vizyonu

Flutter tabanlı Moonshot uygulamasında otomatik coin oluşturma sistemi geliştireceğiz. Sistem, veritabanından coin bilgilerini okuyacak ve form doldurma işlemini otomatikleştirecek.

## 🔍 Problem Analizi

### Karşılaşılan Zorluklar
- Flutter uygulamaları UI elementlerini expose etmiyor
- macOS güvenlik modeli direkt uygulama kontrolüne izin vermiyor
- Klavye event'leri ile karakter uyumsuzluğu problemi

### Çözüm Stratejisi
- Koordinat tabanlı otomasyon
- Clipboard (pano) üzerinden metin girişi
- macOS native API'leri kullanımı

## 🛠️ Teknoloji Seçimleri

### Core Framework
**macOS Quartz/Core Graphics**
- Neden: macOS'ta low-level mouse/keyboard kontrolü için tek yol
- Ne sağlıyor: CGEvent API'leri ile sistem seviyesinde event simülasyonu

### Programming Language
**Python 3.9+**
- Neden: PyObjC bridge ile macOS API'lerine kolay erişim

### Gerekli Kütüphaneler

```txt
# macOS Integration
pyobjc-core         # Python-Objective-C bridge
pyobjc-framework-Cocoa    # Cocoa framework erişimi
pyobjc-framework-Quartz   # Quartz/CoreGraphics API

# Clipboard Operations
pyperclip           # Cross-platform clipboard kütüphanesi

# Database
sqlalchemy          # ORM için
alembic            # Migration yönetimi (opsiyonel)

# Utilities
loguru             # Gelişmiş loglama
python-dotenv      # Çevre değişkenleri (opsiyonel)

# Development
black              # Kod formatlama
pytest            # Test framework
```

## 📋 Uygulama Adımları

### Adım 1: Koordinat Yakalama Sistemi

**Amaç**: Form elemanlarının ekran koordinatlarını belirlemek

**Yaklaşım**:
1. İnteraktif bir araç geliştirilecek
2. Kullanıcı her form elemanına tıklayacak
3. Koordinatlar JSON formatında saklanacak

**Yakalanacak Elemanlar**:
- Ticker input alanı
- Name input alanı
- Description textarea
- Add Image butonu
- Image library modal elemanları
- Website URL alanı
- Twitter/sosyal medya alanları
- Create/Submit butonu

### Adım 2: Veritabanı Tasarımı

**Amaç**: Coin bilgilerini strukturlı şekilde saklamak

**Tablo Yapısı Önerisi**:
```sql
coins:
- id (primary key)
- name (coin adı)
- ticker (sembol)
- description (açıklama)
- website_url
- twitter_handle
- image_reference (opsiyonel)
- status (pending/processing/completed/failed)
- created_at
- processed_at
- error_message
```

**ORM Kullanımı**: SQLAlchemy ile model tabanlı erişim

### Adım 3: Otomasyon Motoru

**Core Bileşenler**:

#### 3.1 Mouse Kontrolü
```python
# Quartz CGEvent API kullanarak mouse simülasyonu
- CGEventCreateMouseEvent() - Mouse event oluşturma
- CGEventPost() - Event'i sisteme gönderme
- kCGEventLeftMouseDown/Up - Click simülasyonu
```

#### 3.2 Metin Girişi Stratejisi
```python
# Clipboard yaklaşımı:
1. pyperclip.copy(text) - Metni panoya kopyala
2. Cmd+V simülasyonu - CGEvent ile yapıştır
```

**Neden Clipboard?**
- Karakter encoding sorunlarını bypass eder
- Daha güvenilir ve hızlı

#### 3.3 Form Doldurma Akışı
```
1. Veritabanından pending coin al
2. Moonshot formunu aç (manuel)
3. Her alan için:
   - Koordinata tıkla
   - Mevcut içeriği temizle (Cmd+A, Delete)
   - Yeni değeri clipboard'a kopyala
   - Cmd+V ile yapıştır
   - Kısa bekleme (UI güncellemesi için)
4. Görsel seçimi (koordinat tabanlı)
5. Form gönderimi
6. Veritabanı durumunu güncelle
```

### Adım 4: Hata Yönetimi ve Logging

**Logging Stratejisi**:
- Her işlem adımını logla
- Koordinat yakalama logları
- Form doldurma adımları
- Hata durumları detaylı kayıt

**Hata Senaryoları**:
- Form elemanı bulunamadı
- Moonshot uygulaması açık değil
- Rate limiting
- Network hataları

## 🏗️ Önerilen Proje Yapısı

```
project/
├── capture/
│   └── coordinate_capture.py    # Koordinat yakalama aracı
├── automation/
│   ├── mouse_controller.py      # Mouse işlemleri
│   ├── keyboard_controller.py   # Klavye işlemleri
│   └── form_filler.py          # Form doldurma mantığı
├── database/
│   ├── models.py               # SQLAlchemy modelleri
│   └── manager.py              # DB işlemleri
├── config/
│   └── settings.py             # Ayarlar ve sabitler
├── utils/
│   ├── logger.py               # Loglama yapılandırması
│   └── helpers.py              # Yardımcı fonksiyonlar
└── main.py                     # Ana uygulama entry point
```

## ⚡ Performans Optimizasyonları

### Timing Stratejisi
- UI elemanları arası minimum bekleme: 1 saniye
- Modal/popup açılması: 3 saniye
- Form submit sonrası: 5 saniye
- Rate limiting: Coinler arası 30 saniye



## 🚀 Implementasyon Sırası

1. **Faz 1**: Koordinat yakalama aracını geliştir
2. **Faz 2**: Mouse/keyboard controller'ları oluştur
3. **Faz 3**: Veritabanı yapısını kur
4. **Faz 4**: Form doldurma mantığını implement et
5. **Faz 5**: Test ve optimizasyon


## 📚 Kaynaklar

- [Quartz Event Services](https://developer.apple.com/documentation/coregraphics/quartz_event_services)
- [PyObjC Documentation](https://pyobjc.readthedocs.io/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)

