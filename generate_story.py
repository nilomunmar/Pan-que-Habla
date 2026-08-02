"""
Genera la imagen de la Historia de Instagram:
- Carga el fondo (fijo o siguiente del carrusel)
- Calcula n días restantes
- Escribe el texto centrado, ajustado a varias líneas si hace falta
- Guarda el resultado en OUTPUT_PATH
"""
import json
import os
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import config
from scheduler import days_remaining


def load_state() -> dict:
    if os.path.exists(config.STATE_FILE):
        with open(config.STATE_FILE, "r") as f:
            return json.load(f)
    return {"carousel_index": -1}


def save_state(state: dict) -> None:
    Path(config.STATE_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(config.STATE_FILE, "w") as f:
        json.dump(state, f)


def pick_background() -> Image.Image:
    if config.BACKGROUND_MODE == "fixed":
        return Image.open(config.FIXED_BACKGROUND_PATH).convert("RGBA")

    # modo carrusel: rota secuencialmente por los archivos ordenados alfabéticamente
    valid_ext = (".jpg", ".jpeg", ".png")
    files = sorted(
        f for f in os.listdir(config.CAROUSEL_DIR) if f.lower().endswith(valid_ext)
    )
    if not files:
        raise FileNotFoundError(
            f"No hay imágenes en {config.CAROUSEL_DIR} para el modo carrusel"
        )

    state = load_state()
    next_index = (state.get("carousel_index", -1) + 1) % len(files)
    state["carousel_index"] = next_index
    save_state(state)

    chosen = files[next_index]
    return Image.open(os.path.join(config.CAROUSEL_DIR, chosen)).convert("RGBA")


def fit_background(img: Image.Image) -> Image.Image:
    """Recorta y escala el fondo para llenar exactamente CANVAS_SIZE (estilo 'cover')."""
    target_w, target_h = config.CANVAS_SIZE
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h

    if src_ratio > target_ratio:
        # imagen más ancha de lo necesario: recorta a los lados
        new_h = target_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)

    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), trial, font=font, stroke_width=config.STROKE_WIDTH)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text(img: Image.Image, text: str) -> Image.Image:
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(config.FONT_PATH, config.FONT_SIZE)
    max_width = config.CANVAS_SIZE[0] - 2 * config.TEXT_MARGIN_X

    lines = wrap_text(draw, text, font, max_width)

    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=config.STROKE_WIDTH)
        line_heights.append(bbox[3] - bbox[1])
    line_spacing = 20
    total_h = sum(line_heights) + line_spacing * (len(lines) - 1)

    canvas_w, canvas_h = config.CANVAS_SIZE
    if config.TEXT_POSITION == "top":
        y = int(canvas_h * 0.12)
    elif config.TEXT_POSITION == "bottom":
        y = canvas_h - int(canvas_h * 0.12) - total_h
    else:  # center
        y = (canvas_h - total_h) // 2

    for line, h in zip(lines, line_heights):
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=config.STROKE_WIDTH)
        w = bbox[2] - bbox[0]
        x = (canvas_w - w) // 2
        draw.text(
            (x, y),
            line,
            font=font,
            fill=config.TEXT_COLOR,
            stroke_width=config.STROKE_WIDTH,
            stroke_fill=config.STROKE_COLOR,
        )
        y += h + line_spacing

    return img


def generate(today: date = None) -> str:
    today = today or date.today()
    n = days_remaining(today)
    text = config.build_text(n)

    bg = pick_background()
    bg = fit_background(bg)
    final_img = draw_text(bg, text)

    Path(config.OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    final_img.convert("RGB").save(config.OUTPUT_PATH, quality=95)
    print(f"Imagen generada: {config.OUTPUT_PATH}")
    print(f"Texto: {text}")
    return config.OUTPUT_PATH


if __name__ == "__main__":
    generate()
