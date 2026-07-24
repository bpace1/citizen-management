"""Tests unitarios para ``ciudadanos.exceptions``.

Verifica la lógica interna de las excepciones de dominio:
atributos propios y formato del mensaje de error.
"""

from __future__ import annotations

from ciudadanos.exceptions import (
    DuplicateDNIError,
    EmptyRegistroError,
    PersonNotFoundError,
)


class TestDuplicateDNIError:
    def test_stores_dni_attribute(self) -> None:
        err = DuplicateDNIError("12345678")
        assert err.dni == "12345678"

    def test_message_contains_dni(self) -> None:
        err = DuplicateDNIError("12345678")
        assert "12345678" in str(err)

    def test_is_ciudadanos_error(self) -> None:
        from ciudadanos.exceptions import CiudadanosError

        assert isinstance(DuplicateDNIError("12345678"), CiudadanosError)


class TestPersonNotFoundError:
    def test_stores_dni_attribute(self) -> None:
        err = PersonNotFoundError("99999999")
        assert err.dni == "99999999"

    def test_message_contains_dni(self) -> None:
        err = PersonNotFoundError("99999999")
        assert "99999999" in str(err)

    def test_is_ciudadanos_error(self) -> None:
        from ciudadanos.exceptions import CiudadanosError

        assert isinstance(PersonNotFoundError("99999999"), CiudadanosError)


class TestEmptyRegistroError:
    def test_is_ciudadanos_error(self) -> None:
        from ciudadanos.exceptions import CiudadanosError

        assert isinstance(EmptyRegistroError("vacío"), CiudadanosError)

    def test_message_preserved(self) -> None:
        err = EmptyRegistroError("La operación no está definida para un registro vacío.")
        assert "vacío" in str(err)
