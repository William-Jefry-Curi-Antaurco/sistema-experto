from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from models import db, Consulta, RespuestaConsulta, Sintoma


class ConsultaService:

    @staticmethod
    def crear_consulta(
        nombre_usuario: str,
        descripcion_problema: str | None = None,
    ) -> Consulta:
        nombre = (nombre_usuario or "").strip()

        if not nombre:
            raise ValueError(
                "El nombre del usuario es obligatorio."
            )

        consulta = Consulta(
            nombre_usuario=nombre,
            descripcion_problema=descripcion_problema,
            estado_consulta="INICIADA",
        )

        try:
            db.session.add(consulta)
            db.session.commit()

        except SQLAlchemyError as error:
            db.session.rollback()
            raise RuntimeError(
                f"No se pudo crear la consulta: {error}"
            ) from error

        return consulta

    @staticmethod
    def guardar_respuesta(
            id_consulta: int,
            id_sintoma: int,
            valor_respuesta: str,
    ) -> RespuestaConsulta:
        consulta = db.session.get(
            Consulta,
            id_consulta,
        )

        if consulta is None:
            raise ValueError(
                "La consulta no existe."
            )

        if consulta.estado_consulta == "CANCELADA":
            raise ValueError(
                "No se pueden registrar respuestas "
                "en una consulta cancelada."
            )

        sintoma = Sintoma.query.filter_by(
            id_sintoma=id_sintoma,
            estado=True,
        ).first()

        if sintoma is None:
            raise ValueError(
                "El síntoma no existe o está inactivo."
            )

        valor = str(
            valor_respuesta or ""
        ).strip().upper()

        if valor not in {
            "SI",
            "NO",
            "NO_SE",
        }:
            raise ValueError(
                "La respuesta debe ser SI, NO o NO_SE."
            )

        respuesta = RespuestaConsulta.query.filter_by(
            id_consulta=id_consulta,
            id_sintoma=id_sintoma,
        ).first()

        if respuesta is None:
            respuesta = RespuestaConsulta(
                id_consulta=id_consulta,
                id_sintoma=id_sintoma,
                valor_respuesta=valor,
            )

            db.session.add(respuesta)

        else:
            respuesta.valor_respuesta = valor

        try:
            db.session.commit()
            db.session.refresh(respuesta)

            cantidad = (
                RespuestaConsulta.query
                .filter_by(
                    id_consulta=id_consulta
                )
                .count()
            )

            print(
                "RESPUESTA CONFIRMADA EN BD:",
                respuesta.id_respuesta,
                flush=True,
            )

            print(
                "TOTAL RESPUESTAS CONSULTA",
                id_consulta,
                ":",
                cantidad,
                flush=True,
            )

        except Exception:
            db.session.rollback()
            raise

        return respuesta



    @staticmethod
    def cancelar_consulta(
        id_consulta: int,
        observacion: str | None = None,
    ) -> Consulta:
        consulta = Consulta.query.get(id_consulta)

        if consulta is None:
            raise ValueError("La consulta no existe.")

        if consulta.estado_consulta == "FINALIZADA":
            raise ValueError(
                "No se puede cancelar una consulta finalizada."
            )

        if consulta.estado_consulta == "CANCELADA":
            raise ValueError(
                "La consulta ya se encuentra cancelada."
            )

        consulta.estado_consulta = "CANCELADA"
        consulta.observacion = (
            observacion.strip()
            if observacion
            else None
        )
        consulta.fecha_fin = datetime.utcnow()

        try:
            db.session.commit()

        except SQLAlchemyError as error:
            db.session.rollback()

            raise RuntimeError(
                f"No se pudo cancelar la consulta: {error}"
            ) from error

        return consulta