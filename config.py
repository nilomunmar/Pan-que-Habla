"""
Configuración del bot de Historias de Instagram.
Edita SOLO este archivo para ajustar fechas, textos y estilos.
"""
from datetime import date

# ------------------------------------------------------------------
# 1. FECHA OBJETIVO (el día de la ponencia del pan que habla)
#    Formato: date(AÑO, MES, DIA)
# ------------------------------------------------------------------
TARGET_DATE = date(2027, 7, 22)  # <-- CAMBIA ESTO por la fecha real

# ------------------------------------------------------------------
# 2. FECHA DE CAMBIO DE FRECUENCIA (semanal -> diario)
# ------------------------------------------------------------------
DAILY_FROM_DATE = date(2027, 7, 1)

# Día de la semana en el que se publica mientras es "semanal".
# 0 = lunes ... 6 = domingo
WEEKLY_WEEKDAY = 0  # lunes

# ------------------------------------------------------------------
# 3. TEXTOS
# ------------------------------------------------------------------
def build_text(n: int) -> str:
    if n > 1:
        return f"¡ Tan sólo quedan {n} días para la ponencia del Pan que Habla!"
    elif n == 1:
        return "¡Queda 1 sólo día para la ponencia del pan que habla! Muchas vidas canbiarán mañana..."
    elif n == 0:
        return "¡HOY ES LA PONENCIA DEL PAN QUE HABLA! ¿ESTÁIS PREPARADOS PARA EL MAYOR EVENTO DE VUESTRAS VIDAS?"
    else:
        return "La ponencia del pan que habla ya ha terminado. ¡Nos vemos el año que viene!"

# ------------------------------------------------------------------
# 4. FONDO: 'fixed' (una sola imagen) o 'carousel' (rota entre varias)
# ------------------------------------------------------------------
BACKGROUND_MODE = "fixed"  # "fixed" | "carousel"

# Usado si BACKGROUND_MODE == "fixed"
FIXED_BACKGROUND_PATH = "assets/background.jpg"

# Usado si BACKGROUND_MODE == "carousel"
# Se recorren en orden y se rota según el número de publicación
# (no aleatorio, para que no se repita la misma dos veces seguidas)
CAROUSEL_DIR = "assets/carousel"

# ------------------------------------------------------------------
# 5. ESTILO DEL TEXTO
# ------------------------------------------------------------------
FONT_PATH = "assets/font.ttf"       # ruta a una fuente .ttf/.otf
FONT_SIZE = 90
TEXT_COLOR = (255, 255, 255, 255)   # blanco
STROKE_COLOR = (0, 0, 0, 255)       # contorno negro para legibilidad
STROKE_WIDTH = 4
TEXT_MARGIN_X = 80                  # margen horizontal para el ajuste de línea
TEXT_POSITION = "center"            # "center" | "bottom" | "top"

# Tamaño estándar de Historia de Instagram
CANVAS_SIZE = (1080, 1920)

# ------------------------------------------------------------------
# 6. SALIDA
# ------------------------------------------------------------------
OUTPUT_PATH = "output/story.jpg"
STATE_FILE = "output/state.json"    # guarda el índice del carrusel entre ejecuciones
