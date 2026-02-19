"""
helpers.py
Funciones de utilidad y helpers para la aplicacion.
Aqui se pueden poner funciones que se reutilicen en varios modulos, como:
- Validaciones comunes
- Formateos
- Transformaciones de datos
- Generacion de codigos o identificadores
"""
from typing import Any

def check_not_none(value: Any, name: str) -> None:
    """
    Verifica que un valor no sea None.
    Lanza un ValueError si el valor es None.
    """
    if value is None:
        raise ValueError(f"El valor de '{name}' no puede ser None")

def format_decimal(value: float | None, precision: int = 2) -> float | None:
    """
    Formatea un numero decimal a la cantidad de decimales deseada.
    Retorna None si el valor es None.
    """
    if value is None:
        return None
    return round(value, precision)

def generate_slug(text: str) -> str:
    """
    Genera un slug amigable para URLs a partir de un texto.
    Convierte a minusculas y reemplaza espacios por guiones.
    """
    return text.lower().replace(" ", "-")