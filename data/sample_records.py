"""Datos de ejemplo en el formato crudo del sistema legacy.

Mantener los datos de muestra separados del código de negocio permite
reutilizarlos tanto desde el script de demo como desde los tests,
sin acoplar la lógica del dominio a un dataset particular.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ciudadanos.models import RawPersonRecord

SAMPLE_RECORDS: list[tuple[str, str, str, int]] = [
    ("11111111", "Pedro", "Paez", 24),
    ("22222222", "Ana", "Gomez", 31),
    ("33333333", "Luis", "Fernandez", 17),
    ("44444444", "Marta", "Diaz", 45),
    ("55555555", "Sofia", "Lopez", 25),
    ("66666666", "Diego", "Martinez", 62),
    ("77777777", "Carla", "Suarez", 8),
]
