#modelos/model_tarea.py
from dbconfig.database import db
from modelos.model_proyecto import Proyecto  

class Tarea(db.Model):
    __tablename__ = 'tareas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #importar llave foranea de model_proyecto 
    idProyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fechaInicio = db.Column(db.Date, nullable=False)
    fechaFinPrevista = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(50), nullable=False)

    def __init__(self, idProyecto, nombre, descripcion, fechaInicio, fechaFinPrevista, estado):
        self.idProyecto = idProyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self.fechaFinPrevista = fechaFinPrevista
        self.estado = estado

    def __repr__(self):
        return f"<Tarea {self.id}: {self.nombre}>"
