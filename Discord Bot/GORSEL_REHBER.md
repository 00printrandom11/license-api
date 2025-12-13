# 📸 GÖRSEL REHBER - Discord Bot Deploy (Ekran Görüntüleri ile)

> **Her adımda ne göreceğini bileceksin!**

---

## 📥 ADIM 1: GitHub Desktop İndir

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  GitHub Desktop                      │
│                                      │
│  [Download for Windows 64bit]       │
│                                      │
│  Version 3.3.x                       │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. https://desktop.github.com adresine git
2. "Download for Windows" butonuna tıkla
3. İndirilen dosyayı çalıştır
4. Kurulum otomatik yapılacak

---

## 🔑 ADIM 2: GitHub'a Giriş Yap

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  Sign in to GitHub                   │
│                                      │
│  Username: ________________          │
│  Password: ________________          │
│                                      │
│  [Sign in]                           │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. GitHub Desktop açıldığında "Sign in to GitHub.com" butonuna tıkla
2. Kullanıcı adı ve şifre gir
3. "Sign in" tıkla

---

## 📁 ADIM 3: Repository Oluştur

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  Create a New Repository             │
│                                      │
│  Name: captcha-crush-bot            │
│  Description: (optional)             │
│  Local Path: C:\Users\...\Discord Bot│
│  ☑ Initialize with README           │
│  Git ignore: None                    │
│  License: None                       │
│                                      │
│  [Create Repository]                 │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. Üst menüden **File** → **New Repository** tıkla
2. Name: `captcha-crush-bot` yaz
3. Local Path: `C:\Users\aLmiLa\Desktop\license-api\Discord Bot` seç
4. "Initialize with README" kutucuğunu işaretle
5. "Create Repository" butonuna tıkla

---

## ✅ ADIM 4: Commit (Dosyaları Kaydet)

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  Changes (15)                        │
│  ☑ ticket_bot.py                    │
│  ☑ requirements.txt                 │
│  ☑ .env.example                     │
│  ... (diğer dosyalar)               │
│                                      │
│  Summary: ___________________       │
│  Description: (optional)             │
│                                      │
│  [Commit to main]                    │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. Sol panelde değişen dosyaları göreceksin
2. **Summary** kutusuna yaz: `Initial commit`
3. **Commit to main** butonuna tıkla

---

## 🌐 ADIM 5: GitHub'a Yükle (Publish)

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  Publish Repository                  │
│                                      │
│  Name: captcha-crush-bot            │
│  Description: (optional)             │
│  ☐ Keep this code private           │
│                                      │
│  [Publish Repository]                │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. Üstte **Publish repository** butonuna tıkla
2. **"Keep this code private"** işaretini KALDIRIN
3. **Publish Repository** butonuna tıkla
4. ✅ Tebrikler! Kod GitHub'da!

---

## 🚀 ADIM 6: Render.com'a Git

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  Render                              │
│                                      │
│  Build, deploy, and scale your       │
│  apps with unparalleled ease        │
│                                      │
│  [Get Started]  [Sign In]           │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. https://render.com adresine git
2. **Get Started** butonuna tıkla
3. **Sign up with GitHub** seç
4. **Authorize Render** butonuna tıkla

---

## ⚙️ ADIM 7: Background Worker Oluştur

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  + New                               │
│  ├─ Static Site                      │
│  ├─ Web Service                      │
│  ├─ Private Service                  │
│  ├─ Background Worker  ← BU!         │
│  ├─ Cron Job                         │
│  └─ PostgreSQL                       │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. Sağ üstte **+ New** butonuna tıkla
2. **Background Worker** seç

---

## 🔗 ADIM 8: GitHub Repo Bağla

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  Connect a repository                │
│                                      │
│  ○ captcha-crush-bot                │
│  ○ license-api                       │
│  ○ other-repo                        │
│                                      │
│  [Configure account]                 │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. **captcha-crush-bot** seç
2. **Connect** butonuna tıkla

---

## 📝 ADIM 9: Ayarları Yap

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  Create Background Worker            │
│                                      │
│  Name: ___________________          │
│  Region: Frankfurt (EU Central)      │
│  Branch: main                        │
│  Runtime: Python 3                   │
│  Build Command: _______________     │
│  Start Command: _______________     │
│                                      │
│  Environment Variables               │
│  [Add Environment Variable]          │
│                                      │
│  [Create Background Worker]          │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. **Name**: `captcha-crush-bot`
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python ticket_bot.py`
4. Scroll down yap, **Environment Variables** bölümünü bul

---

## 🔐 ADIM 10: Environment Variables Ekle

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  Environment Variables               │
│                                      │
│  Key: ___________  Value: ________  │
│  [Remove]                            │
│                                      │
│  [Add Environment Variable]          │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
**3 KERE** "Add Environment Variable" butonuna tıkla ve şunları ekle:

#### 1. İlk Değişken:
```
Key: DISCORD_BOT_TOKEN
Value: (Bot tokenini yapıştır)
```

#### 2. İkinci Değişken:
```
Key: PANEL_API_URL
Value: https://license-api-5p24.onrender.com
```

#### 3. Üçüncü Değişken:
```
Key: DISCORD_BOT_API_KEY
Value: CaptchaCrushSecretKey2024!@#
```

---

## 🎉 ADIM 11: Deploy Et!

### Ne göreceksin:
```
┌─────────────────────────────────────┐
│  captcha-crush-bot                   │
│                                      │
│  ==> Building...                     │
│  ==> Installing dependencies...      │
│  ==> Build successful                │
│  ==> Starting bot...                 │
│  ✅ Bot hazır: Captcha Crush Bot    │
│  🌐 Sunucu sayısı: 1                │
└─────────────────────────────────────┘
```

**Ne yapacaksın:**
1. En altta **Create Background Worker** butonuna tıkla
2. Deploy başlayacak (2-3 dakika bekle)
3. ✅ "Bot hazır" mesajını görünce TAMAM!

---

## ✅ BITTI! BOT ÇALIŞIYOR

### Discord'da Kontrol:
```
Captcha Crush Bot  🟢  ← Yeşil nokta görmeli
```

### Render.com'da Kontrol:
```
┌─────────────────────────────────────┐
│  captcha-crush-bot                   │
│  ● Live                              │
│                                      │
│  Logs  |  Events  |  Environment    │
│                                      │
│  ✅ Bot hazır: Captcha Crush Bot    │
│  🌐 Sunucu sayısı: 1                │
└─────────────────────────────────────┘
```

---

## 🎊 TEBRIKLER!

✅ Bot artık 7/24 çalışıyor!
✅ Bilgisayarını kapatabilirsin!
✅ Bot Render.com sunucularında!

**Sorun olursa:** Render.com → Bot servisi → **Logs** sekmesine bak!

