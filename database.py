import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================
# DATABASE CONFIG
# =========================

# Eğer ENV'de DATABASE_URL varsa onu kullan
# Yoksa default olarak SQLite (Render / VPS uyumlu)
BASE_DIR = os.getenv("DB_DIR", "/var/data")
os.makedirs(BASE_DIR, exist_ok=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'licenses.db')}"
)

# =========================
# ENGINE
# =========================

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,
    future=True
)

# =========================
# SESSION
# =========================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # FastAPI için kritik
)

# =========================
# BASE
# =========================

Base = declarative_base()

# =========================
# DEPENDENCY
# =========================

def get_db():
    """
    FastAPI dependency.
    Her request için güvenli DB session sağlar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# INIT DB (OPSİYONEL)
# =========================

def init_db():
    """
    Tüm modelleri oluşturur.
    main.py içinde bir kez çağırman yeterli.
    """
    import models  # noqa: F401
    Base.metadata.create_all(bind=engine)