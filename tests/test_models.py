"""Tests unitarios para ``ciudadanos.models`` (clase ``Person``).

Cubre la creación exitosa de instancias, las validaciones de datos y la
inmutabilidad garantizada por el dataclass ``frozen=True``.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ciudadanos.models import Person


class TestPersonCreation:
    """Creación correcta de instancias de ``Person``."""

    def test_create_valid_person(self) -> None:
        person = Person(dni="11111111", nombre="Pedro", apellido="Paez", age=24)
        assert person.dni == "11111111"
        assert person.nombre == "Pedro"
        assert person.apellido == "Paez"
        assert person.age == 24

    def test_create_person_age_zero(self) -> None:
        """Edad 0 es válida (recién nacido)."""
        person = Person(dni="00000000", nombre="Bebe", apellido="Nuevo", age=0)
        assert person.age == 0

    def test_from_raw_record(self) -> None:
        raw = ("99999999", "Ana", "Gomez", 31)
        person = Person.from_raw_record(raw)
        assert person.dni == "99999999"
        assert person.nombre == "Ana"
        assert person.apellido == "Gomez"
        assert person.age == 31

    def test_as_tuple(self) -> None:
        person = Person(dni="12345678", nombre="Luis", apellido="Fernandez", age=17)
        assert person.as_tuple() == ("Luis", "Fernandez", 17)

    def test_str_representation(self) -> None:
        person = Person(dni="11111111", nombre="Pedro", apellido="Paez", age=24)
        assert "Pedro" in str(person)
        assert "Paez" in str(person)
        assert "11111111" in str(person)


class TestPersonImmutability:
    """``Person`` debe ser inmutable (frozen dataclass)."""

    def test_cannot_modify_dni(self) -> None:
        person = Person(dni="11111111", nombre="Pedro", apellido="Paez", age=24)
        with pytest.raises(FrozenInstanceError):
            person.dni = "99999999"  # type: ignore[misc]

    def test_cannot_modify_age(self) -> None:
        person = Person(dni="11111111", nombre="Pedro", apellido="Paez", age=24)
        with pytest.raises(FrozenInstanceError):
            person.age = 99  # type: ignore[misc]


class TestPersonValidation:
    """Validaciones de coherencia de datos al crear una ``Person``."""

    def test_negative_age_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError):
            Person(dni="11111111", nombre="Pedro", apellido="Paez", age=-1)

    def test_empty_dni_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError):
            Person(dni="", nombre="Pedro", apellido="Paez", age=24)

    def test_blank_dni_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError):
            Person(dni="   ", nombre="Pedro", apellido="Paez", age=24)


class TestPersonValidationExtended:
    """Validaciones adicionales: nombre, apellido, tipos, normalización."""

    def test_name_empty_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError, match="nombre no puede estar vacío"):
            Person(dni="1234567", nombre="", apellido="Perez", age=20)

    def test_name_only_spaces_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError, match="nombre no puede estar vacío"):
            Person(dni="1234567", nombre="   ", apellido="Perez", age=20)

    def test_name_invalid_characters_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError, match="caracteres no permitidos"):
            Person(dni="1234567", nombre="Juan123", apellido="Perez", age=20)

    def test_name_with_valid_special_chars(self) -> None:
        # Letras con tilde, ñ, guiones, apóstrofes, espacios
        person = Person(dni="1234567", nombre="María José", apellido="O'Connor", age=20)
        assert person.nombre == "María José"
        assert person.apellido == "O'Connor"

    def test_apellido_empty_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(
            InvalidPersonDataError, match="apellido no puede estar vacío"
        ):
            Person(dni="1234567", nombre="Juan", apellido="", age=20)

    def test_apellido_only_spaces_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(
            InvalidPersonDataError, match="apellido no puede estar vacío"
        ):
            Person(dni="1234567", nombre="Juan", apellido="   ", age=20)

    def test_apellido_invalid_characters_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError, match="caracteres no permitidos"):
            Person(dni="1234567", nombre="Juan", apellido="Perez@", age=20)

    def test_age_not_int_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError, match="entero no negativo"):
            Person(dni="1234567", nombre="Juan", apellido="Perez", age="veinte")  # type: ignore

    def test_dni_with_spaces_normalized(self) -> None:
        # Verifica que se recorta y se acepta
        person = Person(dni=" 1234567 ", nombre="Juan", apellido="Perez", age=20)
        assert person.dni == "1234567"

    def test_dni_with_internal_spaces_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError, match="contener solo números"):
            Person(dni="123 4567", nombre="Juan", apellido="Perez", age=20)

    def test_from_raw_record_invalid_tuple_length(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError, match="tupla de 4 elementos"):
            Person.from_raw_record(("1234567", "Juan", "Perez"))  # faltaría edad

    def test_from_raw_record_non_tuple_raises(self) -> None:
        from ciudadanos.exceptions import InvalidPersonDataError

        with pytest.raises(InvalidPersonDataError, match="tupla de 4 elementos"):
            Person.from_raw_record("1234567 Juan Perez 20")  # no es tupla
