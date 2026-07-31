"""
migraciones.py - Ajustes de esquema que Base.metadata.create_all() no cubre:
columnas nuevas en tablas que ya existían en una instalación anterior.

Se ejecuta una vez al arrancar la API, después de create_all(). Es seguro
correrlo repetidas veces: cada columna se agrega solo si no existe todavía.

Genérico a propósito: en vez de listar a mano cada columna nueva (fácil de
olvidar una, como pasó con vacantes.empresa_id), compara cada tabla que YA
existe en la base de datos contra las columnas que el modelo actual espera,
y agrega las que falten. Las tablas completamente nuevas (usuarios, empresas,
suscripciones, compatibilidad_candidatos, etc.) no necesitan nada aquí:
create_all() ya las crea completas.

Solo actúa sobre Postgres (producción) — en SQLite local el esquema ya se
gestiona a mano durante el desarrollo.
"""

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from models import Base


def aplicar_migraciones(engine: Engine) -> None:
    if engine.dialect.name != "postgresql":
        return

    inspector = inspect(engine)

    with engine.begin() as conn:
        for nombre_tabla, tabla in Base.metadata.tables.items():
            if not inspector.has_table(nombre_tabla):
                continue  # tabla nueva; create_all() ya la creó completa

            columnas_existentes = {c["name"] for c in inspector.get_columns(nombre_tabla)}

            for columna in tabla.columns:
                if columna.name in columnas_existentes:
                    continue

                tipo_sql = columna.type.compile(dialect=engine.dialect)
                default_sql = ""
                if columna.default is not None and getattr(columna.default, "is_scalar", False):
                    valor = columna.default.arg
                    if isinstance(valor, bool):
                        default_sql = f" DEFAULT {str(valor).upper()}"
                    elif isinstance(valor, (int, float)):
                        default_sql = f" DEFAULT {valor}"
                    elif isinstance(valor, str):
                        escapado = valor.replace("'", "''")
                        default_sql = f" DEFAULT '{escapado}'"

                # Siempre nullable a nivel de base de datos, aunque el modelo
                # diga lo contrario: no se puede agregar una columna NOT NULL
                # sin valor a una tabla que ya tiene filas. La aplicación es
                # la que garantiza que las filas nuevas la llenen.
                conn.execute(text(
                    f'ALTER TABLE {nombre_tabla} ADD COLUMN "{columna.name}" {tipo_sql}{default_sql}'
                ))

        # candidatos.vacante_id pasa a ser opcional (bolsa de talento). Esto
        # es un ALTER COLUMN, no un ADD COLUMN, así que el loop de arriba no
        # lo cubre. Repetirlo no da error aunque ya esté aplicado.
        if inspector.has_table("candidatos"):
            conn.execute(text("ALTER TABLE candidatos ALTER COLUMN vacante_id DROP NOT NULL"))
