"""
Decide si HOY toca publicar, según las reglas:
- Antes de DAILY_FROM_DATE: solo el día de la semana WEEKLY_WEEKDAY
- Desde DAILY_FROM_DATE (incluida) hasta TARGET_DATE (incluida): todos los días
- Después de TARGET_DATE: no se publica más (servicio terminado)

Se puede forzar la ejecución con --force (útil para pruebas manuales).
"""
import argparse
import sys
from datetime import date

from config import TARGET_DATE, DAILY_FROM_DATE, WEEKLY_WEEKDAY


def should_run_today(today: date) -> bool:
    if today > TARGET_DATE:
        return False
    if today >= DAILY_FROM_DATE:
        return True
    return today.weekday() == WEEKLY_WEEKDAY


def days_remaining(today: date) -> int:
    delta = (TARGET_DATE - today).days
    return max(delta, 0) if delta >= 0 else delta  # permite negativo si se pasó


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Ignora el calendario y fuerza la ejecución")
    args = parser.parse_args()

    today = date.today()
    run = args.force or should_run_today(today)
    n = days_remaining(today)

    print(f"Fecha: {today.isoformat()}")
    print(f"Días restantes (n): {n}")
    print(f"¿Toca publicar hoy?: {run}")

    # Salida para usar en GitHub Actions: escribe en $GITHUB_OUTPUT si existe
    import os
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"should_run={'true' if run else 'false'}\n")
            f.write(f"days_remaining={n}\n")

    # Código de salida: 0 si hay que publicar, 1 si no
    sys.exit(0 if run else 1)


if __name__ == "__main__":
    main()
