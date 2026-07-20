from datetime import datetime
from . import db


class Diagnostico(db.Model):
    __tablename__ = "diagnosticos"

    id_diagnostico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey("categorias_falla.id_categoria"),
        nullable=False,
        index=True,
    )
    codigo = db.Column(db.String(30), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    nivel_severidad = db.Column(
        db.Enum(
            "BAJO",
            "MEDIO",
            "ALTO",
            "CRITICO",
            name="nivel_severidad_enum",
        ),
        nullable=False,
        default="MEDIO",
    )

    requiere_escalamiento = db.Column(db.Boolean, nullable=False, default=False)
    estado = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    categoria = db.relationship("CategoriaFalla", back_populates="diagnosticos")

    reglas = db.relationship(
        "Regla",
        back_populates="diagnostico",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    recomendaciones = db.relationship(
        "Recomendacion",
        back_populates="diagnostico",
        lazy="dynamic",
        cascade="all, delete-orphan",
        order_by="Recomendacion.orden",
    )

    resultados = db.relationship(
        "ResultadoDiagnostico",
        back_populates="diagnostico",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def to_dict(self, incluir_recomendaciones=False):
        data = {
            "id_diagnostico": self.id_diagnostico,
            "id_categoria": self.id_categoria,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "nivel_severidad": self.nivel_severidad,
            "requiere_escalamiento": bool(self.requiere_escalamiento),
            "estado": bool(self.estado),
        }

        if incluir_recomendaciones:
            data["recomendaciones"] = [
                item.to_dict()
                for item in self.recomendaciones.filter_by(estado=True).all()
            ]

        return data

    def __repr__(self):
        return f"<Diagnostico {self.codigo}>"
