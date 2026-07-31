"""
migraciones.py - Ajustes de esquema que Base.metadata.create_all() no cubre:
columnas nuevas en tablas que ya existían en una instalación anterior, y el
cambio de candidatos.vacante_id a opcional (bolsa de talento).

Se ejecuta una vez al arrancar la API, después de create_all(). Es seguro
correrlo repetidas veces: cada paso revisa si hace falta antes de alterar.
Solo actúa sobre Postgres (producción) — en SQLite local el esquema ya se
gestiona a mano durante el desarrollo, y ALTER TABLE ADD COLUMN IF NOT EXISTS
no existe en SQLite de la misma forma.
"""

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def aplicar_migraciones(engine: Engine) -> None:
    if engine.dialect.name != "postgresql":
        return

    inspector = inspect(engine)

    with engine.begin() as conn:
        # vacantes: ciclo de vida (borrador/activa/inactiva) y requisitos para
        # el análisis de compatibilidad por IA
        columnas_vacantes = {c["name"] for c in inspector.get_columns("vacantes")}
        if "estado" not in columnas_vacantes:
            conn.execute(text("ALTER TABLE vacantes ADD COLUMN estado VARCHAR(20) DEFAULT 'activa'"))
            # Las vacantes que ya existían en producción ya estaban recibiendo
            # aplicaciones, así que arrancan en "activa", no en "borrador".
            conn.execute(text("UPDATE vacantes SET estado = 'activa' WHERE estado IS NULL"))
        if "requisitos" not in columnas_vacantes:
            conn.execute(text("ALTER TABLE vacantes ADD COLUMN requisitos TEXT"))

        # candidatos: perfil de bolsa de talento (sin vacante) y status de
        # reclutamiento visible para el candidato
        columnas_candidatos = {c["name"] for c in inspector.get_columns("candidatos")}
        if "status_reclutamiento" not in columnas_candidatos:
            conn.execute(text(
                "ALTER TABLE candidatos ADD COLUMN status_reclutamiento VARCHAR(40) DEFAULT 'Aplicación recibida'"
            ))
            conn.execute(text(
                "UPDATE candidatos SET status_reclutamiento = 'Aplicación recibida' WHERE status_reclutamiento IS NULL"
            ))
        conn.execute(text("ALTER TABLE candidatos ALTER COLUMN vacante_id DROP NOT NULL"))

        # empresas: datos de facturación (RNC/comprobante fiscal)
        columnas_empresas = {c["name"] for c in inspector.get_columns("empresas")}
        if "tiene_rnc" not in columnas_empresas:
            conn.execute(text("ALTER TABLE empresas ADD COLUMN razon_social VARCHAR(200)"))
            conn.execute(text("ALTER TABLE empresas ADD COLUMN tiene_rnc BOOLEAN DEFAULT FALSE"))
            conn.execute(text("ALTER TABLE empresas ADD COLUMN rnc VARCHAR(30)"))

        # suscripciones: preferencia de renovación automática
        columnas_suscripciones = {c["name"] for c in inspector.get_columns("suscripciones")}
        if "renovacion_automatica" not in columnas_suscripciones:
            conn.execute(text("ALTER TABLE suscripciones ADD COLUMN renovacion_automatica BOOLEAN DEFAULT FALSE"))
