"""
create_user.py - Crear cuentas de reclutador/empresa/owner

Solo la dueña de la plataforma ejecuta este script (no hay auto-registro).

Uso:
    python create_user.py --email juan@ejemplo.com --nombre "Juan Perez" --rol reclutador
    python create_user.py --email empresa@ejemplo.com --nombre "Constructora XYZ" --rol empresa --empresa "Constructora XYZ"
    python create_user.py --email keren@cenerhconsulting.com --nombre "Keren Mejia" --rol owner
"""

import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import argparse
import getpass

from database import SessionLocal, engine
from models import Base, Empresa, Usuario
from auth_users import hash_password

ROLES_VALIDOS = ("owner", "reclutador", "empresa")


def main():
    parser = argparse.ArgumentParser(description="Crear una cuenta de usuario para CENERH RECRUIT OS")
    parser.add_argument("--email", required=True)
    parser.add_argument("--nombre", required=True)
    parser.add_argument("--rol", required=True, choices=ROLES_VALIDOS)
    parser.add_argument("--empresa", help="Nombre de la empresa (requerido si --rol=empresa)")
    args = parser.parse_args()

    if args.rol == "empresa" and not args.empresa:
        parser.error("--empresa es requerido cuando --rol=empresa")

    password = getpass.getpass("Contraseña para la nueva cuenta: ")
    password_confirm = getpass.getpass("Confirma la contraseña: ")
    if password != password_confirm:
        print("❌ Las contraseñas no coinciden")
        sys.exit(1)
    if len(password) < 8:
        print("❌ La contraseña debe tener al menos 8 caracteres")
        sys.exit(1)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Usuario).filter_by(email=args.email).first():
            print(f"❌ Ya existe una cuenta con el email {args.email}")
            sys.exit(1)

        empresa_id = None
        if args.rol == "empresa":
            empresa = db.query(Empresa).filter_by(nombre=args.empresa).first()
            if not empresa:
                empresa = Empresa(nombre=args.empresa, contacto_email=args.email)
                db.add(empresa)
                db.flush()
            empresa_id = empresa.id

        usuario = Usuario(
            email=args.email,
            password_hash=hash_password(password),
            nombre=args.nombre,
            rol=args.rol,
            empresa_id=empresa_id,
        )
        db.add(usuario)
        db.commit()

        print(f"✅ Cuenta creada: {args.email} (rol={args.rol})")
    finally:
        db.close()


if __name__ == "__main__":
    main()
