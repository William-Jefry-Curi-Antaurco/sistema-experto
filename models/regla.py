from datetime import datetime
from . import db


class Regla(db.Model):
    __tablename__ = "reglas"

    id_regla = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_diagnostico = db.Column(
        db.Integer,
        db.ForeignKey("diagnosticos.id_diagnostico"),
        nullable=False,
        index=True,
    )
    codigo = db.Column(db.String(30), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    operador_logico = db.Column(
        db.Enum("AND", "OR", name="operador_logico_enum"),
        nullable=False,
        default="AND",
    )

    prioridad = db.Column(db.Integer, nullable=False, default=0)
    factor_confianza = db.Column(db.Numeric(5, 4), nullable=False, default=1.0000)
    fuente = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    diagnostico = db.relationship("Diagnostico", back_populates="reglas")

    condiciones = db.relationship(
        "CondicionRegla",
        back_populates="regla",
        lazy="select",
        cascade="all, delete-orphan",
        order_by="CondicionRegla.id_condicion",
    )

    activaciones = db.relationship(
        "ReglaActivada",
        back_populates="regla",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def to_dict(self, incluir_condiciones=False):
        data = {
            "id_regla": self.id_regla,
            "id_diagnostico": self.id_diagnostico,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "operador_logico": self.operador_logico,
            "prioridad": self.prioridad,
            "factor_confianza": float(self.factor_confianza or 0),
            "fuente": self.fuente,
            "estado": bool(self.estado),
        }

        if incluir_condiciones:
            data["condiciones"] = [
                condicion.to_dict() for condicion in self.condiciones
            ]

        return data

    def __repr__(self):
        return f"<Regla {self.codigo}>"


class CondicionRegla(db.Model):
    __tablename__ = "condiciones_regla"

    id_condicion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_regla = db.Column(
        db.Integer,
        db.ForeignKey("reglas.id_regla"),
        nullable=False,
        index=True,
    )
    id_sintoma = db.Column(
        db.Integer,
        db.ForeignKey("sintomas.id_sintoma"),
        nullable=False,
        index=True,
    )

    operador_comparacion = db.Column(
        db.Enum(
            "=",
            "!=",
            ">",
            "<",
            ">=",
            "<=",
            "CONTIENE",
            name="operador_comparacion_enum",
        ),
        nullable=False,
        default="=",
    )

    valor_esperado = db.Column(db.String(100), nullable=False)
    peso = db.Column(db.Numeric(5, 4), nullable=False, default=1.0000)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    regla = db.relationship("Regla", back_populates="condiciones")
    sintoma = db.relationship("Sintoma", back_populates="condiciones")

    __table_args__ = (
        db.UniqueConstraint(
            "id_regla",
            "id_sintoma",
            name="uq_condicion_regla_sintoma",
        ),
    )

    def to_dict(self):
        return {
            "id_condicion": self.id_condicion,
            "id_regla": self.id_regla,
            "id_sintoma": self.id_sintoma,
            "operador_comparacion": self.operador_comparacion,
            "valor_esperado": self.valor_esperado,
            "peso": float(self.peso or 0),
        }

    def __repr__(self):
        return f"<CondicionRegla regla={self.id_regla} sintoma={self.id_sintoma}>"
