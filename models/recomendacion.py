from datetime import datetime
from . import db


class Recomendacion(db.Model):
    __tablename__ = "recomendaciones"

    id_recomendacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_diagnostico = db.Column(
        db.Integer,
        db.ForeignKey("diagnosticos.id_diagnostico"),
        nullable=False,
        index=True,
    )
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    comando_sugerido = db.Column(db.String(255), nullable=True)
    orden = db.Column(db.Integer, nullable=False, default=0)
    estado = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    diagnostico = db.relationship("Diagnostico", back_populates="recomendaciones")

    def to_dict(self):
        return {
            "id_recomendacion": self.id_recomendacion,
            "id_diagnostico": self.id_diagnostico,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "comando_sugerido": self.comando_sugerido,
            "orden": self.orden,
            "estado": bool(self.estado),
        }

    def __repr__(self):
        return f"<Recomendacion {self.titulo}>"
