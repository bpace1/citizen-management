"""Entidad de dominio: RegistroPersonas.

Encapsula una colección de `Person` y expone las operaciones de
negocio pedidas: formateo, extremos de edad, segmentación por umbral,
promedio de edad y acceso eficiente por DNI.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from statistics import mean

from ciudadanos.exceptions import (
    DuplicateDNIError,
    EmptyRegistroError,
    PersonNotFoundError,
)
from ciudadanos.models import Person, RawPersonRecord

DEFAULT_AGE_THRESHOLD: int = 25


class RegistroPersonas:
    """Colección validada de personas con operaciones de consulta y métricas.

    Internamente mantiene, además de la tupla ordenada de personas, un
    índice `dict[dni, Person]` para que la consulta por DNI (requisito
    de "acceso eficiente") sea O(1) en lugar de recorrer la lista
    completa en cada consulta.
    """

    def __init__(self, personas: Iterable[Person]) -> None:
        """Construye el registro a partir de instancias de Person ya creadas.

        Se prefiere usar `RegistroPersonas.from_raw_data` cuando se
        parte de las tuplas crudas del sistema legacy; este
        constructor queda disponible para cuando ya se cuenta con
        objetos `Person` (por ejemplo, en tests).

        Raises:
            DuplicateDNIError: Si dos o más personas comparten el mismo DNI.
        """
        self._personas: tuple[Person, ...] = tuple(personas)
        self._index_by_dni: dict[str, Person] = {}

        for persona in self._personas:
            if persona.dni in self._index_by_dni:
                raise DuplicateDNIError(persona.dni)
            self._index_by_dni[persona.dni] = persona

    @classmethod
    def from_raw_data(cls, raw_data: Sequence[RawPersonRecord]) -> RegistroPersonas:
        """Crea un RegistroPersonas a partir de la lista de tuplas del sistema legacy.

        Args:
            raw_data: Secuencia de tuplas (DNI, Nombre, Apellido, Edad).

        Returns:
            Un RegistroPersonas con todos los registros validados.
        """
        personas = (Person.from_raw_record(record) for record in raw_data)
        return cls(personas)

    def __len__(self) -> int:
        return len(self._personas)

    def __iter__(self) -> Iterator[Person]:
        return iter(self._personas)

    def _ensure_not_empty(self) -> None:
        if not self._personas:
            raise EmptyRegistroError(
                "La operación no está definida para un registro vacío."
            )

    def to_dict(self) -> dict[str, tuple[str, str, int]]:
        """Formatea el registro como un diccionario.

        La clave es el DNI (valor único de cada persona) y el valor es
        una tupla (Nombre, Apellido, Edad) con el resto de los datos.

        Returns:
            Diccionario {dni: (nombre, apellido, edad)}.
        """
        return {persona.dni: persona.as_tuple() for persona in self._personas}

    def get_oldest(self) -> Person:
        """Devuelve la persona de mayor edad del registro.

        Raises:
            EmptyRegistroError: Si el registro no tiene personas.
        """
        self._ensure_not_empty()
        return max(self._personas, key=lambda persona: persona.age)

    def get_youngest(self) -> Person:
        """Devuelve la persona de menor edad del registro.

        Raises:
            EmptyRegistroError: Si el registro no tiene personas.
        """
        self._ensure_not_empty()
        return min(self._personas, key=lambda persona: persona.age)

    def segment_by_age(
        self, threshold: int = DEFAULT_AGE_THRESHOLD
    ) -> tuple[tuple[Person, ...], tuple[Person, ...]]:
        """Separa la población en dos grupos según un umbral de edad.

        Args:
            threshold: Edad de corte. Por defecto 25 años.

        Returns:
            Tupla (menores_al_umbral, mayores_o_iguales_al_umbral).
        """
        menores = []
        mayores_o_iguales = []
        for p in self._personas:
            if p.age < threshold:
                menores.append(p)
            else:
                mayores_o_iguales.append(p)
        return tuple(menores), tuple(mayores_o_iguales)

    def average_age(self) -> float:
        """Calcula el promedio de edad de todos los registros.

        Raises:
            EmptyRegistroError: Si el registro no tiene personas.
        """
        self._ensure_not_empty()
        return mean(persona.age for persona in self._personas)

    def get_age_by_dni(self, dni: str) -> int:
        """Consulta directamente la edad de una persona por su DNI en O(1).

        Args:
            dni: DNI de la persona a consultar.

        Raises:
            PersonNotFoundError: Si no existe ninguna persona con ese DNI.
        """
        try:
            return self._index_by_dni[dni].age
        except KeyError as exc:
            raise PersonNotFoundError(dni) from exc
