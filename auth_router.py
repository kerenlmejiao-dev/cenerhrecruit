"""
auth_router.py - Endpoints de login para reclutador/empresa/owner

Las cuentas de empresa/owner se crean con create_user.py (ejecutado solo por
la dueña de la plataforma). Los reclutadores además pueden autorregistrarse
en /registro, protegido con un código de invitación (ver REGISTRO_RECLUTADOR_CODIGO
en .env) para que no cualquiera pueda crear una cuenta con acceso a vacantes
y datos de candidatos.
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from auth_users import create_access_token, get_current_user, hash_password, verify_password
from database import get_db
from email_sender import EnviadorEmail
from models import Usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

RESET_TOKEN_MINUTOS = 60


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


class RegistroReclutadorPayload(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    password: str = Field(..., min_length=8)
    codigo_invitacion: str
    telefono: Optional[str] = None  # WhatsApp, para notificarte nuevas aplicaciones


@router.post("/registro")
def registro_reclutador(payload: RegistroReclutadorPayload, db: Session = Depends(get_db)):
    codigo_esperado = os.getenv("REGISTRO_RECLUTADOR_CODIGO", "")
    if not codigo_esperado:
        raise HTTPException(status_code=503, detail="El autorregistro no está habilitado todavía")
    if payload.codigo_invitacion != codigo_esperado:
        raise HTTPException(status_code=401, detail="Código de invitación inválido")

    if db.query(Usuario).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con este email")

    usuario = Usuario(
        email=payload.email,
        password_hash=hash_password(payload.password),
        nombre=payload.nombre,
        rol="reclutador",
        telefono=payload.telefono,
    )
    db.add(usuario)
    db.commit()

    token = create_access_token(usuario)
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "empresa_id": usuario.empresa_id,
            "documento": usuario.documento,
        },
    }


@router.post("/login")
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(email=payload.email).first()

    if not usuario or not usuario.activo or not verify_password(payload.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    from datetime import datetime
    usuario.ultimo_login = datetime.utcnow()
    db.commit()

    token = create_access_token(usuario)
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "empresa_id": usuario.empresa_id,
            "documento": usuario.documento,
        },
    }


@router.get("/me")
def me(usuario: Usuario = Depends(get_current_user)):
    return {
        "id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "rol": usuario.rol,
        "empresa_id": usuario.empresa_id,
        "documento": usuario.documento,
    }


class OlvidePasswordPayload(BaseModel):
    email: EmailStr


@router.post("/olvide-password")
def olvide_password(payload: OlvidePasswordPayload, db: Session = Depends(get_db)):
    """Sirve para cualquier rol (candidato, reclutador, empresa, owner) --
    todos son cuentas Usuario. Siempre responde igual exista o no el correo,
    para no revelar qué emails tienen cuenta."""
    usuario = db.query(Usuario).filter_by(email=payload.email).first()
    if usuario and usuario.activo:
        usuario.reset_token = secrets.token_urlsafe(32)
        usuario.reset_token_expira = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_MINUTOS)
        db.commit()

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        link = f"{frontend_url}/restablecer-password/{usuario.reset_token}"
        EnviadorEmail.enviar_recuperacion_password(usuario.email, usuario.nombre, link)

    return {"status": "success", "mensaje": "Si el correo tiene una cuenta, te enviamos un enlace para restablecer tu contraseña."}


class RestablecerPasswordPayload(BaseModel):
    token: str
    password: str = Field(..., min_length=8)


@router.post("/restablecer-password")
def restablecer_password(payload: RestablecerPasswordPayload, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(reset_token=payload.token).first()
    if not usuario or not usuario.reset_token_expira or usuario.reset_token_expira < datetime.utcnow():
        raise HTTPException(status_code=400, detail="El enlace es inválido o ya expiró. Solicita uno nuevo.")

    usuario.password_hash = hash_password(payload.password)
    usuario.reset_token = None
    usuario.reset_token_expira = None
    db.commit()

    token = create_access_token(usuario)
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "empresa_id": usuario.empresa_id,
            "documento": usuario.documento,
        },
    }
