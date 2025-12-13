import os
from datetime import datetime, timedelta, timezone
from typing import Dict
import hashlib
import secrets

from fastapi import (
    FastAPI, Request, Depends, Form, HTTPException,
    WebSocket, WebSocketDisconnect
)
from fastapi.responses import (
    HTMLResponse, RedirectResponse,
    JSONResponse, PlainTextResponse
)
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel

from database import Base, engine, get_db, init_db
import models  # 🔥 TABLOLARIN YÜKLENMESİ İÇİN ŞART
from models import License, AuditLog, AdminSession, BannedHWID

# =========================
# FASTAPI
# =========================
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# 🔥 Render restart sonrası tablo garantisi
init_db()

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET_KEY")
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    same_site="lax",
    https_only=True
)

templates = Jinja2Templates(directory="templates")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# 🔒 PANEL IP KISITLAMASI - Sadece bu IP'ler girebilir!
# Render.com Environment Variables'a ekle: ALLOWED_PANEL_IPS=95.70.194.254
ALLOWED_PANEL_IPS = set(
    ip.strip() for ip in os.getenv("ALLOWED_PANEL_IPS", "95.70.194.254").split(",") if ip.strip()
)

# =========================
# WEBSOCKET CONNECTIONS
# =========================
active_sockets: Dict[str, WebSocket] = {}

# =========================
# RATE LIMITING & SECURITY
# =========================
login_attempts: Dict[str, list] = {}  # IP -> [timestamp, ...]

def check_rate_limit(ip: str, max_attempts: int = 5, window_seconds: int = 300) -> bool:
    """Rate limiting - 5 dakikada 5 deneme"""
    now = datetime.now(timezone.utc)

    if ip not in login_attempts:
        login_attempts[ip] = []

    # Eski denemeleri temizle
    login_attempts[ip] = [
        ts for ts in login_attempts[ip]
        if (now - ts).total_seconds() < window_seconds
    ]

    if len(login_attempts[ip]) >= max_attempts:
        return False

    login_attempts[ip].append(now)
    return True

def log_action(
    db: Session,
    action: str,
    target: str = "",
    details: str = "",
    user: str = "system",
    ip: str = "",
    success: bool = True
):
    """Audit log kaydı"""
    log = AuditLog(
        action=action,
        target=target,
        details=details,
        user=user,
        ip_address=ip,
        success=success
    )
    db.add(log)
    db.commit()

def calculate_abuse_score(lic: License) -> int:
    """
    Abuse skoru hesapla - SADECE HWID ÖNEMLİ

    IP değişimi: ARTIK ÖNEMLİ DEĞİL (modem, mobil vb.)
    HWID değişimi: ÇOK CİDDİ - Farklı PC = crack/paylaşım
    """
    score = 0

    # HWID değişimi - TEK ÖNEMLİ KURAL
    # 1 HWID değişimi = farklı PC = otomatik ban
    if lic.hwid_change_count >= 1:
        score = 100  # Direkt ban için yüksek skor

    return score

def ban_hwid(
    db: Session,
    hwid: str,
    license_key: str,
    reason: str,
    conflicting_hwid: str = "",
    banned_by: str = "system",
    ip: str = "",
    details: str = ""
):
    """HWID'yi banlama fonksiyonu"""
    # Zaten banlı mı kontrol et
    existing = db.query(BannedHWID).filter(BannedHWID.hwid == hwid).first()
    if existing:
        return  # Zaten banlı

    banned = BannedHWID(
        hwid=hwid,
        license_key=license_key,
        reason=reason,
        conflicting_hwid=conflicting_hwid,
        banned_by=banned_by,
        ip_address=ip,
        details=details
    )
    db.add(banned)
    db.commit()

    # Log'a kaydet
    log_action(db, "hwid_banned", hwid[:16] + "...",
               f"License: {license_key}, Reason: {reason}",
               banned_by, ip, True)

def is_hwid_banned(db: Session, hwid: str) -> bool:
    """HWID banlı mı kontrol et"""
    return db.query(BannedHWID).filter(BannedHWID.hwid == hwid).count() > 0

# =========================
# TIME (TEK OTORİTE)
# =========================
def server_utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

