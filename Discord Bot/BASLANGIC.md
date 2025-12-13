# ⚡ HIZLI BAŞLANGIÇ - Discord Bot Deploy

> **5 dakikada bot'unu 7/24 çalışır hale getir!**

---

## 🎯 HIZLI ADIMLAR

### 1. GitHub Desktop İndir ve Kur
- İndir: https://desktop.github.com
- Kur ve GitHub hesabınla giriş yap

### 2. Bot'u GitHub'a Yükle
1. GitHub Desktop'ı aç
2. File → New Repository
3. Name: `captcha-crush-bot`
4. Path: `C:\Users\aLmiLa\Desktop\license-api\Discord Bot`
5. Create Repository
6. Commit to main
7. Publish repository

### 3. Render.com'a Git
- https://render.com
- Sign up with GitHub

### 4. Bot'u Deploy Et
1. Render'da: **+ New** → **Background Worker**
2. GitHub repo'yu seç: `captcha-crush-bot`
3. Ayarlar:
   ```
   Name: captcha-crush-bot
   Build Command: pip install -r requirements.txt
   Start Command: python ticket_bot.py
   ```
4. Environment Variables ekle:
   ```
   DISCORD_BOT_TOKEN = (Bot tokenin)
   PANEL_API_URL = https://license-api-5p24.onrender.com
   DISCORD_BOT_API_KEY = CaptchaCrushSecretKey2024!@#
   ```
5. **Create Background Worker**

### 5. Kontrol Et
- Discord'da bot 🟢 yeşil olmalı
- Render logs'ta: `✅ Bot hazır` görmeli

---

## ✅ BITTI!

Bot artık 7/24 çalışıyor! Bilgisayarını kapatabilirsin.

**Detaylı rehber için:** `README_DEPLOYMENT.md` dosyasını oku.

