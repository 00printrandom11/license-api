"""
Database Migration Script - Yeni Kolonları Ekle
Render.com Shell'de çalıştır!
"""

import os
from sqlalchemy import create_engine, text

# Database URL'yi al
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./licenses.db")

# PostgreSQL URL düzeltmesi
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

print("🔧 Database Migration Başlıyor...")
print(f"📊 Database: {DATABASE_URL[:30]}...")

with engine.connect() as conn:
    try:
        # Licenses tablosuna yeni kolonları ekle
        print("\n1️⃣ hwid_change_count ekleniyor...")
        conn.execute(text("ALTER TABLE licenses ADD COLUMN hwid_change_count INTEGER DEFAULT 0"))
        conn.commit()
        print("   ✅ Eklendi")
    except Exception as e:
        if "already exists" in str(e) or "duplicate column" in str(e).lower():
            print("   ⚠️ Zaten var")
        else:
            print(f"   ❌ Hata: {e}")

    try:
        print("\n2️⃣ ip_change_count ekleniyor...")
        conn.execute(text("ALTER TABLE licenses ADD COLUMN ip_change_count INTEGER DEFAULT 0"))
        conn.commit()
        print("   ✅ Eklendi")
    except Exception as e:
        if "already exists" in str(e) or "duplicate column" in str(e).lower():
            print("   ⚠️ Zaten var")
        else:
            print(f"   ❌ Hata: {e}")

    try:
        print("\n3️⃣ check_count ekleniyor...")
        conn.execute(text("ALTER TABLE licenses ADD COLUMN check_count INTEGER DEFAULT 0"))
        conn.commit()
        print("   ✅ Eklendi")
    except Exception as e:
        if "already exists" in str(e) or "duplicate column" in str(e).lower():
            print("   ⚠️ Zaten var")
        else:
            print(f"   ❌ Hata: {e}")

    try:
        print("\n4️⃣ abuse_score ekleniyor...")
        conn.execute(text("ALTER TABLE licenses ADD COLUMN abuse_score INTEGER DEFAULT 0"))
        conn.commit()
        print("   ✅ Eklendi")
    except Exception as e:
        if "already exists" in str(e) or "duplicate column" in str(e).lower():
            print("   ⚠️ Zaten var")
        else:
            print(f"   ❌ Hata: {e}")

    try:
        print("\n5️⃣ is_banned ekleniyor...")
        conn.execute(text("ALTER TABLE licenses ADD COLUMN is_banned BOOLEAN DEFAULT 0"))
        conn.commit()
        print("   ✅ Eklendi")
    except Exception as e:
        if "already exists" in str(e) or "duplicate column" in str(e).lower():
            print("   ⚠️ Zaten var")
        else:
            print(f"   ❌ Hata: {e}")

    try:
        print("\n6️⃣ last_seen_ip ekleniyor...")
        conn.execute(text("ALTER TABLE licenses ADD COLUMN last_seen_ip VARCHAR(64) DEFAULT ''"))
        conn.commit()
        print("   ✅ Eklendi")
    except Exception as e:
        if "already exists" in str(e) or "duplicate column" in str(e).lower():
            print("   ⚠️ Zaten var")
        else:
            print(f"   ❌ Hata: {e}")

print("\n" + "="*50)
print("✅ Migration Tamamlandı!")
print("🔄 Şimdi servisi restart edin")
print("="*50)

