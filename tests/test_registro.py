"""Tests unitarios para ``ciudadanos.registro`` (clase ``RegistroPersonas``).

Cubre el ciclo completo: creación desde datos crudos, formateo, extremos de
edad, promedio, segmentación por umbral y acceso por DNI. También verifica el
comportamiento ante registros vacíos, DNIs duplicados y datos inválidos.
"""

from __future__ import annotations

import pytest

from ciudadanos.exceptions import (
    DuplicateDNIError,
    EmptyRegistroError,
    InvalidPersonDataError,
    PersonNotFoundError,
)
from ciudadanos.models import Person
from ciudadanos.registro import DEFAULT_AGE_THRESHOLD, RegistroPersonas


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


class TestRegistroCreacion:
    """Construcción del registro y validaciones de integridad."""

    def test_longitud_correcta(self, registro: RegistroPersonas) -> None:
        assert len(registro) == 5

    def test_es_iterable_de_persons(self, registro: RegistroPersonas) -> None:
        assert all(isinstance(p, Person) for p in registro)

    def test_dni_duplicado_lanza_error(self) -> None:
        data = [
            ("11111111", "Pedro", "Paez", 24),
            ("11111111", "Carlos", "Ruiz", 30),
        ]
        with pytest.raises(DuplicateDNIError):
            RegistroPersonas.from_raw_data(data)

    def test_datos_invalidos_lanzan_error(self) -> None:
        data = [("1234567", "Juan123", "Perez", 20)]
        with pytest.raises(InvalidPersonDataError):
            RegistroPersonas.from_raw_data(data)


class TestToDict:
    """Formateo del registro como diccionario."""

    def test_claves_son_dnis(self, registro: RegistroPersonas) -> None:
        assert set(registro.to_dict().keys()) == {
            "11111111", "22222222", "33333333", "44444444", "55555555"
        }

    def test_valores_son_tuplas_de_tres_elementos(self, registro: RegistroPersonas) -> None:
        for value in registro.to_dict().values():
            assert isinstance(value, tuple)
            assert len(value) == 3

    def test_entrada_concreta(self, registro: RegistroPersonas) -> None:
        assert registro.to_dict()["11111111"] == ("Pedro", "Paez", 24)


class TestExtremosDeEdad:
    """Persona de mayor y menor edad dentro del registro."""

    def test_mayor(self, registro: RegistroPersonas) -> None:
        oldest = registro.get_oldest()
        assert oldest.age == 45
        assert oldest.dni == "44444444"

    def test_menor(self, registro: RegistroPersonas) -> None:
        youngest = registro.get_youngest()
        assert youngest.age == 17
        assert youngest.dni == "33333333"

    def test_mayor_en_registro_vacio_lanza_error(self) -> None:
        with pytest.raises(EmptyRegistroError):
            RegistroPersonas(personas=[]).get_oldest()

    def test_menor_en_registro_vacio_lanza_error(self) -> None:
        with pytest.raises(EmptyRegistroError):
            RegistroPersonas(personas=[]).get_youngest()


class TestPromedioDeEdad:
    """Cálculo del promedio de edad."""

    def test_valor_correcto(self, registro: RegistroPersonas) -> None:
        # (24 + 31 + 17 + 45 + 25) / 5 = 28.4
        assert registro.average_age() == pytest.approx(28.4)

    def test_registro_vacio_lanza_error(self) -> None:
        with pytest.raises(EmptyRegistroError):
            RegistroPersonas(personas=[]).average_age()


class TestSegmentacionPorEdad:
    """División de la población en dos grupos según un umbral."""

    def test_umbral_por_defecto(self, registro: RegistroPersonas) -> None:
        menores, mayores = registro.segment_by_age()
        assert all(p.age < DEFAULT_AGE_THRESHOLD for p in menores)
        assert all(p.age >= DEFAULT_AGE_THRESHOLD for p in mayores)

    def test_umbral_personalizado(self, registro: RegistroPersonas) -> None:
        menores, mayores = registro.segment_by_age(threshold=30)
        assert all(p.age < 30 for p in menores)
        assert all(p.age >= 30 for p in mayores)

    def test_total_preservado(self, registro: RegistroPersonas) -> None:
        menores, mayores = registro.segment_by_age()
        assert len(menores) + len(mayores) == len(registro)


class TestAccesoPorDNI:
    """Consulta de edad por DNI en O(1)."""

    def test_dni_existente(self, registro: RegistroPersonas) -> None:
        assert registro.get_age_by_dni("11111111") == 24

    def test_dni_inexistente_lanza_error(self, registro: RegistroPersonas) -> None:
        with pytest.raises(PersonNotFoundError):
            registro.get_age_by_dni("00000000")
