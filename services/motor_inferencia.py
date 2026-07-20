from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from sqlalchemy.orm import joinedload, selectinload

from models import (
    db,
    Consulta,
    RespuestaConsulta,
    Regla,
    ReglaActivada,
    ResultadoDiagnostico,
    CondicionRegla,
)


@dataclass
class EvaluacionCondicion:
    id_condicion: int
    id_sintoma: int
    codigo_sintoma: str
    pregunta: str
    valor_recibido: str | None
    valor_esperado: str
    operador: str
    peso: float
    evaluable: bool
    cumplida: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_condicion": self.id_condicion,
            "id_sintoma": self.id_sintoma,
            "codigo_sintoma": self.codigo_sintoma,
            "pregunta": self.pregunta,
            "valor_recibido": self.valor_recibido,
            "valor_esperado": self.valor_esperado,
            "operador": self.operador,
            "peso": self.peso,
            "evaluable": self.evaluable,
            "cumplida": self.cumplida,
        }


class MotorInferenciaService:
    """
    Motor de inferencia por encadenamiento hacia adelante.

    Flujo:
    1. Obtiene las respuestas de una consulta.
    2. Evalúa las condiciones de las reglas activas.
    3. Registra las reglas que alcanzan el umbral mínimo.
    4. Agrupa evidencias por diagnóstico.
    5. Calcula confianza y selecciona el diagnóstico principal.
    """

    VALORES_DESCONOCIDOS = {
        "",
        "NO_SE",
        "NO SÉ",
        "NO_SE_APLICA",
        "DESCONOCIDO",
        "NULL",
        "NONE",
    }

    def __init__(
        self,
        umbral_activacion: float = 50.0,
        max_resultados: int = 5,
    ) -> None:
        if not 0 <= umbral_activacion <= 100:
            raise ValueError("El umbral de activación debe estar entre 0 y 100.")

        self.umbral_activacion = float(umbral_activacion)
        self.max_resultados = int(max_resultados)

    def evaluar_consulta(
            self,
            id_consulta: int,
    ) -> dict[str, Any]:

        consulta = (
            Consulta.query
            .filter_by(id_consulta=id_consulta)
            .first()
        )

        if consulta is None:
            raise ValueError(
                f"No existe la consulta con id {id_consulta}."
            )

        if consulta.estado_consulta == "CANCELADA":
            raise ValueError(
                "No se puede evaluar una consulta cancelada."
            )

        respuestas_guardadas = (
            RespuestaConsulta.query
            .filter_by(id_consulta=id_consulta)
            .all()
        )

        print(
            "RESPUESTAS EN BD PARA CONSULTA",
            id_consulta,
            ":",
            len(respuestas_guardadas),
            flush=True,
        )

        for respuesta in respuestas_guardadas:
            print(
                "Síntoma:",
                respuesta.id_sintoma,
                "Valor:",
                respuesta.valor_respuesta,
                flush=True,
            )

        respuestas = {
            respuesta.id_sintoma:
                respuesta.valor_respuesta
            for respuesta in respuestas_guardadas
        }

        if not respuestas:
            raise ValueError(
                f"La consulta {id_consulta} no tiene respuestas "
                "registradas en la base de datos."
            )

        reglas = (
            Regla.query.options(
                joinedload(Regla.diagnostico),
                selectinload(
                    Regla.condiciones
                ).joinedload(
                    CondicionRegla.sintoma
                ),
            )
            .filter(Regla.estado.is_(True))
            .order_by(
                Regla.prioridad.desc(),
                Regla.id_regla.asc(),
            )
            .all()
        )

        if not reglas:
            raise ValueError(
                "No existen reglas activas en la base de conocimiento."
            )

        # Elimina resultados anteriores para recalcular.
        ReglaActivada.query.filter_by(
            id_consulta=id_consulta
        ).delete(
            synchronize_session=False
        )

        ResultadoDiagnostico.query.filter_by(
            id_consulta=id_consulta
        ).delete(
            synchronize_session=False
        )

        evaluaciones_reglas: list[
            dict[str, Any]
        ] = []

        reglas_activadas: list[
            dict[str, Any]
        ] = []

        for regla in reglas:
            evaluacion = self._evaluar_regla(
                regla=regla,
                respuestas=respuestas,
            )

            evaluaciones_reglas.append(
                evaluacion
            )

            print(
                "REGLA:",
                evaluacion["codigo"],
                "CUMPLIMIENTO:",
                evaluacion["porcentaje_cumplimiento"],
                "ACTIVADA:",
                evaluacion["activada"],
                flush=True,
            )

            if not evaluacion["activada"]:
                continue

            activacion = ReglaActivada(
                id_consulta=id_consulta,
                id_regla=regla.id_regla,
                porcentaje_cumplimiento=round(
                    evaluacion[
                        "porcentaje_cumplimiento"
                    ],
                    2,
                ),
                detalle=json.dumps(
                    evaluacion["condiciones"],
                    ensure_ascii=False,
                ),
            )

            db.session.add(activacion)
            reglas_activadas.append(
                evaluacion
            )

        resultados = self._crear_resultados(
            id_consulta=id_consulta,
            reglas_activadas=reglas_activadas,
        )

        if resultados:
            consulta.estado_consulta = "FINALIZADA"
            consulta.fecha_fin = datetime.utcnow()
        else:
            consulta.estado_consulta = "INICIADA"
            consulta.fecha_fin = None

        try:
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        respuesta_final = {
            "consulta": consulta.to_dict(),
            "cantidad_reglas_evaluadas": len(
                evaluaciones_reglas
            ),
            "cantidad_reglas_activadas": len(
                reglas_activadas
            ),
            "reglas_activadas": reglas_activadas,
            "resultados": [
                resultado.to_dict()
                for resultado in resultados
            ],
        }

        print(
            "RESULTADO FINAL DEL MOTOR:",
            respuesta_final,
            flush=True,
        )

        return respuesta_final


    def _evaluar_regla(
        self,
        regla: Regla,
        respuestas: dict[int, str],
    ) -> dict[str, Any]:
        evaluaciones: list[EvaluacionCondicion] = []

        for condicion in regla.condiciones:
            valor_recibido = respuestas.get(condicion.id_sintoma)
            evaluable = not self._es_desconocido(valor_recibido)

            cumplida = False
            if evaluable:
                cumplida = self._comparar(
                    valor_recibido,
                    condicion.valor_esperado,
                    condicion.operador_comparacion,
                )

            evaluaciones.append(
                EvaluacionCondicion(
                    id_condicion=condicion.id_condicion,
                    id_sintoma=condicion.id_sintoma,
                    codigo_sintoma=condicion.sintoma.codigo,
                    pregunta=condicion.sintoma.pregunta,
                    valor_recibido=valor_recibido,
                    valor_esperado=condicion.valor_esperado,
                    operador=condicion.operador_comparacion,
                    peso=float(condicion.peso or 1),
                    evaluable=evaluable,
                    cumplida=cumplida,
                )
            )

        evaluables = [item for item in evaluaciones if item.evaluable]

        if not evaluables:
            porcentaje = 0.0
            activada = False
        elif regla.operador_logico == "OR":
            # En OR basta una condición; se conserva el porcentaje ponderado
            # para ordenar reglas con más evidencia.
            activada = any(item.cumplida for item in evaluables)
            porcentaje = self._porcentaje_ponderado(evaluables)
        else:
            # En AND se permite activación parcial por umbral, porque algunas
            # respuestas pueden ser desconocidas. El porcentaje representa
            # cuánta evidencia disponible coincide con la regla.
            porcentaje = self._porcentaje_ponderado(evaluables)
            activada = porcentaje >= self.umbral_activacion

        factor = self._normalizar_factor_confianza(regla.factor_confianza)
        confianza = min(100.0, porcentaje * factor)

        return {
            "id_regla": regla.id_regla,
            "codigo": regla.codigo,
            "nombre": regla.nombre,
            "id_diagnostico": regla.id_diagnostico,
            "diagnostico": regla.diagnostico.nombre,
            "operador_logico": regla.operador_logico,
            "prioridad": regla.prioridad,
            "factor_confianza": factor,
            "porcentaje_cumplimiento": round(porcentaje, 2),
            "porcentaje_confianza": round(confianza, 2),
            "activada": bool(activada),
            "condiciones": [item.to_dict() for item in evaluaciones],
        }

    @staticmethod
    def _porcentaje_ponderado(
        evaluaciones: list[EvaluacionCondicion],
    ) -> float:
        peso_total = sum(max(item.peso, 0.0) for item in evaluaciones)
        if peso_total <= 0:
            return 0.0

        peso_cumplido = sum(
            max(item.peso, 0.0)
            for item in evaluaciones
            if item.cumplida
        )
        return (peso_cumplido / peso_total) * 100.0

    def _crear_resultados(
        self,
        id_consulta: int,
        reglas_activadas: list[dict[str, Any]],
    ) -> list[ResultadoDiagnostico]:
        agrupadas: dict[int, list[dict[str, Any]]] = defaultdict(list)

        for regla in reglas_activadas:
            agrupadas[regla["id_diagnostico"]].append(regla)

        candidatos: list[dict[str, Any]] = []

        for id_diagnostico, evidencias in agrupadas.items():
            # Se combina la mejor evidencia con un pequeño refuerzo por
            # reglas adicionales compatibles, sin superar 100%.
            confianzas = sorted(
                (float(item["porcentaje_confianza"]) for item in evidencias),
                reverse=True,
            )

            confianza_combinada = confianzas[0]
            for confianza in confianzas[1:]:
                confianza_combinada += (
                    (100.0 - confianza_combinada) * (confianza / 100.0) * 0.25
                )

            confianza_combinada = min(100.0, confianza_combinada)

            evidencias_ordenadas = sorted(
                evidencias,
                key=lambda item: (
                    item["porcentaje_confianza"],
                    item["prioridad"],
                ),
                reverse=True,
            )

            explicacion = self._generar_explicacion(evidencias_ordenadas)

            candidatos.append(
                {
                    "id_diagnostico": id_diagnostico,
                    "confianza": round(confianza_combinada, 2),
                    "prioridad": max(item["prioridad"] for item in evidencias),
                    "explicacion": explicacion,
                }
            )

        candidatos.sort(
            key=lambda item: (
                item["confianza"],
                item["prioridad"],
            ),
            reverse=True,
        )

        resultados: list[ResultadoDiagnostico] = []

        for indice, candidato in enumerate(candidatos[: self.max_resultados]):
            resultado = ResultadoDiagnostico(
                id_consulta=id_consulta,
                id_diagnostico=candidato["id_diagnostico"],
                porcentaje_confianza=candidato["confianza"],
                es_principal=(indice == 0),
                explicacion=candidato["explicacion"],
            )
            db.session.add(resultado)
            resultados.append(resultado)

        db.session.flush()
        return resultados

    @staticmethod
    def _generar_explicacion(
        evidencias: list[dict[str, Any]],
    ) -> str:
        fragmentos: list[str] = []

        for regla in evidencias:
            condiciones_cumplidas = [
                condicion
                for condicion in regla["condiciones"]
                if condicion["evaluable"] and condicion["cumplida"]
            ]

            hechos = [
                (
                    f'{condicion["codigo_sintoma"]}='
                    f'{condicion["valor_recibido"]}'
                )
                for condicion in condiciones_cumplidas
            ]

            detalle_hechos = ", ".join(hechos) if hechos else "evidencia parcial"

            fragmentos.append(
                f'Se activó {regla["codigo"]} ({regla["nombre"]}) '
                f'con {regla["porcentaje_cumplimiento"]:.2f}% de cumplimiento, '
                f'a partir de: {detalle_hechos}.'
            )

        return " ".join(fragmentos)

    @classmethod
    def _es_desconocido(cls, valor: Any) -> bool:
        if valor is None:
            return True
        return str(valor).strip().upper() in cls.VALORES_DESCONOCIDOS

    @classmethod
    def _comparar(
            cls,
            valor_recibido: Any,
            valor_esperado: Any,
            operador: str,
    ) -> bool:
        operador_normalizado = str(
            operador or "="
        ).strip().upper()

        equivalencias_operador = {
            "=": "=",
            "==": "=",
            "IGUAL": "=",

            "!=": "!=",
            "<>": "!=",
            "DIFERENTE": "!=",

            ">": ">",
            "MAYOR": ">",

            "<": "<",
            "MENOR": "<",

            ">=": ">=",
            "MAYOR_IGUAL": ">=",
            "MAYOR O IGUAL": ">=",

            "<=": "<=",
            "MENOR_IGUAL": "<=",
            "MENOR O IGUAL": "<=",

            "CONTIENE": "CONTIENE",
        }

        operador_normalizado = equivalencias_operador.get(
            operador_normalizado,
            operador_normalizado,
        )

        recibido_normalizado = cls._normalizar_texto(
            valor_recibido
        )
        esperado_normalizado = cls._normalizar_texto(
            valor_esperado
        )

        if operador_normalizado == "=":
            return (
                    recibido_normalizado ==
                    esperado_normalizado
            )

        if operador_normalizado == "!=":
            return (
                    recibido_normalizado !=
                    esperado_normalizado
            )

        if operador_normalizado == "CONTIENE":
            return (
                    esperado_normalizado
                    in recibido_normalizado
            )

        recibido_numero = cls._a_decimal(
            valor_recibido
        )
        esperado_numero = cls._a_decimal(
            valor_esperado
        )

        if (
                recibido_numero is None or
                esperado_numero is None
        ):
            return False

        if operador_normalizado == ">":
            return recibido_numero > esperado_numero

        if operador_normalizado == "<":
            return recibido_numero < esperado_numero

        if operador_normalizado == ">=":
            return recibido_numero >= esperado_numero

        if operador_normalizado == "<=":
            return recibido_numero <= esperado_numero

        return False

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        texto = str(valor).strip().upper()

        equivalencias = {
            "TRUE": "SI",
            "1": "SI",
            "VERDADERO": "SI",
            "YES": "SI",
            "FALSE": "NO",
            "0": "NO",
            "FALSO": "NO",
        }
        return equivalencias.get(texto, texto)

    @staticmethod
    def _a_decimal(valor: Any) -> Decimal | None:
        try:
            return Decimal(str(valor).strip().replace(",", "."))
        except (InvalidOperation, ValueError, TypeError):
            return None

    @staticmethod
    def _normalizar_factor_confianza(valor: Any) -> float:
        try:
            factor = float(valor)
        except (TypeError, ValueError):
            return 1.0

        # Permite guardar 0.85 o 85 en la base de datos.
        if factor > 1:
            factor /= 100.0

        return max(0.0, min(factor, 1.0))
