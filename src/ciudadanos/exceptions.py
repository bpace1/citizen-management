"""Excepciones de dominio para el paquete `ciudadanos`.

Se define una jerarquía propia en lugar de reutilizar excepciones
genéricas de Python (ValueError, KeyError, etc.) para que el código
cliente pueda capturar errores de negocio de forma explícita y
diferenciada de errores de programación.
"""

from __future__ import annotations


class CiudadanosError(Exception):
    """Excepción base de la que heredan todos los errores del dominio."""


class InvalidPersonDataError(CiudadanosError):
    """Se lanza cuando los datos de una Persona son inconsistentes.

    Por ejemplo: edad negativa o DNI vacío.
    """


class DuplicateDNIError(CiudadanosError):
    """Se lanza cuando se intenta registrar un DNI ya existente."""

    def __init__(self, dni: str) -> None:
        self.dni = dni
        super().__init__(f"El DNI '{dni}' ya se encuentra registrado.")


class PersonNotFoundError(CiudadanosError):
    """Se lanza cuando se consulta un DNI que no existe en el registro."""

    def __init__(self, dni: str) -> None:
        self.dni = dni
        super().__init__(f"No existe ninguna persona registrada con DNI '{dni}'.")


class EmptyRegistroError(CiudadanosError):
    """Se lanza al pedir una métrica (máximo, mínimo, promedio) sobre un
    registro vacío, donde esa métrica no está definida.
    """
