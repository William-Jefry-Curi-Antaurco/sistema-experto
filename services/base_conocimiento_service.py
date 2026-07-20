from models import (
    CategoriaFalla,
    Sintoma,
    Diagnostico,
    Regla,
)


class BaseConocimientoService:
    @staticmethod
    def resumen() -> dict:
        return {
            "categorias_activas": CategoriaFalla.query.filter_by(estado=True).count(),
            "sintomas_activos": Sintoma.query.filter_by(estado=True).count(),
            "diagnosticos_activos": Diagnostico.query.filter_by(estado=True).count(),
            "reglas_activas": Regla.query.filter_by(estado=True).count(),
        }

    @staticmethod
    def obtener_regla(codigo: str) -> dict | None:
        regla = Regla.query.filter_by(codigo=codigo).first()
        return regla.to_dict(incluir_condiciones=True) if regla else None

    @staticmethod
    def listar_reglas() -> list[dict]:
        reglas = (
            Regla.query.filter_by(estado=True)
            .order_by(Regla.prioridad.desc(), Regla.codigo.asc())
            .all()
        )
        return [regla.to_dict(incluir_condiciones=True) for regla in reglas]
