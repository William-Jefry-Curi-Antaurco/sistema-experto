from flask import Blueprint, jsonify, request

from models import CategoriaFalla, Sintoma, Diagnostico


catalogo_bp = Blueprint(
    "catalogos",
    __name__,
    url_prefix="/api/catalogos"
)


@catalogo_bp.get("/categorias")
def listar_categorias():
    try:
        categorias = (
            CategoriaFalla.query
            .filter_by(estado=True)
            .order_by(CategoriaFalla.nombre.asc())
            .all()
        )

        return jsonify({
            "estado": "correcto",
            "cantidad": len(categorias),
            "datos": [
                categoria.to_dict()
                for categoria in categorias
            ]
        })

    except Exception as error:
        return jsonify({
            "estado": "error",
            "mensaje": "No se pudieron listar las categorías",
            "detalle": str(error)
        }), 500


@catalogo_bp.get("/categorias/<int:id_categoria>")
def obtener_categoria(id_categoria):
    categoria = CategoriaFalla.query.get(id_categoria)

    if categoria is None:
        return jsonify({
            "estado": "error",
            "mensaje": "La categoría no existe"
        }), 404

    return jsonify({
        "estado": "correcto",
        "datos": categoria.to_dict()
    })


@catalogo_bp.get("/sintomas")
def listar_sintomas():
    try:
        id_categoria = request.args.get("id_categoria", type=int)

        query = Sintoma.query.filter_by(estado=True)

        if id_categoria is not None:
            query = query.filter_by(id_categoria=id_categoria)

        sintomas = (
            query
            .order_by(
                Sintoma.orden.asc(),
                Sintoma.id_sintoma.asc()
            )
            .all()
        )

        return jsonify({
            "estado": "correcto",
            "cantidad": len(sintomas),
            "datos": [
                sintoma.to_dict()
                for sintoma in sintomas
            ]
        })

    except Exception as error:
        return jsonify({
            "estado": "error",
            "mensaje": "No se pudieron listar los síntomas",
            "detalle": str(error)
        }), 500


@catalogo_bp.get("/categorias/<int:id_categoria>/sintomas")
def listar_sintomas_categoria(id_categoria):
    categoria = CategoriaFalla.query.get(id_categoria)

    if categoria is None:
        return jsonify({
            "estado": "error",
            "mensaje": "La categoría no existe"
        }), 404

    try:
        sintomas = (
            Sintoma.query
            .filter_by(
                id_categoria=id_categoria,
                estado=True
            )
            .order_by(
                Sintoma.orden.asc(),
                Sintoma.id_sintoma.asc()
            )
            .all()
        )

        return jsonify({
            "estado": "correcto",
            "categoria": categoria.to_dict(),
            "cantidad": len(sintomas),
            "datos": [
                sintoma.to_dict()
                for sintoma in sintomas
            ]
        })

    except Exception as error:
        return jsonify({
            "estado": "error",
            "mensaje": "No se pudieron listar los síntomas",
            "detalle": str(error)
        }), 500


@catalogo_bp.get("/diagnosticos")
def listar_diagnosticos():
    try:
        id_categoria = request.args.get("id_categoria", type=int)

        query = Diagnostico.query.filter_by(estado=True)

        if id_categoria is not None:
            query = query.filter_by(id_categoria=id_categoria)

        diagnosticos = (
            query
            .order_by(Diagnostico.nombre.asc())
            .all()
        )

        return jsonify({
            "estado": "correcto",
            "cantidad": len(diagnosticos),
            "datos": [
                diagnostico.to_dict(
                    incluir_recomendaciones=True
                )
                for diagnostico in diagnosticos
            ]
        })

    except Exception as error:
        return jsonify({
            "estado": "error",
            "mensaje": "No se pudieron listar los diagnósticos",
            "detalle": str(error)
        }), 500