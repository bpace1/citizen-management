"""Tests unitarios para ``ciudadanos.models`` (clase ``Person``).

Cubre la creación exitosa de instancias, la inmutabilidad garantizada por el
dataclass ``frozen=True``, las validaciones de cada campo y el constructor
alternativo ``from_raw_record``.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ciudadanos.exceptions import InvalidPersonDataError
from ciudadanos.models import MAX_AGE, Person


class TestPersonCreacion:
    """Camino feliz: instancias válidas y métodos auxiliares."""

    def test_persona_completa(self) -> None:
        person = Person(dni="11111111", nombre="Pedro", apellido="Paez", age=24)
        assert person.dni == "11111111"
        assert person.nombre == "Pedro"
        assert person.apellido == "Paez"
        assert person.age == 24

    def test_edad_cero_es_valida(self) -> None:
        person = Person(dni="00000000", nombre="Bebe", apellido="Nuevo", age=0)
        assert person.age == 0

    def test_caracteres_especiales_validos(self) -> None:
        """Tildes, ñ, guiones y apóstrofes deben ser aceptados."""
        person = Person(dni="1234567", nombre="María José", apellido="O'Connor", age=20)
        assert person.nombre == "María José"
        assert person.apellido == "O'Connor"

    def test_as_tuple(self) -> None:
        person = Person(dni="12345678", nombre="Luis", apellido="Fernandez", age=17)
        assert person.as_tuple() == ("Luis", "Fernandez", 17)

    def test_str_contiene_datos_clave(self) -> None:
        person = Person(dni="11111111", nombre="Pedro", apellido="Paez", age=24)
        assert "Pedro" in str(person)
        assert "Paez" in str(person)
        assert "11111111" in str(person)


class TestPersonInmutabilidad:
    """``Person`` es un dataclass frozen: ningún campo puede modificarse."""

    def test_no_se_puede_modificar_dni(self) -> None:
        person = Person(dni="11111111", nombre="Pedro", apellido="Paez", age=24)
        with pytest.raises(FrozenInstanceError):
            person.dni = "99999999"  # type: ignore[misc]

    def test_no_se_puede_modificar_edad(self) -> None:
        person = Person(dni="11111111", nombre="Pedro", apellido="Paez", age=24)
        with pytest.raises(FrozenInstanceError):
            person.age = 99  # type: ignore[misc]


class TestPersonValidacionDNI:
    """Validaciones del campo ``dni``."""

    def test_tipo_invalido_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="DNI debe ser texto"):
            Person(dni=12345678, nombre="Juan", apellido="Perez", age=20)  # type: ignore[arg-type]

    def test_vacio_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError):
            Person(dni="", nombre="Pedro", apellido="Paez", age=24)

    def test_solo_espacios_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError):
            Person(dni="   ", nombre="Pedro", apellido="Paez", age=24)

    def test_espacios_internos_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="contener solo números"):
            Person(dni="123 4567", nombre="Juan", apellido="Perez", age=20)

    def test_espacios_extremos_se_normalizan(self) -> None:
        """El DNI con espacios en los bordes debe aceptarse y quedar limpio."""
        person = Person(dni=" 1234567 ", nombre="Juan", apellido="Perez", age=20)
        assert person.dni == "1234567"


class TestPersonValidacionNombre:
    """Validaciones del campo ``nombre``."""

    def test_tipo_invalido_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="nombre debe ser texto"):
            Person(dni="1234567", nombre=123, apellido="Perez", age=20)  # type: ignore[arg-type]

    def test_vacio_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="nombre no puede estar vacío"):
            Person(dni="1234567", nombre="", apellido="Perez", age=20)

    def test_solo_espacios_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="nombre no puede estar vacío"):
            Person(dni="1234567", nombre="   ", apellido="Perez", age=20)

    def test_caracteres_invalidos_lanzan_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="caracteres no permitidos"):
            Person(dni="1234567", nombre="Juan123", apellido="Perez", age=20)


class TestPersonValidacionApellido:
    """Validaciones del campo ``apellido``."""

    def test_tipo_invalido_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="apellido debe ser texto"):
            Person(dni="1234567", nombre="Juan", apellido=456, age=20)  # type: ignore[arg-type]

    def test_vacio_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="apellido no puede estar vacío"):
            Person(dni="1234567", nombre="Juan", apellido="", age=20)

    def test_solo_espacios_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="apellido no puede estar vacío"):
            Person(dni="1234567", nombre="Juan", apellido="   ", age=20)

    def test_caracteres_invalidos_lanzan_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="caracteres no permitidos"):
            Person(dni="1234567", nombre="Juan", apellido="Perez@", age=20)


class TestPersonValidacionEdad:
    """Validaciones del campo ``age``."""

    def test_tipo_invalido_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="entero no negativo"):
            Person(dni="1234567", nombre="Juan", apellido="Perez", age="veinte")  # type: ignore[arg-type]

    def test_negativa_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError):
            Person(dni="11111111", nombre="Pedro", apellido="Paez", age=-1)

    def test_supera_maximo_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="excede el máximo permitido"):
            Person(dni="1234567", nombre="Juan", apellido="Perez", age=MAX_AGE + 1)


class TestPersonFromRawRecord:
    """Constructor alternativo ``from_raw_record``."""

    def test_tupla_valida(self) -> None:
        person = Person.from_raw_record(("99999999", "Ana", "Gomez", 31))
        assert person.dni == "99999999"
        assert person.nombre == "Ana"
        assert person.apellido == "Gomez"
        assert person.age == 31

    def test_tupla_incompleta_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="tupla de 4 elementos"):
            Person.from_raw_record(("1234567", "Juan", "Perez"))  # type: ignore[arg-type]

    def test_no_tupla_lanza_error(self) -> None:
        with pytest.raises(InvalidPersonDataError, match="tupla de 4 elementos"):
            Person.from_raw_record("1234567 Juan Perez 20")  # type: ignore[arg-type]
