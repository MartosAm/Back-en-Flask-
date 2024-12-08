#controladores/comentarios_controlador.py
from dbconfig.database import db
from modelos.model_comentarios import Comentario
from modelos.model_proyecto import Proyecto
from modelos.model_usuario import Usuario
from modelos.model_tarea import Tarea
from sqlalchemy import text
#Agregar copmentario
def agregar_comentario(idProyecto, idTarea, idUsuario, texto, fechaHora):
    try:
        # Verificar si el proyecto y la tarea existen
        proyecto_existente = Proyecto.query.filter_by(id=idProyecto).first()
        tarea_existente = Tarea.query.filter_by(id=idTarea).first()

        if proyecto_existente or tarea_existente:
            # Verificar si el usuario existe
            usuario_existente = Usuario.query.filter_by(id=idUsuario).first()

            if usuario_existente:
                # Agregar el comentario al proyecto o tarea
                nuevo_comentario = Comentario(idProyecto=idProyecto, idTarea=idTarea, idUsuario=idUsuario, texto=texto, fechaHora=fechaHora)
                db.session.add(nuevo_comentario)
                db.session.commit()
                return {'p_resultado': 'Éxito: Comentario agregado satisfactoriamente'}
            else:
                return {'p_resultado': 'Error: El usuario especificado no existe'}
        else:
            return {'p_resultado': 'Error: El proyecto o la tarea especificada no existe'}

    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}
#Eliminar comentario
def eliminar_comentario(id_comentario):
    try:
        # Verificar si el comentario existe
        comentario_existente = Comentario.query.filter_by(id=id_comentario).first()

        if comentario_existente:
            # Eliminar el comentario
            db.session.delete(comentario_existente)
            db.session.commit()
            return {'p_resultado': 'Éxito: Comentario eliminado correctamente'}
        else:
            return {'p_resultado': 'Error: El comentario especificado no existe'}
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}
#Obtener comentarios de l proyectp
def obtener_comentarios_proyecto_tarea(p_idProyecto, p_idTarea):
    try:
        # Llamar al procedimiento almacenado en MySQL para obtener los comentarios
        sql = text("CALL ObtenerComentarios(:p_idProyecto, :p_idTarea, @p_resultado)")
        resultado = db.session.execute(sql, {'p_idProyecto': p_idProyecto, 'p_idTarea': p_idTarea}).fetchall()

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Obtener el resultado del procedimiento almacenado
        resultado_text = db.session.execute(text("SELECT @p_resultado")).fetchone()
        p_resultado = resultado_text[0]

        if resultado:
            comentarios = []
            for comentario in resultado:
                comentario_info = {
                    'id': comentario[0],
                    'idProyecto': comentario[1],
                    'idTarea': comentario[2],
                    'idUsuario': comentario[3],
                    'texto': comentario[4],
                    'fechaHora': comentario[5].strftime('%Y-%m-%d %H:%M:%S')
                }
                comentarios.append(comentario_info)
            
            return {'comentarios': comentarios, 'resultado': p_resultado}
        else:
            return {'error': p_resultado}

    except Exception as e:
        # Revertir cualquier cambio en caso de error
        db.session.rollback()
        return {'error': str(e)}