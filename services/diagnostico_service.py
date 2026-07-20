from models import ResultadoDiagnostico


class DiagnosticoService:
    @staticmethod
    def obtener_resultados(id_consulta: int) -> list[dict]:
        resultados = (
            ResultadoDiagnostico.query.filter_by(id_consulta=id_consulta)
            .order_by(
                ResultadoDiagnostico.es_principal.desc(),
                ResultadoDiagnostico.porcentaje_confianza.desc(),
            )
            .all()
        )

        return [
            resultado.to_dict(incluir_recomendaciones=True)
            for resultado in resultados
        ]

    @staticmethod
    def obtener_principal(id_consulta: int) -> dict | None:
        resultado = ResultadoDiagnostico.query.filter_by(
            id_consulta=id_consulta,
            es_principal=True,
        ).first()

        return (
            resultado.to_dict(incluir_recomendaciones=True)
            if resultado
            else None
        )
