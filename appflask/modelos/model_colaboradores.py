#modelos/model_colaboradores.py
from dbconfig.database import db

class Colaborador(db.Model):
    __tablename__ = 'colaboradores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

    proyecto = db.relationship('Proyecto', backref='colaboradores')
    usuario = db.relationship('Usuario', backref='colaboradores')

    def __init__(self, idProyecto, idUsuario, rol):
        self.idProyecto = idProyecto
        self.idUsuario = idUsuario
        self.rol = rol

    def __repr__(self):
        return f"<Colaborador {self.id}: Proyecto {self.idProyecto}, Usuario {self.idUsuario}, Rol {self.rol}>"
    