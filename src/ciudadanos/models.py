"""
Modelos de dominio para el paquete ``ciudadanos``.

Define la estructura de datos ``Person`` (inmutable y auto-validada) y
el alias de tipo ``RawPersonRecord`` que describe el formato de entrada
proveniente del sistema legacy.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ciudadanos.exceptions import InvalidPersonDataError

# Alias del tipo de entrada crudo del sistema legacy: (DNI, Nombre, Apellido, Edad)
RawPersonRecord = tuple[str, str, str, int]

# Expresión regular para nombres/apellidos: letras, espacios, guiones, apóstrofes
_NAME_PATTERN = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-']+$")

# Edad máxima biológicamente razonable
MAX_AGE: int = 150


@dataclass(frozen=True, slots=True)
class Person:
    """Representa a una persona del padrón ciudadano.

    Es **inmutable** (``frozen=True``) y valida la coherencia de sus datos
    en el momento de la creación, garantizando que ninguna instancia pueda
    existir en un estado inválido.

    Attributes:
        dni: Documento Nacional de Identidad. Debe ser una cadena de 7 a 8 números.
        nombre: Nombre de pila de la persona (no vacío, solo caracteres válidos).
        apellido: Apellido de la persona (no vacío, solo caracteres válidos).
        age: Edad en años completos. No puede ser negativa.
    """

    dni: str
    nombre: str
    apellido: str
    age: int

    def __post_init__(self) -> None:
        """Valida la coherencia de los datos tras la inicialización."""
        # Normalización y validación de DNI
        if not isinstance(self.dni, str):
            raise InvalidPersonDataError(
                f"El DNI debe ser texto. Se recibió: {self.dni}."
            )
        dni_limpio = self.dni.strip()
        if not dni_limpio.isdigit() or not (7 <= len(dni_limpio) <= 8):
            raise InvalidPersonDataError(
                f"El DNI debe contener solo números y tener entre 7 y 8 caracteres. Se recibió: '{dni_limpio}'."
            )
        object.__setattr__(self, "dni", dni_limpio)

        # Validación de nombre
        if not isinstance(self.nombre, str):
            raise InvalidPersonDataError(
                f"El nombre debe ser texto. Se recibió: {self.nombre}."
            )
        nombre_limpio = self.nombre.strip()
        if nombre_limpio == "":
            raise InvalidPersonDataError("El nombre no puede estar vacío.")
        if not _NAME_PATTERN.match(nombre_limpio):
            raise InvalidPersonDataError(
                f"El nombre contiene caracteres no permitidos. Se recibió: '{nombre_limpio}'."
            )
        object.__setattr__(self, "nombre", nombre_limpio)

        # Validación de apellido
        if not isinstance(self.apellido, str):
            raise InvalidPersonDataError(
                f"El apellido debe ser texto. Se recibió: {self.apellido}."
            )
        apellido_limpio = self.apellido.strip()
        if apellido_limpio == "":
            raise InvalidPersonDataError("El apellido no puede estar vacío.")
        if not _NAME_PATTERN.match(apellido_limpio):
            raise InvalidPersonDataError(
                f"El apellido contiene caracteres no permitidos. Se recibió: '{apellido_limpio}'."
            )
        object.__setattr__(self, "apellido", apellido_limpio)

        # Validación de edad
        if not isinstance(self.age, int) or self.age < 0:
            raise InvalidPersonDataError(
                f"La edad debe ser un entero no negativo. Se recibió: {self.age}."
            )
        if self.age > MAX_AGE:
            raise InvalidPersonDataError(
                f"La edad {self.age} excede el máximo permitido ({MAX_AGE} años)."
            )

    @classmethod
    def from_raw_record(cls, record: RawPersonRecord) -> Person:
        """Construye una instancia a partir de una tupla cruda del sistema legacy.

        Args:
            record: Tupla con el formato ``(DNI, Nombre, Apellido, Edad)``.

        Returns:
            Una nueva instancia de ``Person`` con los datos validados.

        Raises:
            InvalidPersonDataError: Si la edad es negativa, el DNI está vacío o su formato es inválido,
                o si nombre/apellido están vacíos o tienen caracteres no permitidos.
        """
        if not isinstance(record, tuple) or len(record) != 4:
            raise InvalidPersonDataError(
                f"Se esperaba una tupla de 4 elementos (DNI, nombre, apellido, edad). Se recibió: {record}"
            )
        dni, nombre, apellido, age = record
        return cls(dni=dni, nombre=nombre, apellido=apellido, age=age)

    def as_tuple(self) -> tuple[str, str, int]:
        """Devuelve los campos no-clave como tupla ``(nombre, apellido, edad)``.

        Returns:
            Tupla con nombre, apellido y edad de la persona.
        """
        return (self.nombre, self.apellido, self.age)

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido} (DNI: {self.dni}, Edad: {self.age})"
