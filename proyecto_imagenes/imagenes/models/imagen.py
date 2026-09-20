from datetime import datetime

from ..database import db


class Imagen(db.Model):
    __tablename__ = "imagenes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    comentario = db.Column(db.String(255))

    archivo_original = db.Column(db.String(255), nullable=False)
    archivo_procesado = db.Column(db.String(255), nullable=False)
    peso_original = db.Column(db.Integer)
    peso_procesado = db.Column(db.Integer)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Imagen {self.id} - {self.nombre}>"
