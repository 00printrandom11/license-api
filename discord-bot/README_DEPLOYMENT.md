# 🤖 Discord Bot'u 24/7 Çalıştırma Rehberi (Acemiler İçin)

> **Amaç:** Bot'un bilgisayarın kapalı olduğunda bile çalışması için Render.com'da ücretsiz host etmek.

---

## ⚠️ ÖNEMLİ: İLK OKUMAN GEREKEN

**Bu rehber seni adım adım yönlendirecek. Her adımı sırayla yap, atlamadan ilerle!**

**Ne yapacağız?**
1. Bot dosyalarını GitHub'a yükleyeceğiz
2. Render.com'da ücretsiz hesap açacağız
3. Bot'u Render.com'a bağlayacağız
4. Bot bilgisayarın kapalı olsa bile 7/24 çalışacak!

**Gereken Sürе:** ~15 dakika

---

## 📋 ADIM 1: GitHub Hesabı Oluştur (Eğer Yoksa)

### 1.1 GitHub'a Git:
- Tarayıcında aç: **https://github.com**
- Sağ üstte **"Sign up"** (Kayıt Ol) butonuna tıkla
- Email, kullanıcı adı, şifre belirle
- Email'ini doğrula

### 1.2 GitHub Desktop İndir (Daha Kolay):
- Git: **https://desktop.github.com**
- **"Download for Windows"** butonuna tıkla
- İndir ve kur
- GitHub hesabınla giriş yap

---

## 📁 ADIM 2: Bot Klasörünü GitHub'a Yükle

### 2.1 GitHub Desktop'ta Repository Oluştur:

1. **GitHub Desktop'ı aç**
2. Üst menüden **"File"** → **"New repository"** tıkla
3. Ayarları yap:
   ```
   Name: captcha-crush-bot
   Description: Discord bot for Captcha Crush
   Local path: C:\Users\aLmiLa\Desktop\license-api\Discord Bot
   ✓ Initialize this repository with a README (İŞARETLE!)
   Git ignore: None
   License: None
   ```
4. **"Create Repository"** butonuna tıkla

### 2.2 Dosyaları Ekle ve Yükle:

1. GitHub Desktop'ta sol altta **"Summary"** kutusuna yaz:
   ```
   Initial commit: Discord bot
   ```

2. **"Commit to main"** butonuna tıkla

3. Üst menüden **"Publish repository"** butonuna tıkla
   - **"Keep this code private"** KALDIRIN (işareti kaldır)
   - **"Publish Repository"** butonuna tıkla

4. ✅ **Tebrikler! Bot dosyaları GitHub'da!**
   - Kontrol et: **https://github.com/KULLANICI_ADIN/captcha-crush-bot**

---

## 🌐 ADIM 3: Render.com Hesabı Oluştur

### 3.1 Render.com'a Kayıt Ol:

1. Git: **https://render.com**
2. Sağ üstte **"Get Started"** butonuna tıkla
3. **"Sign up with GitHub"** seç (GitHub hesabınla)
4. Render'ın GitHub erişim izni iste → **"Authorize Render"** tıkla
5. Email'ini doğrula

---

## 🚀 ADIM 4: Bot'u Render.com'da Çalıştır

### 4.1 Yeni Servis Oluştur:

1. Render Dashboard'da (ana sayfa) sağ üstte **"+ New"** butonuna tıkla
2. **"Background Worker"** seç (ÖNEMLİ!)

### 4.2 GitHub Repo'yu Bağla:

1. **"Connect a repository"** bölümünde:
   - Eğer repo görünmüyorsa: **"Configure account"** tıkla
   - Tüm repo'lara erişim ver VEYA sadece `captcha-crush-bot` seç
   - **"Install"** tıkla
2. Listeden **"captcha-crush-bot"** seç
3. **"Connect"** butonuna tıkla

### 4.3 Ayarları Yap:

Şimdi karşına çıkan formu doldur:

