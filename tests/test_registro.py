"""Tests unitarios para ``ciudadanos.registro`` (clase ``RegistroPersonas``).

Cubre el ciclo completo: creación desde datos crudos, formateo,
extremos de edad, segmentación, promedio y acceso por DNI.
También verifica el comportamiento ante registros vacíos y DNIs duplicados.
"""

from __future__ import annotations

import pytest

from ciudadanos.exceptions import (
    DuplicateDNIError,
    EmptyRegistroError,
    PersonNotFoundError,
    InvalidPersonDataError,
)
from ciudadanos.models import Person
from ciudadanos.registro import DEFAULT_AGE_THRESHOLD, RegistroPersonas

# Fixtures

RAW_DATA = [
    ("11111111", "Pedro", "Paez", 24),
    ("22222222", "Ana", "Gomez", 31),
    ("33333333", "Luis", "Fernandez", 17),
    ("44444444", "Marta", "Diaz", 45),
    ("55555555", "Sofia", "Lopez", 25),
]


@pytest.fixture()
def registro() -> RegistroPersonas:
    return RegistroPersonas.from_raw_data(RAW_DATA)


# Creación


class TestRegistroCreation:
    def test_from_raw_data_length(self, registro: RegistroPersonas) -> None:
        assert len(registro) == 5

    def test_duplicate_dni_raises(self) -> None:
        data = [
            ("11111111", "Pedro", "Paez", 24),
            ("11111111", "Carlos", "Ruiz", 30),
        ]
        with pytest.raises(DuplicateDNIError):
            RegistroPersonas.from_raw_data(data)

    def test_iterable(self, registro: RegistroPersonas) -> None:
        persons = list(registro)
        assert all(isinstance(p, Person) for p in persons)


# Formateo


class TestToDict:
    def test_keys_are_dnis(self, registro: RegistroPersonas) -> None:
        result = registro.to_dict()
        assert set(result.keys()) == {
            "11111111",
            "22222222",
            "33333333",
            "44444444",
            "55555555",
        }

    def test_values_are_tuples(self, registro: RegistroPersonas) -> None:
        result = registro.to_dict()
        for value in result.values():
            assert isinstance(value, tuple)
            assert len(value) == 3

    def test_specific_entry(self, registro: RegistroPersonas) -> None:
        result = registro.to_dict()
        assert result["11111111"] == ("Pedro", "Paez", 24)


# Extremos de edad


class TestAgeExtremes:
    def test_get_oldest(self, registro: RegistroPersonas) -> None:
        oldest = registro.get_oldest()
        assert oldest.age == 45
        assert oldest.dni == "44444444"

    def test_get_youngest(self, registro: RegistroPersonas) -> None:
        youngest = registro.get_youngest()
        assert youngest.age == 17
        assert youngest.dni == "33333333"

    def test_oldest_empty_raises(self) -> None:
        reg = RegistroPersonas(personas=[])
        with pytest.raises(EmptyRegistroError):
            reg.get_oldest()

    def test_youngest_empty_raises(self) -> None:
        reg = RegistroPersonas(personas=[])
        with pytest.raises(EmptyRegistroError):
            reg.get_youngest()


# Promedio


class TestAverageAge:
    def test_average_age(self, registro: RegistroPersonas) -> None:
        # (24 + 31 + 17 + 45 + 25) / 5 = 28.4
        assert registro.average_age() == pytest.approx(28.4)

    def test_average_empty_raises(self) -> None:
        reg = RegistroPersonas(personas=[])
        with pytest.raises(EmptyRegistroError):
            reg.average_age()


# Segmentación


class TestSegmentByAge:
    def test_default_threshold(self, registro: RegistroPersonas) -> None:
        menores, mayores = registro.segment_by_age()
        assert all(p.age < DEFAULT_AGE_THRESHOLD for p in menores)
        assert all(p.age >= DEFAULT_AGE_THRESHOLD for p in mayores)

    def test_custom_threshold(self, registro: RegistroPersonas) -> None:
        menores, mayores = registro.segment_by_age(threshold=30)
        assert all(p.age < 30 for p in menores)
        assert all(p.age >= 30 for p in mayores)

    def test_total_count_preserved(self, registro: RegistroPersonas) -> None:
        menores, mayores = registro.segment_by_age()
        assert len(menores) + len(mayores) == len(registro)


# Acceso por DNI


class TestGetAgeByDni:
    def test_existing_dni(self, registro: RegistroPersonas) -> None:
        assert registro.get_age_by_dni("11111111") == 24

    def test_nonexistent_dni_raises(self, registro: RegistroPersonas) -> None:
        with pytest.raises(PersonNotFoundError):
            registro.get_age_by_dni("00000000")


# Validación de datos crudos


class TestRawDataValidation:
    def test_from_raw_data_with_invalid_name_raises(self) -> None:
        data = [("1234567", "Juan123", "Perez", 20)]  # nombre inválido
        with pytest.raises(InvalidPersonDataError):
            RegistroPersonas.from_raw_data(data)
