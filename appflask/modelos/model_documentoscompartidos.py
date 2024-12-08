#modelos/model_documentoscompartidos.py
from dbconfig.database import db

class DocumentoCompartido(db.Model):
    __tablename__ = 'documentoscompartidos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(255), nullable=True)

    proyecto = db.relationship('Proyecto', backref='documentos_compartidos')

    def __init__(self, idProyecto, nombre, ubicacion=None):
        self.idProyecto = idProyecto
        self.nombre = nombre
        self.ubicacion = ubicacion

    def __repr__(self):
        return f"<DocumentoCompartido {self.id}: Proyecto {self.idProyecto}, Nombre {self.nombre}, Ubicación {self.ubicacion}>"
