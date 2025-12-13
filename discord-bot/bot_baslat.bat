@echo off
chcp 65001 >nul
title Captcha Crush Discord Bot
color 0A

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   🎫 Captcha Crush - Discord Ticket Bot          ║
echo ║                                                    ║
echo ║   🚀 Bot başlatılıyor...                          ║
echo ╚════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

if not exist .env (
    echo ❌ .env dosyası bulunamadı!
    echo.
    echo 📝 Önce .env dosyası oluştur:
    echo    1. .env.example dosyasını kopyala
    echo    2. .env olarak yeniden adlandır
    echo    3. Bot token'ını yapıştır
    echo.
    pause
    exit
)

echo ✅ .env dosyası bulundu
echo.
echo 📦 Gereksinimler kontrol ediliyor...
pip install -r requirements.txt -q

echo.
echo ✨ Bot başlatılıyor...
echo.
python ticket_bot.py

pause

