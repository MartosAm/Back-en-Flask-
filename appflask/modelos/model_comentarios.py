#modelos/model_comentarios.py
from dbconfig.database import db

class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    idTarea = db.Column(db.Integer, db.ForeignKey('tareas.id'), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    fechaHora = db.Column(db.DateTime, nullable=False)

    proyecto = db.relationship('Proyecto', backref='comentarios')
    tarea = db.relationship('Tarea', backref='comentarios')
    usuario = db.relationship('Usuario', backref='comentarios')

    def __init__(self, idProyecto, idTarea, idUsuario, texto, fechaHora):
        self.idProyecto = idProyecto
        self.idTarea = idTarea
        self.idUsuario = idUsuario
        self.texto = texto
        self.fechaHora = fechaHora

    def __repr__(self):
        return f"<Comentario {self.id}: Proyecto {self.idProyecto}, Tarea {self.idTarea}, Usuario {self.idUsuario}, Texto {self.texto}, FechaHora {self.fechaHora}>"
