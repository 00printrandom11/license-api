# 🧠 END-GAME License API - Professional Edition

## ✨ Özellikler

### 🔑 Çekirdek Sistem
- ✅ **License Authority** - Sunucu tek zaman otoritesi (server_timestamp)
- ✅ **Online-Only Validation** - Sürekli sunucu kontrolü gerektirir
- ✅ **Heartbeat System** - Lisans durumu gerçek zamanlı takip
- ✅ **WebSocket Push Control** - Anında lisans kapatma/güncelleme

### 🔒 Güvenlik
- ✅ **Audit Log System** - Tüm işlemler kaydedilir (kim, ne zaman, nereden)
- ✅ **Abuse & Anomaly Detection** - HWID/IP değişim takibi ve otomatik ban
- ✅ **Admin Security** - Rate limiting, IP kontrolü, session yönetimi
- ✅ **Automated Banning** - Abuse skoru 50+ olan lisanslar otomatik banlanır

### 📊 Panel Özellikleri
- ✅ Real-time metrics dashboard
- ✅ Gelişmiş lisans yönetimi (CRUD)
- ✅ Süre ekleme/çıkarma (saat/gün)
- ✅ HWID reset
- ✅ Durum yönetimi (aktif/pasif)
- ✅ Ban/Unban işlemleri
- ✅ Abuse skoru sıfırlama
- ✅ Canlı arama/filtreleme
- ✅ Audit log görüntüleme

## 🚀 Kurulum

### 1. Gereksinimler
```bash
pip install -r requirements.txt
```

### 2. Ortam Değişkenleri (.env)
```bash
# Admin Bilgileri
ADMIN_USERNAME=admin
ADMIN_PASSWORD=güçlü_şifreniz

# Secret Key
SECRET_KEY=çok_güçlü_rastgele_anahtar

# IP Whitelist (Render.com için isteğe bağlı)
ALLOWED_PANEL_IPS=

# Veritabanı
DB_DIR=/var/data
DATABASE_URL=sqlite:///licenses.db
```

### 3. Lokal Test
```bash
uvicorn main:app --reload
```

### 4. Render.com Deploy
1. GitHub repo oluştur ve kodu push et
2. Render.com'da yeni Web Service oluştur
3. Environment variables ekle
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 📡 API Endpoints

### Public API
```
GET  /api/time              - Sunucu zamanı
POST /api/activate          - İlk aktivasyon
POST /api/check             - Lisans kontrolü
WS   /ws/{license_key}      - WebSocket bağlantısı
```

### Admin Panel
```
GET  /panel/login           - Giriş sayfası
POST /panel/login           - Giriş işlemi
GET  /panel                 - Ana panel
GET  /panel/logout          - Çıkış

POST /panel/licenses/create              - Yeni lisans
POST /panel/licenses/add_time            - Süre ekle
POST /panel/licenses/{id}/toggle         - Durum değiştir
POST /panel/licenses/{id}/reset_hwid     - HWID sıfırla
POST /panel/licenses/{id}/ban            - Ban/Unban
POST /panel/licenses/{id}/reset_abuse    - Abuse sıfırla
POST /panel/licenses/{id}/delete         - Sil
```

## 🎯 Kullanım

### Desktop Uygulaması için örnek kod:
```python
import requests
import time

API_URL = "https://your-app.onrender.com"
LICENSE_KEY = "your-license-key"
HWID = "your-hardware-id"

# 1. İlk aktivasyon
def activate():
    response = requests.post(f"{API_URL}/api/activate", json={
        "license_key": LICENSE_KEY,
        "hwid": HWID,
        "ip_address": None  # Otomatik alınır
    })
    return response.json()

# 2. Periyodik kontrol (her 30 saniyede)
def check_license():
    while True:
        response = requests.post(f"{API_URL}/api/check", json={
            "license_key": LICENSE_KEY,
            "hwid": HWID
        })
        
        data = response.json()
        if data["status"] != "active":
            print("❌ Lisans geçersiz!")
            exit()
        
        print(f"✅ Lisans aktif - Kalan: {data['remaining_seconds']}s")
        time.sleep(30)
```

## 🛡️ Güvenlik Özellikleri

### HWID Conflict Detection (Otomatik Ban Sistemi)

**IP önemli değil - Sadece HWID önemli!** ✅

#### Sistem Mantığı:
Aynı lisans key farklı bir bilgisayarda kullanılmaya çalışılırsa:

1. 🚨 **Tespit** - System farklı HWID'yi algılar
2. 🚫 **Her İki PC Ban** - Eski ve yeni HWID banlanır
3. ❌ **Key Pasif** - Lisans devre dışı bırakılır
4. 📝 **Kayıt** - Tüm detaylar loglanır
5. 📊 **Panel** - Banlı HWID'ler sekmesinde görünür

