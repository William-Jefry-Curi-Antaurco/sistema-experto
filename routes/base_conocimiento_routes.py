from flask import Blueprint, jsonify

from services.base_conocimiento_service import BaseConocimientoService


base_conocimiento_bp = Blueprint(
    "base_conocimiento",
    __name__,
    url_prefix="/api/base-conocimiento"
)


@base_conocimiento_bp.get("/resumen")
def obtener_resumen():
    try:
        resumen = BaseConocimientoService.resumen()

        return jsonify({
            "estado": "correcto",
            "datos": resumen
        })

    except Exception as error:
        return jsonify({
            "estado": "error",
            "mensaje": "No se pudo obtener el resumen",
            "detalle": str(error)
        }), 500


@base_conocimiento_bp.get("/reglas")
def listar_reglas():
    try:
        reglas = BaseConocimientoService.listar_reglas()

        return jsonify({
            "estado": "correcto",
            "cantidad": len(reglas),
            "datos": reglas
        })

    except Exception as error:
        return jsonify({
            "estado": "error",
            "mensaje": "No se pudieron listar las reglas",
            "detalle": str(error)
        }), 500


@base_conocimiento_bp.get("/reglas/<string:codigo>")
def obtener_regla(codigo):
    try:
        regla = BaseConocimientoService.obtener_regla(
            codigo.upper()
        )

        if regla is None:
            return jsonify({
                "estado": "error",
                "mensaje": "La regla no existe"
            }), 404

        return jsonify({
            "estado": "correcto",
            "datos": regla
        })

    except Exception as error:
        return jsonify({
            "estado": "error",
            "mensaje": "No se pudo obtener la regla",
            "detalle": str(error)
        }), 500