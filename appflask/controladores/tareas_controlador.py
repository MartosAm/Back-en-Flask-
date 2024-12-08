#controladores/tareas_controlador.py
from flask import Blueprint, request, jsonify
from modelos.model_tarea import Tarea
from dbconfig.database import db
from sqlalchemy import text

#Obtener detalles de la tarea
def obtener_todas_tareas_proyecto(idProyecto):
    try:
        
        # Llamar al procedimiento almacenado en MySQL para obtener todas las tareas de un proyecto
        sql = text("SELECT id, idProyecto, nombre, descripcion, fechaInicio, fechaFinPrevista, estado FROM Tareas WHERE idProyecto = :idProyecto")
        resultado = db.session.execute(sql, {'idProyecto': idProyecto}).fetchall()

        # Formatear el resultado como una lista de diccionarios
        tareas = []
        for tarea in resultado:
            tarea_detalles = {
                'id': tarea[0],
                'idProyecto': tarea[1],
                'nombre': tarea[2],
                'descripcion': tarea[3],
                'fechaInicio': tarea[4].strftime('%Y-%m-%d'),
                'fechaFinPrevista': tarea[5].strftime('%Y-%m-%d'),
                'estado': tarea[6]
            }
            tareas.append(tarea_detalles)

        return {'tareas': tareas}

    except Exception as e:
        # Revertir cualquier cambio en caso de error
        db.session.rollback()
        return {'error': str(e)}
#Obtener todas las taaaaaaaaaaaareaaaaas 
# Función para crear una nueva tarea a través del procedimiento almacenado
def crear_nueva_tarea(p_idProyecto, p_nombre, p_descripcion, p_fechaInicio, p_fechaFinPrevista):
    try:
        # Llamar al procedimiento almacenado en MySQL para crear la nueva tarea
        sql = text("CALL CrearNuevaTarea(:p_idProyecto, :p_nombre, :p_descripcion, :p_fechaInicio, :p_fechaFinPrevista, @p_idTarea, @p_resultado)")
        db.session.execute(sql, {
            'p_idProyecto': p_idProyecto,
            'p_nombre': p_nombre,
            'p_descripcion': p_descripcion,
            'p_fechaInicio': p_fechaInicio,
            'p_fechaFinPrevista': p_fechaFinPrevista
        })

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Obtener el resultado del procedimiento almacenado
        resultado = db.session.execute(text("SELECT @p_idTarea, @p_resultado")).fetchone()
        p_idTarea = resultado[0]
        p_resultado = resultado[1]

        if p_idTarea:
            # Si se creó correctamente, retornar el resultado
            return {'p_idTarea': p_idTarea, 'p_resultado': p_resultado}
        else:
            # Manejar el caso de error en la creación de la tarea
            return {'error': p_resultado}

    except Exception as e:
        # Revertir cualquier cambio en caso de error
        db.session.rollback()
        return {'error': str(e)}
#Actualizar detalles de la tarea 
def actualizar_detalles_tarea(p_idProyecto, p_idTarea, p_nombre, p_descripcion, p_fechaInicio, p_fechaFinPrevista):
    try:
        # Llamar al procedimiento almacenado en MySQL para actualizar los detalles de la tarea
        sql = text("CALL ActualizarDetallesTarea(:p_idProyecto, :p_idTarea, :p_nombre, :p_descripcion, :p_fechaInicio, :p_fechaFinPrevista, @p_resultado)")
        db.session.execute(sql, {
            'p_idProyecto': p_idProyecto,
            'p_idTarea': p_idTarea,
            'p_nombre': p_nombre,
            'p_descripcion': p_descripcion,
            'p_fechaInicio': p_fechaInicio,
            'p_fechaFinPrevista': p_fechaFinPrevista
        })

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Obtener el resultado del procedimiento almacenado
        resultado = db.session.execute(text("SELECT @p_resultado")).fetchone()
        p_resultado = resultado[0]

        return {'p_resultado': p_resultado}

    except Exception as e:
        # Revertir cualquier cambio en caso de error
        db.session.rollback()
        return {'error': str(e)}

#Eliminar Tarea
def eliminar_tarea(id_tarea):
    try:
        # Verificar si la tarea existe
        tarea = Tarea.query.filter_by(id=id_tarea).first()

        if tarea:
            # Eliminar la tarea
            db.session.delete(tarea)
            db.session.commit()
            return {'resultado': 'Éxito: Tarea eliminada correctamente'}, 200
        else:
            return {'error': 'Error: La tarea especificada no existe'}, 404

    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al eliminar la tarea: {str(e)}'}, 500