```
Name: captcha-crush-bot

Region: Frankfurt (EU Central) veya Ohio (US East)

Branch: main

Runtime: Python 3

Build Command: pip install -r requirements.txt

Start Command: python ticket_bot.py

Instance Type: Free
```

**NOT:** Hiçbir şeyi değiştirme, yukarıdaki gibi yaz!

### 4.4 Environment Variables (Çevre Değişkenleri) Ekle:

**ÇOK ÖNEMLİ!** Scroll down yap, **"Environment Variables"** bölümünü bul.

**"Add Environment Variable"** butonuna 3 kere tıkla ve şunları ekle:

#### 1. İlk Değişken:
```
Key: DISCORD_BOT_TOKEN
Value: (Discord Developer Portal'dan bot tokenini buraya yapıştır)
```

**Bot Token Nerede?**
1. Git: **https://discord.com/developers/applications**
2. Bot uygulamanı seç
3. Sol menüden **"Bot"** tıkla
4. **"Reset Token"** butonuna tıkla
5. Token'ı kopyala ve buraya yapıştır

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

### 4.5 Deploy Et:

1. En altta **"Create Background Worker"** butonuna tıkla
2. Deploy başlayacak (2-3 dakika sürer)
3. Ekranda logları göreceksin:
   ```
   ==> Building...
   ==> Installing dependencies...
   ==> Build successful
   ==> Starting bot...
   ✅ Bot hazır: Captcha Crush Bot
   ```

4. ✅ **Tebrikler! Bot artık 7/24 çalışıyor!**

---

## ✅ ADIM 5: Bot Çalışıyor mu Kontrol Et

### 5.1 Discord'da Kontrol:

1. Discord sunucuna git
2. Bot'un durumuna bak:
   - 🟢 Yeşil nokta = Çalışıyor ✅
   - ⚫ Gri nokta = Çalışmıyor ❌

### 5.2 Render.com'da Kontrol:

1. Render Dashboard'a dön
2. **"captcha-crush-bot"** servisine tıkla
3. **"Logs"** sekmesine bak
4. Göreceksin:
   ```
   ✅ Bot hazır: Captcha Crush Bot (ID: ...)
   🌐 Sunucu sayısı: 1
   ```

---

## 🎉 TAMAM! ŞİMDİ NE OLDU?

✅ **Bot artık Render.com sunucularında çalışıyor!**
✅ **Bilgisayarını kapatabilirsin, bot çalışmaya devam eder!**
✅ **Render.com ücretsiz plan: Ayda 750 saat (yeterli)**
✅ **Bot crash olursa otomatik yeniden başlar**

---

## 🔧 Bot'u Güncellemek İstersen

### GitHub Desktop ile:

1. Bot dosyalarında değişiklik yap (örnek: `ticket_bot.py`)
2. **GitHub Desktop**'ı aç
3. Sol altta **"Summary"** yaz: `Bot güncellendi`
4. **"Commit to main"** tıkla
5. **"Push origin"** butonuna tıkla
6. **Render.com otomatik algılayıp yeni versiyonu deploy eder!**

---

## ❓ Sorun Mu Var?

### Bot çalışmıyor:

1. **Render.com → Bot servisi → Logs** sekmesini kontrol et
2. Kırmızı hata mesajı varsa, `DISCORD_BOT_TOKEN` doğru mu kontrol et
3. Environment Variables'ı tekrar kontrol et

### Bot Discord'da görünmüyor:

1. Discord Developer Portal'da **"Bot"** sekmesini aç
2. **"Privileged Gateway Intents"** bölümünde şunları AÇIK yap:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
3. **"Save Changes"** tıkla
4. Render.com'da bot'u yeniden başlat: **"Manual Deploy" → "Deploy latest commit"**

---

## 🆘 YARDIM LAZIMSA

Render.com loglarını kontrol et, hata mesajını oku ve Google'da ara.

**Başarılar! 🚀**

