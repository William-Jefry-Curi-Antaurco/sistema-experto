import traceback

from flask import Blueprint, jsonify, request

from models import Consulta
from services.consulta_service import ConsultaService
from services.pregunta_service import PreguntaService


print(
    "CARGANDO ARCHIVO DE RUTAS:",
    __file__,
    flush=True,
)

consulta_bp = Blueprint(
    "consultas",
    __name__,
    url_prefix="/api/consultas",
)


@consulta_bp.post("")
def crear_consulta():
    datos = request.get_json(silent=True) or {}

    nombre_usuario = datos.get("nombre_usuario")
    descripcion_problema = datos.get("descripcion_problema")

    try:
        consulta = ConsultaService.crear_consulta(
            nombre_usuario=nombre_usuario,
            descripcion_problema=descripcion_problema,
        )

        return jsonify({
            "estado": "correcto",
            "mensaje": "Consulta creada correctamente",
            "datos": consulta.to_dict(),
        }), 201

    except ValueError as error:
        return jsonify({
            "estado": "error",
            "mensaje": str(error),
        }), 422

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "estado": "error",
            "mensaje": "No se pudo crear la consulta",
            "detalle": str(error),
            "tipo_error": type(error).__name__,
        }), 500


@consulta_bp.get("")
def listar_consultas():
    try:
        consultas = (
            Consulta.query
            .order_by(Consulta.fecha_inicio.desc())
            .all()
        )

        return jsonify({
            "estado": "correcto",
            "cantidad": len(consultas),
            "datos": [
                consulta.to_dict()
                for consulta in consultas
            ],
        })

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "estado": "error",
            "mensaje": "No se pudieron listar las consultas",
            "detalle": str(error),
            "tipo_error": type(error).__name__,
        }), 500


@consulta_bp.get("/<int:id_consulta>")
def obtener_consulta(id_consulta):
    consulta = Consulta.query.get(id_consulta)

    if consulta is None:
        return jsonify({
            "estado": "error",
            "mensaje": "La consulta no existe",
        }), 404

    return jsonify({
        "estado": "correcto",
        "datos": consulta.to_dict(
            incluir_detalle=True,
        ),
    })


@consulta_bp.post("/<int:id_consulta>/respuestas")
def guardar_respuesta(id_consulta):
    datos = request.get_json(silent=True) or {}

    id_sintoma = datos.get("id_sintoma")
    valor_respuesta = datos.get("valor_respuesta")

    print(
        "\n========== GUARDAR RESPUESTA ==========",
        flush=True,
    )
    print(
        "Consulta:",
        id_consulta,
        "Síntoma:",
        id_sintoma,
        "Valor:",
        valor_respuesta,
        flush=True,
    )

    if id_sintoma is None:
        return jsonify({
            "estado": "error",
            "mensaje": "El campo id_sintoma es obligatorio.",
        }), 422

    if valor_respuesta is None:
        return jsonify({
            "estado": "error",
            "mensaje": "El campo valor_respuesta es obligatorio.",
        }), 422

    try:
        id_sintoma = int(id_sintoma)
    except (TypeError, ValueError):
        return jsonify({
            "estado": "error",
            "mensaje": "El id_sintoma debe ser un número entero.",
        }), 422

    valor_respuesta = str(
        valor_respuesta
    ).strip().upper()

    if valor_respuesta not in {
        "SI",
        "NO",
        "NO_SE",
    }:
        return jsonify({
            "estado": "error",
            "mensaje": (
                "La respuesta debe ser SI, NO o NO_SE."
            ),
        }), 422

    try:
        respuesta = ConsultaService.guardar_respuesta(
            id_consulta=id_consulta,
            id_sintoma=id_sintoma,
            valor_respuesta=valor_respuesta,
        )

        print(
            "RESPUESTA GUARDADA:",
            respuesta.id_respuesta,
            respuesta.id_consulta,
            respuesta.id_sintoma,
            respuesta.valor_respuesta,
            flush=True,
        )

        return jsonify({
            "estado": "correcto",
            "mensaje": "Respuesta registrada correctamente.",
            "datos": respuesta.to_dict(),
        }), 200

    except ValueError as error:
        print(
            "ERROR DE VALIDACIÓN:",
            str(error),
            flush=True,
        )

        return jsonify({
            "estado": "error",
            "mensaje": str(error),
        }), 422

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "estado": "error",
            "mensaje": "No se pudo guardar la respuesta.",
            "detalle": str(error),
            "tipo_error": type(error).__name__,
        }), 500

@consulta_bp.get(
    "/<int:id_consulta>/siguiente-pregunta"
)
def siguiente_pregunta(id_consulta):
    id_categoria = request.args.get(
        "id_categoria",
        type=int,
    )

    try:
        pregunta = PreguntaService.siguiente_pregunta(
            id_consulta=id_consulta,
            id_categoria=id_categoria,
        )

        if pregunta is None:
            return jsonify({
                "estado": "correcto",
                "mensaje": (
                    "No quedan preguntas pendientes"
                ),
                "datos": None,
            })

        return jsonify({
            "estado": "correcto",
            "datos": pregunta.to_dict(),
        })

    except ValueError as error:
        return jsonify({
            "estado": "error",
            "mensaje": str(error),
        }), 404

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "estado": "error",
            "mensaje": (
                "No se pudo obtener "
                "la siguiente pregunta"
            ),
            "detalle": str(error),
            "tipo_error": type(error).__name__,
        }), 500


@consulta_bp.post(
    "/<int:id_consulta>/cancelar"
)
def cancelar_consulta(id_consulta):
    datos = request.get_json(silent=True) or {}
    observacion = datos.get("observacion")

    try:
        consulta = ConsultaService.cancelar_consulta(
            id_consulta=id_consulta,
            observacion=observacion,
        )

        return jsonify({
            "estado": "correcto",
            "mensaje": (
                "Consulta cancelada correctamente"
            ),
            "datos": consulta.to_dict(),
        })

    except ValueError as error:
        return jsonify({
            "estado": "error",
            "mensaje": str(error),
        }), 404

    except Exception as error:
        traceback.print_exc()

        return jsonify({
            "estado": "error",
            "mensaje": (
                "No se pudo cancelar la consulta"
            ),
            "detalle": str(error),
            "tipo_error": type(error).__name__,
        }), 500