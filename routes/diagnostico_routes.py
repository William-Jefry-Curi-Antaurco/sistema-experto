from flask import Blueprint, jsonify
import traceback

from models import Consulta
from services.diagnostico_service import DiagnosticoService
from services.motor_inferencia import MotorInferenciaService


diagnostico_bp = Blueprint(
    "diagnosticos",
    __name__,
    url_prefix="/api/diagnosticos",
)


@diagnostico_bp.post(
    "/consultas/<int:id_consulta>/evaluar"
)
def evaluar_consulta(id_consulta):
    try:
        motor = MotorInferenciaService(
            umbral_activacion=50.0,
            max_resultados=5,
        )

        resultado = motor.evaluar_consulta(
            id_consulta=id_consulta
        )

        print(
            "TIPO DEL RESULTADO:",
            type(resultado).__name__,
            flush=True,
        )

        print(
            "CONTENIDO DEL RESULTADO:",
            repr(resultado),
            flush=True,
        )

        if resultado is None:
            return jsonify({
                "estado": "error",
                "mensaje": (
                    "El motor de inferencia terminó, "
                    "pero no devolvió ningún resultado."
                ),
                "datos": None,
            }), 500

        return jsonify({
            "estado": "correcto",
            "mensaje": "Consulta evaluada correctamente",
            "datos": resultado,
        }), 200

    except ValueError as error:
        return jsonify({
            "estado": "error",
            "mensaje": str(error),
        }), 422

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "estado": "error",
            "mensaje": "No se pudo evaluar la consulta",
            "detalle": str(error),
            "tipo_error": type(error).__name__,
        }), 500


@diagnostico_bp.get(
    "/consultas/<int:id_consulta>/resultados"
)
def obtener_resultados(id_consulta):
    consulta = Consulta.query.get(id_consulta)

    if consulta is None:
        return jsonify({
            "estado": "error",
            "mensaje": "La consulta no existe",
        }), 404

    try:
        resultados = DiagnosticoService.obtener_resultados(
            id_consulta
        )

        return jsonify({
            "estado": "correcto",
            "cantidad": len(resultados),
            "datos": resultados,
        }), 200

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "estado": "error",
            "mensaje": (
                "No se pudieron obtener los resultados"
            ),
            "detalle": str(error),
        }), 500


@diagnostico_bp.get(
    "/consultas/<int:id_consulta>/principal"
)
def obtener_principal(id_consulta):
    consulta = Consulta.query.get(id_consulta)

    if consulta is None:
        return jsonify({
            "estado": "error",
            "mensaje": "La consulta no existe",
        }), 404

    try:
        resultado = DiagnosticoService.obtener_principal(
            id_consulta
        )

        if resultado is None:
            return jsonify({
                "estado": "error",
                "mensaje": (
                    "La consulta todavía no tiene un diagnóstico. "
                    "Ninguna regla produjo un resultado principal."
                ),
            }), 404

        return jsonify({
            "estado": "correcto",
            "datos": resultado,
        }), 200

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "estado": "error",
            "mensaje": (
                "No se pudo obtener el diagnóstico principal"
            ),
            "detalle": str(error),
        }), 500