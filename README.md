# Citizen Management 🏛️

Sistema de procesamiento y gestión de registros de ciudadanos, desarrollado como solución al desafío técnico de Adhoc.

---

## Estructura del proyecto

```
citizen-management/
├── data/
│   └── sample_records.py      # Dataset de muestra del sistema legacy
├── scripts/
│   └── demo.py                # Script de demostración interactiva
├── src/
│   └── ciudadanos/
│       ├── __init__.py        # API pública del paquete
│       ├── exceptions.py      # Jerarquía de excepciones de dominio
│       ├── models.py          # Modelo Person (inmutable y validado)
│       └── registro.py        # RegistroPersonas con todas las operaciones
├── tests/
│   ├── test_models.py         # Tests de Person
│   └── test_registro.py      # Tests de RegistroPersonas
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## Requisitos

- Python 3.11 o superior

---

## Instalación con entorno virtual (venv)

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPO>
cd citizen-management

# 2. Crear el entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# 4. Instalar el paquete en modo editable (incluye dependencias de desarrollo)
pip install -e ".[dev]"
```

---

## Ejecutar el script de demostración

Con el entorno virtual activo y desde la raíz del proyecto:

```bash
python scripts/demo.py
```

La salida mostrará todas las operaciones disponibles: formateo del registro, extremos de edad, promedio, segmentación por umbral y consulta por DNI.

---

## Ejecutar los tests

```bash
# Todos los tests
pytest

# Con reporte de cobertura en terminal
pytest --cov

# Con reporte de cobertura en HTML
pytest --cov --cov-report=html
# Abrir: htmlcov/index.html
```

---

## Formato de los datos de entrada

Los datos se reciben como una lista de tuplas con el esquema:

```python
(DNI: str, Nombre: str, Apellido: str, Edad: int)
```

Ejemplo:

```python
("11111111", "Pedro", "Paez", 24)
```

---

## Funcionalidades

| Método | Descripción |
|--------|-------------|
| `RegistroPersonas.from_raw_data(data)` | Crea el registro desde tuplas crudas |
| `registro.to_dict()` | `{dni: (nombre, apellido, edad)}` |
| `registro.get_oldest()` | Persona con mayor edad |
| `registro.get_youngest()` | Persona con menor edad |
| `registro.average_age()` | Promedio de edades |
| `registro.segment_by_age(threshold=25)` | Dos grupos: menores / mayores al umbral |
| `registro.get_age_by_dni(dni)` | Edad de una persona por DNI en O(1) |
