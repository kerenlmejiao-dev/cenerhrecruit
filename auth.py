"""
auth.py - Autenticación mínima compartida (API key de administrador)

Protege endpoints administrativos/masivos (listados completos de candidatos,
sincronización con CRM, etc.) con una API key compartida definida en la
variable de entorno ADMIN_API_KEY (ver .env.example).
"""

import os
import secrets

from fastapi import Header, HTTPException

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "")


def require_admin(x_admin_key: str = Header(default="")) -> None:
    if not ADMIN_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="ADMIN_API_KEY no configurada en el servidor; acceso admin deshabilitado",
        )
    if not secrets.compare_digest(x_admin_key, ADMIN_API_KEY):
        raise HTTPException(status_code=401, detail="Credencial de administrador inválida")
