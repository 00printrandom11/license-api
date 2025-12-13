# 🚀 HIZLI BAŞLANGIÇ - Render.com Deploy

## 1️⃣ GitHub'a Yükle

```bash
cd C:\Users\aLmiLa\Desktop\license-api
git init
git add .
git commit -m "🧠 END-GAME License System v1.0"
git branch -M main
git remote add origin https://github.com/USERNAME/license-api.git
git push -u origin main
```

## 2️⃣ Render.com Kurulum

1. https://render.com → Sign In (GitHub ile)
2. **New +** → **Web Service**
3. Repository seç: `license-api`
4. Ayarlar:
   - **Name**: `license-api` (veya istediğin)
   - **Region**: `Frankfurt` (en yakın)
   - **Branch**: `main`
   - **Root Directory**: (boş bırak)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

## 3️⃣ Environment Variables Ekle

**Advanced** → **Environment Variables** → **Add Environment Variable**

```
ADMIN_USERNAME = admin
ADMIN_PASSWORD = SifreNiz123!
SECRET_KEY = rastgele_çok_uzun_güvenli_anahtar_12345
DB_DIR = /var/data
```

**⚠️ ÖNEMLİ**: 
- `ADMIN_PASSWORD` güçlü bir şifre olsun
- `SECRET_KEY` rastgele en az 32 karakter olsun

## 4️⃣ Deploy Et

- **Create Web Service** butonuna tıkla
- Deploy başlayacak (2-3 dakika sürer)
- Yeşil **Live** görünce hazır!

## 5️⃣ Test Et

URL'in: `https://license-api-xyz.onrender.com`

### Panel'e Giriş
1. Tarayıcıda: `https://your-app.onrender.com/panel/login`
2. Username: `admin`
3. Password: Environment variable'da ne yazdıysan

### İlk Lisans Oluştur
1. Panel'e gir
2. **➕ Yeni Lisans** sekmesi
3. Süre: `30` gün
4. Not: `Test Lisansı`
5. **🔑 Lisans Oluştur**

### Desktop Uygulamadan Test
```python
import requests

API_URL = "https://your-app.onrender.com"
LICENSE_KEY = "panelden_aldığın_key"
HWID = "test-hwid-12345"

# Aktivasyon
response = requests.post(f"{API_URL}/api/activate", json={
    "license_key": LICENSE_KEY,
    "hwid": HWID
})

print(response.json())
# {'status': 'active', 'remaining_seconds': 2592000, 'server_timestamp': 1702412345.678}
```

## 🎯 Sonraki Adımlar

### Desktop App Integration
Desktop uygulamanıza şu özellikleri ekleyin:

1. **İlk Açılış**: `/api/activate` çağır
2. **Her 30sn**: `/api/check` çağır
3. **Offline Tolerance**: Max 2-5 dakika
4. **HWID Hesaplama**: Makine ID + CPU ID + Disk Serial
5. **Şifreleme**: API isteklerini şifrele

### Panel Güvenliği
- IP Whitelist aktif et: `ALLOWED_PANEL_IPS=1.2.3.4,5.6.7.8`
- 2FA ekle (opsiyonel)
- Session timeout (opsiyonel)

### Monitoring
- Render Dashboard → Logs
- Metrics → CPU/Memory kullanımı
- Abuse skorları yüksek olanları kontrol et

## 🆘 Sorun Giderme

### Deploy Hata Veriyor
- Build logs'u kontrol et
- `requirements.txt` eksik mi?
- Python versiyonu 3.8+ olmalı

### Panel Açılmıyor
- URL doğru mu? `/panel/login`
- Deploy tamamlandı mı? (Yeşil **Live**)
- Environment variables eklenmiş mi?

### "403 Forbidden" Hatası
- `ALLOWED_PANEL_IPS` varsa kaldır veya kendi IP'ni ekle

### Database Hatası
- `DB_DIR=/var/data` olmalı
- Render otomatik oluşturur

## 📊 Önemli Bilgiler

### Render Free Tier Limitler
- ✅ 750 saat/ay (24/7 çalışabilir)
- ✅ 512MB RAM (bu API için yeterli)
- ✅ Otomatik SSL (HTTPS)
- ⚠️ 15dk inaktif sonra uyur (ilk istek 30sn sürer)
- ⚠️ Her ay DB sıfırlanmaz (kalıcı)

### Performans Optimizasyonu
- Paid plan → Always-on (uyumaz)
- PostgreSQL → Daha hızlı (opsiyonel)
- CDN → Statik dosyalar için (gerekmiyor)

### Backup
SQLite DB: `/var/data/licenses.db`
- Render Dashboard → Shell → `cat /var/data/licenses.db > backup.db`
- Veya PostgreSQL kullan (otomatik backup)

## ✅ Checklist

- [ ] GitHub'a push ettim
- [ ] Render'da Web Service oluşturdum
- [ ] Environment variables ekledim
- [ ] Deploy başarılı (yeşil Live)
- [ ] Panel'e giriş yaptım
- [ ] İlk lisansı oluşturdum
- [ ] Desktop app'ten test ettim
- [ ] README.md okudum

## 🎉 Başarılı!

Artık profesyonel bir lisans sisteminiz var:
- ✅ Abuse detection
- ✅ Audit logging  
- ✅ Real-time monitoring
- ✅ WebSocket support
- ✅ Admin panel

**Good luck! 🚀**

