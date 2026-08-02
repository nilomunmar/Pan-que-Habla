"""
Refresca un access token de Instagram de larga duración (válido ~60 días)
por otro nuevo de otros ~60 días. Hay que ejecutarlo periódicamente
(GitHub Actions se encarga, ver .github/workflows/refresh_token.yml)
ANTES de que el token actual caduque.

Variables de entorno requeridas:
    IG_ACCESS_TOKEN -> el token actual (aún válido)

Imprime el nuevo token; en el workflow se usa la CLI de GitHub para
actualizar el secret automáticamente.
"""
import os
import sys

import requests

GRAPH_BASE = "https://graph.instagram.com"


def refresh_token(current_token: str) -> str:
    resp = requests.get(
        f"{GRAPH_BASE}/refresh_access_token",
        params={
            "grant_type": "ig_refresh_token",
            "access_token": current_token,
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "access_token" not in data:
        raise RuntimeError(f"Respuesta inesperada al refrescar el token: {data}")
    return data["access_token"]


def main():
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        print("Falta la variable de entorno IG_ACCESS_TOKEN", file=sys.stderr)
        sys.exit(1)

    new_token = refresh_token(token)
    print(new_token)


if __name__ == "__main__":
    main()