# =========================
# IP / AUTH
# =========================
def get_client_ip(request: Request) -> str:
    for h in ("x-forwarded-for", "x-real-ip"):
        if h in request.headers:
            return request.headers[h].split(",")[0].strip()
    return request.client.host if request.client else "0.0.0.0"

def ensure_panel_ip(request: Request):
    if ALLOWED_PANEL_IPS and get_client_ip(request) not in ALLOWED_PANEL_IPS:
        raise HTTPException(status_code=403)

def is_logged_in(request: Request) -> bool:
    return bool(request.session.get("admin_logged_in"))

def require_login(request: Request):
    if not is_logged_in(request):
        raise HTTPException(status_code=401)

# =========================
# API MODELS
# =========================
class LicenseRequest(BaseModel):
    license_key: str
    hwid: str
    ip_address: str | None = None

# =========================
# ROOT
# =========================
@app.get("/", response_class=PlainTextResponse)
async def root():
    return "License API running"

# =========================
# SERVER TIME
# =========================
@app.get("/api/time")
async def api_time():
    now = datetime.now(timezone.utc)
    return {
        "utc_timestamp": now.timestamp(),
        "utc_iso": now.isoformat()
    }

# =========================
# ACTIVATE / CHECK
# =========================
@app.post("/api/activate")
async def api_activate(
    payload: LicenseRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = payload.ip_address or get_client_ip(request)

    # HWID banlı mı kontrol et
    if is_hwid_banned(db, payload.hwid):
        log_action(db, "banned_hwid_attempt", payload.hwid[:16] + "...",
                   f"License: {payload.license_key}", "client", client_ip, False)
        return {"status": "inactive", "reason": "HWID banned"}

    lic = db.query(License).filter(
        License.license_key == payload.license_key
    ).first()

    if not lic or not lic.is_active or lic.is_banned:
        log_action(db, "activate_failed", payload.license_key, f"IP: {client_ip}", "client", client_ip, False)
        return {"status": "inactive"}

    now = server_utcnow()

    if lic.expiry_date and now > lic.expiry_date:
        lic.is_active = False
        db.commit()
        log_action(db, "activate_expired", lic.license_key, "", "client", client_ip, False)
        return {"status": "inactive"}

    # HWID kontrolü - FARKLІ PC TESPİTİ
    if not lic.hwid:
        # İlk aktivasyon
        lic.hwid = payload.hwid
        lic.activation_date = now
        lic.expiry_date = now + timedelta(days=lic.duration_days)
        log_action(db, "first_activation", lic.license_key, f"HWID: {payload.hwid[:16]}...", "client", client_ip, True)

    elif lic.hwid != payload.hwid:
        # 🚨 FARKLI PC TESPİT EDİLDİ!
        old_hwid = lic.hwid
        new_hwid = payload.hwid

        # Her iki HWID'yi de banla
        ban_hwid(db, old_hwid, lic.license_key,
                 "Aynı key farklı PC'de kullanıldı (Eski PC)",
                 new_hwid, "system", client_ip,
                 f"Conflict detected: {old_hwid[:16]} vs {new_hwid[:16]}")

        ban_hwid(db, new_hwid, lic.license_key,
                 "Aynı key farklı PC'de kullanıldı (Yeni PC)",
                 old_hwid, "system", client_ip,
                 f"Conflict detected: {new_hwid[:16]} vs {old_hwid[:16]}")

        # Lisansı devre dışı bırak
        lic.is_active = False
        lic.is_banned = True
        lic.hwid_change_count += 1
        lic.abuse_score = 100

        db.commit()

        log_action(db, "hwid_conflict_detected", lic.license_key,
                   f"Old HWID: {old_hwid[:16]}..., New HWID: {new_hwid[:16]}... - BOTH BANNED",
                   "system", client_ip, True)

        return {
            "status": "inactive",
            "reason": "HWID conflict - Both PCs banned"
        }

    lic.last_check_at = now
    lic.client_ip = client_ip
    lic.check_count += 1
    db.commit()

    remaining = max(0, int((lic.expiry_date - now).total_seconds()))
    return {
        "status": "active",
        "remaining_seconds": remaining,
        "server_timestamp": datetime.now(timezone.utc).timestamp()
    }

@app.post("/api/check")
async def api_check(
    payload: LicenseRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = payload.ip_address or get_client_ip(request)

    # HWID banlı mı kontrol et
    if is_hwid_banned(db, payload.hwid):
        return {"status": "inactive", "reason": "HWID banned"}

    lic = db.query(License).filter(
        License.license_key == payload.license_key,
        License.hwid == payload.hwid
    ).first()

    if not lic or not lic.is_active or lic.is_banned:
        return {"status": "inactive"}

    now = server_utcnow()

    if lic.expiry_date and now > lic.expiry_date:
        lic.is_active = False
        db.commit()
        return {"status": "inactive"}

    lic.last_check_at = now
    lic.client_ip = client_ip
    lic.check_count += 1
    db.commit()

    remaining = max(0, int((lic.expiry_date - now).total_seconds()))
    return {
        "status": "active",
        "remaining_seconds": remaining,
        "server_timestamp": datetime.now(timezone.utc).timestamp()
    }

# =========================
# LOGIN
# =========================
@app.get("/panel/login", response_class=HTMLResponse)
async def login_page(request: Request):
    ensure_panel_ip(request)
    if is_logged_in(request):
        return RedirectResponse("/panel", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/panel/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    ensure_panel_ip(request)
    client_ip = get_client_ip(request)

    # Rate limiting kontrolü
    if not check_rate_limit(client_ip):
        log_action(db, "login_rate_limit", username, f"Too many attempts", username, client_ip, False)
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Çok fazla deneme! 5 dakika bekleyin."}
        )

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["admin_logged_in"] = True
        request.session["admin_ip"] = client_ip
        log_action(db, "admin_login", username, f"Success", username, client_ip, True)
        return RedirectResponse("/panel", status_code=303)

    log_action(db, "login_failed", username, f"Invalid credentials", username, client_ip, False)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Hatalı giriş"}
    )

@app.get("/panel/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/panel/login", status_code=303)

# =========================
# PANEL
# =========================
@app.get("/panel", response_class=HTMLResponse)
async def panel_dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    ensure_panel_ip(request)
    require_login(request)

    now = server_utcnow()
    licenses = db.query(License).order_by(desc(License.id)).all()

    # Metrics hesaplama
    total_licenses = len(licenses)
    active_now = sum(1 for lic in licenses if lic.last_check_at and (now - lic.last_check_at).total_seconds() < 60)
    banned_count = sum(1 for lic in licenses if lic.is_banned)
    expired_count = sum(1 for lic in licenses if lic.expiry_date and now > lic.expiry_date)

    # Son 20 audit log
    recent_logs = db.query(AuditLog).order_by(desc(AuditLog.timestamp)).limit(20).all()

    # Banlı HWID'ler
    banned_hwids = db.query(BannedHWID).order_by(desc(BannedHWID.banned_at)).all()

    return templates.TemplateResponse(
        "panel.html",
        {
            "request": request,
            "licenses": licenses,
            "now": now,
            "metrics": {
                "total": total_licenses,
                "active_now": active_now,
                "banned": banned_count,
                "expired": expired_count,
                "banned_hwids": len(banned_hwids)
            },
            "recent_logs": recent_logs,
            "banned_hwids": banned_hwids
        }
    )

# =========================
# WEBSOCKET PUSH
# =========================
async def push_refresh(lic: License):
    ws = active_sockets.get(lic.license_key)
    if ws:
        try:
            await ws.send_json({"action": "refresh"})
        except:
            active_sockets.pop(lic.license_key, None)

# =========================
# PANEL ACTIONS
# =========================
@app.post("/panel/licenses/create")
async def panel_create(
    request: Request,
    duration_days: int = Form(...),
    note: str = Form(""),
    db: Session = Depends(get_db)
):
    ensure_panel_ip(request)
    require_login(request)

    import uuid
    key = uuid.uuid4().hex[:24]
    lic = License(
        license_key=key,
        duration_days=duration_days,
        note=note,
        is_active=True
    )
    db.add(lic)
    db.commit()

    log_action(db, "license_created", key, f"Duration: {duration_days} days, Note: {note}", "admin", get_client_ip(request), True)

    return RedirectResponse("/panel", status_code=303)

@app.post("/panel/licenses/add_time")
async def panel_add_time(
    request: Request,
    license_id: int = Form(...),
    amount: int = Form(...),
    unit: str = Form(...),
    db: Session = Depends(get_db)
):
    ensure_panel_ip(request)
    require_login(request)

    lic = db.query(License).filter(License.id == license_id).first()
    if lic and lic.expiry_date:
        old_expiry = lic.expiry_date
        if unit == "hours":
            lic.expiry_date += timedelta(hours=amount)
        else:
            lic.expiry_date += timedelta(days=amount)
        db.commit()

        log_action(db, "time_added", lic.license_key, f"+{amount} {unit}", "admin", get_client_ip(request), True)
        await push_refresh(lic)

    return RedirectResponse("/panel", status_code=303)

@app.post("/panel/licenses/{lid}/toggle")
async def panel_toggle(
    request: Request,
    lid: int,
    db: Session = Depends(get_db)
):
    ensure_panel_ip(request)
    require_login(request)

    lic = db.query(License).filter(License.id == lid).first()
    if lic:
        lic.is_active = not lic.is_active
        db.commit()

        log_action(db, "status_toggled", lic.license_key, f"New status: {'active' if lic.is_active else 'inactive'}", "admin", get_client_ip(request), True)
        await push_refresh(lic)

    return RedirectResponse("/panel", status_code=303)

@app.post("/panel/licenses/{lid}/reset_hwid")
async def panel_reset(
    request: Request,
    lid: int,
    db: Session = Depends(get_db)
):
    ensure_panel_ip(request)
    require_login(request)

    lic = db.query(License).filter(License.id == lid).first()
    if lic:
        old_hwid = lic.hwid
        lic.hwid = ""
        lic.is_active = False
        db.commit()

        log_action(db, "hwid_reset", lic.license_key, f"Old HWID: {old_hwid[:16]}...", "admin", get_client_ip(request), True)
        await push_refresh(lic)

    return RedirectResponse("/panel", status_code=303)

@app.post("/panel/licenses/{lid}/delete")
async def panel_delete(
    request: Request,
    lid: int,
    db: Session = Depends(get_db)
):
    ensure_panel_ip(request)
    require_login(request)

    lic = db.query(License).filter(License.id == lid).first()
    if lic:
        key = lic.license_key
        await push_refresh(lic)
        db.delete(lic)
        db.commit()

        log_action(db, "license_deleted", key, "", "admin", get_client_ip(request), True)

    return RedirectResponse("/panel", status_code=303)

@app.post("/panel/licenses/{lid}/ban")
async def panel_ban(
    request: Request,
    lid: int,
    db: Session = Depends(get_db)
):
    ensure_panel_ip(request)
    require_login(request)

    lic = db.query(License).filter(License.id == lid).first()
    if lic:
        lic.is_banned = not lic.is_banned
        db.commit()

        log_action(db, "ban_toggled", lic.license_key, f"Banned: {lic.is_banned}", "admin", get_client_ip(request), True)
        await push_refresh(lic)

    return RedirectResponse("/panel", status_code=303)

@app.post("/panel/licenses/{lid}/reset_abuse")
async def panel_reset_abuse(
    request: Request,
    lid: int,
    db: Session = Depends(get_db)
):
    ensure_panel_ip(request)
    require_login(request)

    lic = db.query(License).filter(License.id == lid).first()
    if lic:
        lic.abuse_score = 0
        lic.hwid_change_count = 0
        lic.ip_change_count = 0
        db.commit()

        log_action(db, "abuse_reset", lic.license_key, "", "admin", get_client_ip(request), True)

    return RedirectResponse("/panel", status_code=303)

# =========================
# WEBSOCKET ENDPOINT
# =========================
@app.websocket("/ws/{license_key}")
async def license_ws(ws: WebSocket, license_key: str):
    await ws.accept()
    active_sockets[license_key] = ws
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        active_sockets.pop(license_key, None)