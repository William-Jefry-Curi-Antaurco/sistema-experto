from models import Sintoma, Consulta, RespuestaConsulta


class PreguntaService:
    @staticmethod
    def listar_preguntas(
        id_categoria: int | None = None,
    ) -> list[Sintoma]:
        query = Sintoma.query.filter_by(estado=True)

        if id_categoria is not None:
            query = query.filter_by(id_categoria=id_categoria)

        return query.order_by(Sintoma.orden.asc(), Sintoma.id_sintoma.asc()).all()

    @staticmethod
    def siguiente_pregunta(
        id_consulta: int,
        id_categoria: int | None = None,
    ) -> Sintoma | None:
        consulta = Consulta.query.get(id_consulta)
        if consulta is None:
            raise ValueError("La consulta no existe.")

        respondidas = {
            item.id_sintoma
            for item in RespuestaConsulta.query.filter_by(
                id_consulta=id_consulta
            ).all()
        }

        preguntas = PreguntaService.listar_preguntas(id_categoria=id_categoria)

        return next(
            (
                pregunta
                for pregunta in preguntas
                if pregunta.id_sintoma not in respondidas
            ),
            None,
        )