#### Örnekler:

**✅ Normal Kullanım**:
```
Müşteri:
- PC 1'de programı kullanıyor (HWID: ABC123...)
- IP'si 100 kez değişti (modem, mobil vb.) ✅
- Hiçbir sorun yok ✅
```

**🚫 Crack Denemesi**:
```
Cracker:
- PC 1'de çalıştırdı (HWID: ABC123...)
- PC 2'de çalıştırmaya çalıştı (HWID: DEF456...)

Sistem Tepkisi:
→ HWID ABC123 BANLANDI 🚫
→ HWID DEF456 BANLANDI 🚫  
→ Lisans PASİF ❌
→ Her iki PC de artık çalışamaz!
```

#### Panel - Banlı HWID'ler Sekmesi:
Panelde göreceğiniz bilgiler:
- 🔢 Ban ID
- 🖥️ Banlı HWID
- 🔑 Hangi lisans key
- 📋 Ban nedeni
- 🔄 Çakışan HWID (diğer PC)
- 👤 Kim banladı (system/admin)
- 📅 Ban tarihi ve saati
- 🌐 IP adresi
- 📝 Detaylar

### Rate Limiting
- Login: 5 deneme / 5 dakika
- Tüm admin işlemleri loglanır
- IP bazlı erişim kontrolü

### Audit Log
Tüm işlemler kaydedilir:
- Kullanıcı adı
- IP adresi
- İşlem tipi
- Hedef (license_key)
- Detaylar
- Zaman damgası

## 📈 Render.com Production Ayarları

```yaml
# render.yaml
services:
  - type: web
    name: license-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: ADMIN_USERNAME
        value: admin
      - key: ADMIN_PASSWORD
        generateValue: true
      - key: SECRET_KEY
        generateValue: true
      - key: DB_DIR
        value: /var/data
```

## 🎨 Panel Özellikleri

### Metrics Dashboard
- 📊 Toplam lisans sayısı
- 🟢 Şu an aktif olanlar (son 60sn içinde)
- 🚫 Banlı lisanslar
- ⏰ Süresi dolmuş lisanslar

### Lisans Tablosu Kolonları
- ID
- KEY (kopyalama butonu ile)
- HWID (ilk 16 karakter)
- SON KONTROL (tarih/saat)
- DURUM (Çalışıyor/Aktif/Pasif/Banlı)
- BİTİŞ TARİHİ
- KALAN SÜRE
- IP ADRESİ
- ABUSE SKORU
- NOT
- İŞLEMLER (6+ buton)

### İşlem Butonları
- ⏱ Süre - Saat/gün ekleme
- ⏸/▶ Durdur/Başlat
- 🔄 HWID Reset
- 🚫/✅ Ban/Unban
- 🔧 Abuse Reset
- 🗑 Sil

## 🔧 Bakım

### Veritabanı Yedekleme
```bash
# SQLite için
cp /var/data/licenses.db /backup/licenses_$(date +%Y%m%d).db
```

### Log Temizleme
```python
# Eski logları temizle (90 gün+)
from datetime import datetime, timedelta
from database import get_db
from models import AuditLog

db = next(get_db())
cutoff = datetime.utcnow() - timedelta(days=90)
db.query(AuditLog).filter(AuditLog.timestamp < cutoff).delete()
db.commit()
```

## 📝 Notlar

- ✅ Render.com ücretsiz tier'da sorunsuz çalışır
- ✅ Auto-refresh her 10 saniyede bir
- ✅ Session timeout yok (güvenlik için eklenebilir)
- ✅ PostgreSQL desteği var (DATABASE_URL ile)
- ✅ Responsive tasarım (mobil uyumlu)

## 🆘 Sorun Giderme

### "Lisans geçersiz" hatası
- HWID değişmiş olabilir → HWID Reset kullan
- Lisans süresi dolmuş → Süre ekle
- Lisans banlı → Unban et
- Abuse skoru yüksek → Abuse Reset

### Panel'e giriş yapamıyorum
- Username/password doğru mu kontrol et
- Rate limit aşıldı mı? (5 dakika bekle)
- IP whitelist aktif mi? (ALLOWED_PANEL_IPS)

### Render.com'da çalışmıyor
- Environment variables eklenmiş mi?
- DB_DIR=/var/data olmalı
- Port $PORT kullanılmalı
- Build logs kontrol et

## 📜 Lisans

Bu proje özel bir projedir. Ticari kullanım için izin gereklidir.

---

**⚡ Made with END-GAME Security Framework**

