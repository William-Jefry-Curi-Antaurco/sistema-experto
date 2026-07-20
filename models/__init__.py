from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importaciones al final para evitar dependencias circulares.
from .categoria import CategoriaFalla
from .sintoma import Sintoma
from .diagnostico import Diagnostico
from .recomendacion import Recomendacion
from .regla import Regla, CondicionRegla
from .consulta import (
    Consulta,
    RespuestaConsulta,
    ReglaActivada,
    ResultadoDiagnostico,
)

__all__ = [
    "db",
    "CategoriaFalla",
    "Sintoma",
    "Diagnostico",
    "Recomendacion",
    "Regla",
    "CondicionRegla",
    "Consulta",
    "RespuestaConsulta",
    "ReglaActivada",
    "ResultadoDiagnostico",
]
