from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    Text
)
from datetime import datetime, timezone
from database import Base


def utcnow():
    """ Tek zaman standardı """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class License(Base):
    __tablename__ = "licenses"

    # =========================
    # CORE
    # =========================
    id = Column(Integer, primary_key=True, index=True)

    license_key = Column(String(64), unique=True, nullable=False, index=True)
    hwid = Column(String(256), default="", index=True)

    duration_days = Column(Float, default=30)
    is_active = Column(Boolean, default=False)  # 🔒 Varsayılan PASİF - Admin aktif edecek
    is_banned = Column(Boolean, default=False)  # admin hard-ban

    # =========================
    # TIME
    # =========================
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    activation_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)

    last_check_at = Column(DateTime, nullable=True)

    # =========================
    # NETWORK
    # =========================
    client_ip = Column(String(64), default="")
    last_seen_ip = Column(String(64), default="")

    # =========================
    # SECURITY & ABUSE
    # =========================
    hwid_change_count = Column(Integer, default=0)
    ip_change_count = Column(Integer, default=0)
    check_count = Column(Integer, default=0)
    abuse_score = Column(Integer, default=0)

    # =========================
    # META
    # =========================
    note = Column(String(500), default="")

    # =========================
    # PROPERTIES
    # =========================
    @property
    def remaining_seconds(self) -> int:
        if not self.expiry_date:
            return 0
        sec = int((self.expiry_date - utcnow()).total_seconds())
        return max(sec, 0)

    @property
    def remaining_days(self) -> float:
        if not self.expiry_date:
            return 0.0
        return round(self.remaining_seconds / 86400, 2)

    @property
    def remaining_human(self) -> str:
        sec = self.remaining_seconds
        if sec <= 0:
            return "Süre Doldu"

        days = sec // 86400
        hours = (sec % 86400) // 3600
        minutes = (sec % 3600) // 60

        if days > 0:
            return f"{days}g {hours}s"
        if hours > 0:
            return f"{hours}s {minutes}dk"
        return f"{minutes}dk"

    @property
    def program_running(self) -> bool:
        """
        Son kontrol 60 saniye içindeyse program çalışıyor kabul edilir
        """
        if not self.last_check_at:
            return False
        return (utcnow() - self.last_check_at).total_seconds() <= 60

    @property
    def is_expired(self) -> bool:
        if not self.expiry_date:
            return False
        return utcnow() > self.expiry_date


# =========================
# AUDIT LOG SYSTEM
# =========================
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=utcnow, index=True)

    # Kim ne yaptı
    action = Column(String(100), nullable=False, index=True)
    target = Column(String(100))  # license_key veya diğer
    details = Column(Text, default="")

    # Kim yaptı
    user = Column(String(100), default="system")
    ip_address = Column(String(64), default="")

    # Sonuç
    success = Column(Boolean, default=True)


# =========================
# ADMIN SESSION TRACKING
# =========================
class AdminSession(Base):
    __tablename__ = "admin_sessions"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    ip_address = Column(String(64), nullable=False)

    login_at = Column(DateTime, default=utcnow)
    last_activity = Column(DateTime, default=utcnow)
    logout_at = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True)
    session_token = Column(String(256), unique=True)


# =========================
# BANNED HWID SYSTEM
# =========================
class BannedHWID(Base):
    __tablename__ = "banned_hwids"

    id = Column(Integer, primary_key=True, index=True)
    hwid = Column(String(256), unique=True, nullable=False, index=True)

    # Neden banlandı
    license_key = Column(String(64), nullable=False)  # Hangi lisans
    reason = Column(String(500), default="Aynı key farklı PC'de kullanıldı")

    # Diğer HWID (eşleşen)
    conflicting_hwid = Column(String(256), default="")

    # Kim banladı
    banned_by = Column(String(100), default="system")  # system veya admin
    banned_at = Column(DateTime, default=utcnow, index=True)

    # Detaylar
    ip_address = Column(String(64), default="")
    details = Column(Text, default="")

