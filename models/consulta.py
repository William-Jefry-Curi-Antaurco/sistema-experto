from datetime import datetime
from . import db


class Consulta(db.Model):
    __tablename__ = "consultas"

    id_consulta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_usuario = db.Column(db.String(150), nullable=False)
    descripcion_problema = db.Column(db.Text, nullable=True)

    estado_consulta = db.Column(
        db.Enum(
            "INICIADA",
            "FINALIZADA",
            "CANCELADA",
            name="estado_consulta_enum",
        ),
        nullable=False,
        default="INICIADA",
    )

    observacion = db.Column(db.Text, nullable=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime, nullable=True)

    respuestas = db.relationship(
        "RespuestaConsulta",
        back_populates="consulta",
        lazy="select",
        cascade="all, delete-orphan",
        order_by="RespuestaConsulta.created_at",
    )

    reglas_activadas = db.relationship(
        "ReglaActivada",
        back_populates="consulta",
        lazy="select",
        cascade="all, delete-orphan",
        order_by="ReglaActivada.porcentaje_cumplimiento.desc()",
    )

    resultados = db.relationship(
        "ResultadoDiagnostico",
        back_populates="consulta",
        lazy="select",
        cascade="all, delete-orphan",
        order_by="ResultadoDiagnostico.porcentaje_confianza.desc()",
    )

    def to_dict(self, incluir_detalle=False):
        data = {
            "id_consulta": self.id_consulta,
            "nombre_usuario": self.nombre_usuario,
            "descripcion_problema": self.descripcion_problema,
            "estado_consulta": self.estado_consulta,
            "observacion": self.observacion,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
        }

        if incluir_detalle:
            data["respuestas"] = [r.to_dict() for r in self.respuestas]
            data["reglas_activadas"] = [r.to_dict() for r in self.reglas_activadas]
            data["resultados"] = [r.to_dict() for r in self.resultados]

        return data

    def __repr__(self):
        return f"<Consulta {self.id_consulta}>"


class RespuestaConsulta(db.Model):
    __tablename__ = "respuestas_consulta"

    id_respuesta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(
        db.Integer,
        db.ForeignKey("consultas.id_consulta"),
        nullable=False,
        index=True,
    )
    id_sintoma = db.Column(
        db.Integer,
        db.ForeignKey("sintomas.id_sintoma"),
        nullable=False,
        index=True,
    )
    valor_respuesta = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    consulta = db.relationship("Consulta", back_populates="respuestas")
    sintoma = db.relationship("Sintoma", back_populates="respuestas")

    __table_args__ = (
        db.UniqueConstraint(
            "id_consulta",
            "id_sintoma",
            name="uq_respuesta_consulta_sintoma",
        ),
    )

    def to_dict(self):
        return {
            "id_respuesta": self.id_respuesta,
            "id_consulta": self.id_consulta,
            "id_sintoma": self.id_sintoma,
            "valor_respuesta": self.valor_respuesta,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<RespuestaConsulta consulta={self.id_consulta} sintoma={self.id_sintoma}>"


class ReglaActivada(db.Model):
    __tablename__ = "reglas_activadas"

    id_activacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(
        db.Integer,
        db.ForeignKey("consultas.id_consulta"),
        nullable=False,
        index=True,
    )
    id_regla = db.Column(
        db.Integer,
        db.ForeignKey("reglas.id_regla"),
        nullable=False,
        index=True,
    )
    porcentaje_cumplimiento = db.Column(db.Numeric(5, 2), nullable=False)
    detalle = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    consulta = db.relationship("Consulta", back_populates="reglas_activadas")
    regla = db.relationship("Regla", back_populates="activaciones")

    __table_args__ = (
        db.UniqueConstraint(
            "id_consulta",
            "id_regla",
            name="uq_regla_activada_consulta",
        ),
    )

    def to_dict(self):
        return {
            "id_activacion": self.id_activacion,
            "id_consulta": self.id_consulta,
            "id_regla": self.id_regla,
            "codigo_regla": self.regla.codigo if self.regla else None,
            "porcentaje_cumplimiento": float(self.porcentaje_cumplimiento or 0),
            "detalle": self.detalle,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<ReglaActivada consulta={self.id_consulta} regla={self.id_regla}>"


class ResultadoDiagnostico(db.Model):
    __tablename__ = "resultados_diagnostico"

    id_resultado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(
        db.Integer,
        db.ForeignKey("consultas.id_consulta"),
        nullable=False,
        index=True,
    )
    id_diagnostico = db.Column(
        db.Integer,
        db.ForeignKey("diagnosticos.id_diagnostico"),
        nullable=False,
        index=True,
    )
    porcentaje_confianza = db.Column(db.Numeric(5, 2), nullable=False)
    es_principal = db.Column(db.Boolean, nullable=False, default=False)
    explicacion = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    consulta = db.relationship("Consulta", back_populates="resultados")
    diagnostico = db.relationship("Diagnostico", back_populates="resultados")

    __table_args__ = (
        db.UniqueConstraint(
            "id_consulta",
            "id_diagnostico",
            name="uq_resultado_consulta_diagnostico",
        ),
    )

    def to_dict(self, incluir_recomendaciones=True):
        data = {
            "id_resultado": self.id_resultado,
            "id_consulta": self.id_consulta,
            "id_diagnostico": self.id_diagnostico,
            "porcentaje_confianza": float(self.porcentaje_confianza or 0),
            "es_principal": bool(self.es_principal),
            "explicacion": self.explicacion,
            "diagnostico": self.diagnostico.to_dict()
            if self.diagnostico
            else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

        if incluir_recomendaciones and self.diagnostico:
            data["recomendaciones"] = [
                r.to_dict()
                for r in self.diagnostico.recomendaciones.filter_by(estado=True).all()
            ]

        return data

    def __repr__(self):
        return (
            f"<ResultadoDiagnostico consulta={self.id_consulta} "
            f"diagnostico={self.id_diagnostico}>"
        )
