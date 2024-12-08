#controladores/colaborador_controlador.py
from flask import jsonify
from dbconfig.database import db
from modelos.model_colaboradores import Colaborador
from sqlalchemy import text
from modelos.model_proyecto import Proyecto
from modelos.model_usuario import Usuario
#Eliminar controlador
def eliminar_colaborador(id_proyecto, id_usuario):
#obtener 
    try:
        # Verificar si el colaborador existe en el proyecto
        colaborador = Colaborador.query.filter_by(idProyecto=id_proyecto, idUsuario=id_usuario).first()

        if not colaborador:
            return {'error': 'El usuario no es colaborador del proyecto'}, 404

        # Eliminar el usuario como colaborador del proyecto
        db.session.delete(colaborador)
        db.session.commit()

        return {'resultado': 'Éxito: Usuario eliminado como colaborador del proyecto'}, 200

    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al eliminar al usuario como colaborador del proyecto: {str(e)}'}, 500
#OBTENER DETALLES PROYECTO
def obtener_colaboradores_proyecto(id_proyecto):
    try:
        # Llamar al procedimiento almacenado para obtener los colaboradores del proyecto
        resultado = db.session.execute(text("CALL ObtenerColaboradoresProyecto(:p_idProyecto, @p_resultado)"),
                                        {"p_idProyecto": id_proyecto})
        
        # Extraer los resultados
        colaboradores = resultado.fetchall()
        
        # Serializar los resultados en un formato JSON
        colaboradores_json = []
        for colaborador in colaboradores:
            colaborador_json = {
                'id': colaborador[0],
                'idUsuario': colaborador[1],
                'nombreUsuario': colaborador[2],
                'rol': colaborador[3]
            }
            colaboradores_json.append(colaborador_json)
    
        return {'colaboradores': colaboradores_json}, 200

    except Exception as e:
        return {'error': str(e)}, 500
# 
"""

def agregar_colaborador(p_idProyecto, p_idUsuario, p_rol):
    try:
        # Verificar si el proyecto y el usuario existen
        proyecto_existente = Proyecto.query.filter_by(id=p_idProyecto).first()
        usuario_existente = Usuario.query.filter_by(id=p_idUsuario).first()

        if proyecto_existente and usuario_existente:
            # Verificar si el usuario ya es colaborador del proyecto
            colaborador_existente = Colaborador.query.filter_by(idProyecto=p_idProyecto, idUsuario=p_idUsuario).first()

            if not colaborador_existente:
                # Agregar el usuario como colaborador al proyecto
                nuevo_colaborador = Colaborador(idProyecto=p_idProyecto, idUsuario=p_idUsuario, rol=p_rol)
                db.session.add(nuevo_colaborador)
                db.session.commit()
                return {'resultado': 'Éxito: Usuario agregado como colaborador al proyecto'}
            else:
                return {'error': 'Error: El usuario ya es colaborador del proyecto'}
        else:
            return {'error': 'Error: El proyecto o el usuario especificado no existen'}

    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}   
    
"""

    
 