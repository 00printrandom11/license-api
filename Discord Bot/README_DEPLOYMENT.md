# Discord Bot Render.com Deployment

Bu klasör Discord bot'unu Render.com'da host etmek için gerekli dosyaları içerir.

## 🚀 Deployment Adımları:

### 1️⃣ GitHub Repository Oluştur:
```bash
cd "C:\Users\aLmiLa\Desktop\license-api\Discord Bot"
git init
git add .
git commit -m "Initial commit: Discord bot"
git remote add origin https://github.com/KULLANICI_ADI/discord-bot.git
git push -u origin main
```

### 2️⃣ Render.com'da Worker Servisi Oluştur:
1. https://dashboard.render.com/new/worker
2. **Connect Repository**: GitHub'daki bot repo'sunu seç
3. **Name**: `captcha-crush-bot`
4. **Environment**: `Python 3`
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `python ticket_bot.py`

### 3️⃣ Environment Variables Ekle:
```
DISCORD_BOT_TOKEN = (Discord Developer Portal'dan al)
PANEL_API_URL = https://license-api-5p24.onrender.com
DISCORD_BOT_API_KEY = CaptchaCrushSecretKey2024!@#
```

### 4️⃣ Deploy:
- **"Create Worker"** butonuna tıkla
- Bot 24/7 çalışmaya başlayacak! ✅

## 📝 Notlar:

- ✅ Bot bilgisayarın kapalı olması durumunda çalışmaya devam eder
- ✅ Render.com Free Plan: 750 saat/ay (yeterli)
- ✅ Otomatik restart (crash durumunda)
- ✅ Log takibi: Render Dashboard'dan

## 🔧 Güncelleme:

GitHub'a push yaptığında Render otomatik deploy eder:
```bash
git add .
git commit -m "Update bot"
git push origin main
```

