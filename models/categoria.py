from datetime import datetime

from . import db


class CategoriaFalla(db.Model):
    __tablename__ = "categorias_falla"

    id_categoria = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    nombre = db.Column(
        db.String(100),
        nullable=False,
        unique=True,
    )

    descripcion = db.Column(
        db.Text,
        nullable=True,
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

    sintomas = db.relationship(
        "Sintoma",
        back_populates="categoria",
        lazy="dynamic",
    )

    diagnosticos = db.relationship(
        "Diagnostico",
        back_populates="categoria",
        lazy="dynamic",
    )

    def to_dict(self):
        return {
            "id_categoria": self.id_categoria,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": bool(self.estado),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at
                else None
            ),
        }

    def __repr__(self):
        return f"<CategoriaFalla {self.nombre}>"