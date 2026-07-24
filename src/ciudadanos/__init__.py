"""Paquete `ciudadanos`: procesamiento de datos de ciudadanos.

Expone la API pública del dominio: modelos, entidad de registro y
excepciones.
"""

from ciudadanos.exceptions import (
    CiudadanosError,
    DuplicateDNIError,
    EmptyRegistroError,
    InvalidPersonDataError,
    PersonNotFoundError,
)
from ciudadanos.models import Person, RawPersonRecord
from ciudadanos.registro import DEFAULT_AGE_THRESHOLD, RegistroPersonas

__all__ = [
    "Person",
    "RawPersonRecord",
    "RegistroPersonas",
    "DEFAULT_AGE_THRESHOLD",
    "CiudadanosError",
    "InvalidPersonDataError",
    "DuplicateDNIError",
    "PersonNotFoundError",
    "EmptyRegistroError",
]
