from dbconfig.database import db

class Proyecto(db.Model):
    __tablename__ = 'proyectos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fechaInicio = db.Column(db.Date, nullable=False)
    fechaFinPrevista = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='Activo')
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __init__(self, nombre, descripcion, fechaInicio, fechaFinPrevista, idUsuario, estado='Activo'):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self.fechaFinPrevista = fechaFinPrevista
        self.estado = estado
        self.idUsuario = idUsuario

    def __repr__(self):
        return f"<Proyecto {self.id}: {self.nombre}>"
