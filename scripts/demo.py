"""Script de demostración del sistema de gestión de ciudadanos.

Ejecuta todas las operaciones disponibles en ``RegistroPersonas`` sobre
el dataset de muestra y muestra los resultados en consola de forma
legible.

Uso::

    python scripts/demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Permite ejecutar el script desde la raíz del proyecto sin instalar el paquete.
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT))

from ciudadanos import CiudadanosError, DEFAULT_AGE_THRESHOLD, RegistroPersonas
from data.sample_records import SAMPLE_RECORDS

SEPARATOR = "-" * 50


def main() -> None:
    """Punto de entrada principal del script de demostración."""
    print("=" * 50)
    print("  Sistema de Gestión de Ciudadanos — Demo")
    print("=" * 50)

    try:
        registro = RegistroPersonas.from_raw_data(SAMPLE_RECORDS)

        # ── 1. Formateo como diccionario ──────────────────────────────────────────
        print(f"\n{SEPARATOR}")
        print("1. Registro formateado (to_dict):")
        print(SEPARATOR)
        for dni, datos in registro.to_dict().items():
            print(f"  {dni}: {datos}")

        # ── 2. Extremos de edad ──────────────────────────────────────────────────
        print(f"\n{SEPARATOR}")
        print("2. Extremos de edad:")
        print(SEPARATOR)
        print(f"  Mayor:  {registro.get_oldest()}")
        print(f"  Menor:  {registro.get_youngest()}")

        # ── 3. Promedio de edad ───────────────────────────────────────────────────
        print(f"\n{SEPARATOR}")
        print("3. Promedio de edad:")
        print(SEPARATOR)
        promedio = registro.average_age()
        print(f"  Promedio: {promedio:.2f} años")

        # ── 4. Segmentación por umbral de edad ────────────────────────────────────
        print(f"\n{SEPARATOR}")
        print(f"4. Segmentación por umbral de edad ({DEFAULT_AGE_THRESHOLD} años):")
        print(SEPARATOR)
        menores, mayores = registro.segment_by_age()
        print(f"  Menores de {DEFAULT_AGE_THRESHOLD}:")
        for p in menores:
            print(f"    · {p}")
        print(f"  Mayores o iguales a {DEFAULT_AGE_THRESHOLD}:")
        for p in mayores:
            print(f"    · {p}")

        # ── 4b. Segmentación con umbral custom (18) ───────────────────────────────
        print(f"\n{SEPARATOR}")
        print("4b. Segmentación con umbral custom (18 años):")
        print(SEPARATOR)
        menores_18, mayores_18 = registro.segment_by_age(threshold=18)
        print("  Menores de 18:")
        for p in menores_18:
            print(f"    · {p}")
        print("  Mayores o iguales a 18:")
        for p in mayores_18:
            print(f"    · {p}")

        # ── 5. Acceso eficiente por DNI ───────────────────────────────────────────
        print(f"\n{SEPARATOR}")
        print("5. Consulta de edad por DNI:")
        print(SEPARATOR)
        dni_consulta = "22222222"
        edad = registro.get_age_by_dni(dni_consulta)
        print(f"  Edad de la persona con DNI {dni_consulta}: {edad} años")

    except CiudadanosError as exc:
        print(f"\n[ERROR] No se pudo procesar el registro: {exc}")
        return

    print(f"\n{'=' * 50}")
    print("  Fin de la demostración.")
    print("=" * 50)


if __name__ == "__main__":
    main()
