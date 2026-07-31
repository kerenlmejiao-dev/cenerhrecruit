"""
auth_users.py - Autenticación JWT para reclutadores y empresas

Distinto de auth.py (que solo protege endpoints admin/masivos con una
API key compartida). Este módulo maneja cuentas de usuario reales
(Usuario: rol owner/reclutador/empresa) con contraseña + JWT.

No hay auto-registro: las cuentas se crean solo por la dueña de la
plataforma (ver create_user.py).
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import Suscripcion, Usuario

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "600"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(usuario: Usuario) -> str:
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY no configurada en el servidor")

    expira = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "sub": str(usuario.id),
        "email": usuario.email,
        "rol": usuario.rol,
        "empresa_id": usuario.empresa_id,
        "exp": expira,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _decode_token(token: str) -> dict:
    if not SECRET_KEY:
        raise HTTPException(status_code=503, detail="SECRET_KEY no configurada; login deshabilitado")
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = _decode_token(credentials.credentials)
    usuario_id = payload.get("sub")
    usuario = db.query(Usuario).filter_by(id=int(usuario_id)).first()

    if not usuario or not usuario.activo:
        raise HTTPException(status_code=401, detail="Usuario inválido o inactivo")

    return usuario


def require_role(*roles: str):
    """Dependency factory: solo permite continuar si el usuario tiene uno de los roles dados."""

    def dependency(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        if usuario.rol not in roles:
            raise HTTPException(status_code=403, detail="No autorizado para este recurso")
        return usuario

    return dependency


def require_membresia_activa(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Usuario:
    """Como require_role('owner', 'reclutador'), pero además exige que el
    reclutador tenga una membresía paga vigente (ver Suscripcion en
    models.py) -- ningún plan es gratuito. El owner no necesita membresía.

    Mientras dLocal termina de configurarse, la membresía se activa a mano
    con POST /api/admin/activar-membresia (ver admin_router.py); cuando
    dLocal esté listo, el mismo webhook de pago puede activarla en vez de
    hacerlo manualmente."""
    if usuario.rol not in ("owner", "reclutador"):
        raise HTTPException(status_code=403, detail="No autorizado para este recurso")
    if usuario.rol == "owner":
        return usuario

    suscripcion = (
        db.query(Suscripcion)
        .filter_by(usuario_id=usuario.id)
        .order_by(Suscripcion.creado_en.desc())
        .first()
    )
    vigente = (
        suscripcion
        and suscripcion.estado == "activa"
        and suscripcion.fecha_renovacion
        and suscripcion.fecha_renovacion > datetime.utcnow()
    )
    if not vigente:
        if suscripcion and suscripcion.estado == "activa":
            suscripcion.estado = "vencida"
            db.commit()
        raise HTTPException(
            status_code=402,
            detail="Necesitas una membresía activa para usar el panel de reclutador.",
        )
    return usuario
