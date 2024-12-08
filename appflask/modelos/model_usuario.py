#modelos/model_usuario.py
from dbconfig.database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre, email, contrasena):
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena

    def __repr__(self):
        return f"<Usuario {self.id}: {self.nombre}>"
