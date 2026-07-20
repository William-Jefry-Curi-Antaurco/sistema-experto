from datetime import datetime

from . import db


class Sintoma(db.Model):
    __tablename__ = "sintomas"

    id_sintoma = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey("categorias_falla.id_categoria"),
        nullable=False,
        index=True,
    )

    codigo = db.Column(
        db.String(60),
        nullable=False,
        unique=True,
    )

    nombre = db.Column(
        db.String(150),
        nullable=False,
    )

    descripcion = db.Column(
        db.Text,
        nullable=True,
    )

    pregunta = db.Column(
        db.String(255),
        nullable=False,
    )

    tipo_respuesta = db.Column(
        db.Enum(
            "BOOLEANO",
            "OPCION",
            "TEXTO",
            "NUMERICO",
            name="tipo_respuesta_enum",
        ),
        nullable=False,
        default="BOOLEANO",
    )

    unidad_medida = db.Column(
        db.String(30),
        nullable=True,
    )

    orden = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    estado = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    categoria = db.relationship(
        "CategoriaFalla",
        back_populates="sintomas",
    )

    condiciones = db.relationship(
        "CondicionRegla",
        back_populates="sintoma",
        lazy="dynamic",
    )

    respuestas = db.relationship(
        "RespuestaConsulta",
        back_populates="sintoma",
        lazy="dynamic",
    )

    def to_dict(self):
        return {
            "id_sintoma": self.id_sintoma,
            "id_categoria": self.id_categoria,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "pregunta": self.pregunta,
            "tipo_respuesta": self.tipo_respuesta,
            "unidad_medida": self.unidad_medida,
            "orden": self.orden,
            "estado": bool(self.estado),
        }

    def __repr__(self):
        return f"<Sintoma {self.codigo}>"