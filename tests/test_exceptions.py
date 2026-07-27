"""Tests unitarios para ``ciudadanos.exceptions``.

Verifica la jerarquía de herencia, los atributos propios de cada excepción
y el formato del mensaje de error.
"""

from __future__ import annotations

from ciudadanos.exceptions import (
    CiudadanosError,
    DuplicateDNIError,
    EmptyRegistroError,
    InvalidPersonDataError,
    PersonNotFoundError,
)


class TestJerarquia:
    """Todas las excepciones del dominio heredan de ``CiudadanosError``."""

    def test_duplicate_dni_es_ciudadanos_error(self) -> None:
        assert isinstance(DuplicateDNIError("12345678"), CiudadanosError)

    def test_person_not_found_es_ciudadanos_error(self) -> None:
        assert isinstance(PersonNotFoundError("99999999"), CiudadanosError)

    def test_empty_registro_es_ciudadanos_error(self) -> None:
        assert isinstance(EmptyRegistroError("vacío"), CiudadanosError)

    def test_invalid_person_data_es_ciudadanos_error(self) -> None:
        assert isinstance(InvalidPersonDataError("dato inválido"), CiudadanosError)


class TestDuplicateDNIError:
    """``DuplicateDNIError``: almacena el DNI y lo expone en el mensaje."""

    def test_atributo_dni(self) -> None:
        err = DuplicateDNIError("12345678")
        assert err.dni == "12345678"

    def test_mensaje_contiene_dni(self) -> None:
        err = DuplicateDNIError("12345678")
        assert "12345678" in str(err)


class TestPersonNotFoundError:
    """``PersonNotFoundError``: almacena el DNI y lo expone en el mensaje."""

    def test_atributo_dni(self) -> None:
        err = PersonNotFoundError("99999999")
        assert err.dni == "99999999"

    def test_mensaje_contiene_dni(self) -> None:
        err = PersonNotFoundError("99999999")
        assert "99999999" in str(err)


class TestEmptyRegistroError:
    """``EmptyRegistroError``: preserva el mensaje de texto libre."""

    def test_mensaje_preservado(self) -> None:
        err = EmptyRegistroError("La operación no está definida para un registro vacío.")
        assert "vacío" in str(err)
