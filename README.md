# Bot de Historias de Instagram — "El pan que habla"

## Qué hace ahora mismo
- Calcula `n` = días restantes hasta `TARGET_DATE` (config.py).
- Genera una imagen 1080x1920 con un fondo (fijo o carrusel rotativo) y el
  texto superpuesto ("Quedan n días para la ponencia del pan que habla").
- `scheduler.py` decide si TOCA publicar hoy:
  - Antes del 1 de julio: solo el día de la semana indicado (por defecto lunes).
  - Desde el 1 de julio hasta la fecha objetivo: todos los días.
  - Después de la fecha objetivo: no se ejecuta más.
- El workflow de GitHub Actions (`.github/workflows/story.yml`) corre cada
  día, comprueba si toca, y si es así genera la imagen y la deja como
  artefacto descargable.

## Lo que falta (siguiente paso)
La publicación automática real en Instagram vía Graph API. Necesita:
1. Cuenta de Instagram tipo **Business o Creator**, vinculada a una Página de Facebook.
2. Una app en developers.facebook.com con permiso `instagram_content_publish`.
3. Un access token de larga duración guardado como GitHub Secret.
4. Subir `output/story.jpg` a una URL pública (la Graph API pide una URL, no un
   archivo local) — puede ser un bucket S3, Cloudflare R2, o incluso el propio
   repo en GitHub Pages / raw.githubusercontent.com.
5. Dos llamadas a la API: crear el contenedor de media y publicarlo.

## Uso local
```bash
pip install -r requirements.txt

# 1. Pon tus imágenes de fondo en assets/carousel/ (o assets/background.jpg si usas modo "fixed")
# 2. Pon una fuente .ttf en assets/font.ttf
# 3. Ajusta config.py: TARGET_DATE, DAILY_FROM_DATE, textos, estilo

python generate_story.py        # genera output/story.jpg
python scheduler.py --force     # prueba la lógica de "¿toca hoy?"
```

## Estructura
```
ig_bot/
├── config.py              # toda la configuración editable
├── scheduler.py           # lógica de "¿toca publicar hoy?"
├── generate_story.py      # genera la imagen final
├── requirements.txt
├── assets/
│   ├── background.jpg     # (modo fixed)
│   ├── carousel/          # (modo carousel) imágenes .jpg/.png
│   └── font.ttf
├── output/
│   ├── story.jpg           # imagen generada
│   └── state.json          # recuerda qué imagen del carrusel toca
└── .github/workflows/story.yml
```
