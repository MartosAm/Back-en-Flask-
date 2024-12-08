from flask import jsonify
from dbconfig.database import db
from modelos.model_documentoscompartidos import DocumentoCompartido
from modelos.model_proyecto import Proyecto

#Funcion para crear el documento compartido 
def crear_nuevo_documento_compartido(p_idProyecto, p_nombre, p_ubicacion):
    try:
        # Verificar si el proyecto existe
        proyecto_existente = Proyecto.query.filter_by(id=p_idProyecto).first()

        if proyecto_existente:
            # Insertar el nuevo documento compartido
            nuevo_documento_compartido = DocumentoCompartido(
                idProyecto=p_idProyecto,
                nombre=p_nombre,
                ubicacion=p_ubicacion
            )

            db.session.add(nuevo_documento_compartido)
            db.session.commit()

            return {'p_resultado': 'Éxito: Documento compartido creado satisfactoriamente'}
        else:
            return {'p_resultado': 'Error: El proyecto especificado no existe'}

    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}
#elimnar documento compartido
def eliminar_documento_compartido(id_documento):
    try:
        # Verificar si el documento compartido existe
        documento_existente = DocumentoCompartido.query.filter_by(id=id_documento).first()

        if documento_existente:
            # Eliminar el documento compartido
            db.session.delete(documento_existente)
            db.session.commit()
            return {'p_resultado': 'Éxito: Documento compartido eliminado correctamente'}
        else:
            return {'p_resultado': 'Error: El documento compartido especificado no existe'}
        
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}
#Obtener documentos compartidops
def obtener_documentos_compartidos_proyecto(p_idProyecto):
    try:
        # Obtener la lista de todos los documentos compartidos del proyecto
        documentos = DocumentoCompartido.query.filter_by(idProyecto=p_idProyecto).all()

        if documentos:
            documentos_compartidos = [{'id': doc.id, 'nombre': doc.nombre, 'ubicacion': doc.ubicacion} for doc in documentos]
            return {'documentos_compartidos': documentos_compartidos, 'resultado': 'Éxito: Todos los documentos compartidos del proyecto obtenidos satisfactoriamente'}
        else:
            return {'error': 'Error: No se encontraron documentos compartidos para el proyecto especificado'}

    except Exception as e:
        return {'error': str(e)}