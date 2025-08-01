#!/usr/bin/env python3
"""
Script para generar una clave JWT segura
Ejecutar: python generate_jwt_key.py
"""

import secrets
import string

def generate_jwt_secret(length=64):
    """Genera una clave JWT segura"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    secret = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret

if __name__ == "__main__":
    secret = generate_jwt_secret()
    print("=" * 60)
    print("CLAVE JWT GENERADA:")
    print("=" * 60)
    print(f"JWT_SECRET_KEY={secret}")
    print("=" * 60)
    print("Copia esta línea en tu archivo .env")
    print("¡NUNCA compartas esta clave!")
    print("=" * 60)
