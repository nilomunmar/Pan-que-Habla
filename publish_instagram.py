"""
Publica una imagen como Story en Instagram usando la
"Instagram API with Instagram Login" (graph.instagram.com),
que no requiere Página de Facebook vinculada.

Variables de entorno requeridas:
    IG_ACCESS_TOKEN  -> access token de larga duración
    IG_USER_ID       -> tu Instagram User ID (numérico)
    STORY_IMAGE_URL  -> URL pública de la imagen ya generada

Uso:
    python publish_instagram.py
"""
import os
import sys
import time

import requests

GRAPH_BASE = "https://graph.instagram.com/v22.0"


def create_media_container(ig_user_id: str, image_url: str, token: str) -> str:
    resp = requests.post(
        f"{GRAPH_BASE}/{ig_user_id}/media",
        data={
            "media_type": "STORIES",
            "image_url": image_url,
            "access_token": token,
        },
        timeout=30,
    )
    if not resp.ok:
        print(f"Respuesta de error completa de Meta: {resp.text}")
    resp.raise_for_status()
    data = resp.json()
    if "id" not in data:
        raise RuntimeError(f"Respuesta inesperada al crear el contenedor: {data}")
    return data["id"]


def wait_until_ready(container_id: str, token: str, timeout_s: int = 120) -> None:
    """Espera a que el contenedor pase a estado FINISHED antes de publicar."""
    elapsed = 0
    interval = 5
    while elapsed < timeout_s:
        resp = requests.get(
            f"{GRAPH_BASE}/{container_id}",
            params={"fields": "status_code", "access_token": token},
            timeout=30,
        )
        resp.raise_for_status()
        status = resp.json().get("status_code")
        print(f"Estado del contenedor: {status}")
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError("El contenedor de media falló al procesarse (status ERROR)")
        if status == "EXPIRED":
            raise RuntimeError("El contenedor expiró (más de 24h sin publicar)")
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError("Se agotó el tiempo esperando a que el contenedor esté listo")


def publish_media(ig_user_id: str, container_id: str, token: str) -> str:
    resp = requests.post(
        f"{GRAPH_BASE}/{ig_user_id}/media_publish",
        data={
            "creation_id": container_id,
