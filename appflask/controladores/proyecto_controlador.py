#controladores/proyecto_controlador.py
from dbconfig.database import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from modelos.model_proyecto import Proyecto
from modelos.model_colaboradores import Colaborador
from modelos.model_usuario import Usuario
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

# Controlador para actualizar detalles del proyecto
def actualizar_detalles_proyecto(p_idProyecto, p_nombre, p_descripcion, p_fechaInicio, p_fechaFinPrevista):
    try:
        # Ejecutar procedimiento almacenado para actualizar detalles del proyecto
        with db.engine.connect() as connection:
            result = connection.execute(
                text("CALL ActualizarDetallesProyecto(:p_idProyecto, :p_nombre, :p_descripcion, :p_fechaInicio, :p_fechaFinPrevista, @p_resultado)"),
                {"p_idProyecto": p_idProyecto, "p_nombre": p_nombre, "p_descripcion": p_descripcion, "p_fechaInicio": p_fechaInicio, "p_fechaFinPrevista": p_fechaFinPrevista}
            )

            # Obtener valor del parámetro OUT
            result = connection.execute(text("SELECT @p_resultado")).fetchone()
            p_resultado = result[0]  # Asegurarse de obtener el valor correctamente

        # Devolver resultado
        return {'resultado': p_resultado}

    except Exception as e:
        # Manejar errores y hacer rollback en caso de error
        db.session.rollback()
        print(e)  # Imprimir el error completo para depurar
        return {'error': str(e)}
#Crear nuevo proyecto (POST)
# Crear nuevo proyecto (POST)

# Método para crear un nuevo proyecto utilizando el procedimiento almacenado
def crear_nuevo_proyecto(id_usuario, nombre, descripcion, fecha_inicio, fecha_fin_prevista):
    try:
        # Llamar al procedimiento almacenado en MySQL para crear el nuevo proyecto
        sql = text("CALL CrearNuevoProyecto(:nombre, :descripcion, :fecha_inicio, :fecha_fin_prevista, :id_usuario, @p_idProyecto, @p_resultado)")
        db.session.execute(sql, {
            'nombre': nombre,
            'descripcion': descripcion,
            'fecha_inicio': fecha_inicio,
            'fecha_fin_prevista': fecha_fin_prevista,
            'id_usuario': id_usuario
        })

        # Obtener el resultado del procedimiento almacenado
        resultado = db.session.execute(text("SELECT @p_idProyecto, @p_resultado")).fetchone()
        
        if resultado:
            p_idProyecto = resultado[0]
            p_resultado = resultado[1]

            if p_idProyecto == -1:
                # Manejar el caso de error en la creación del proyecto
                return {'error': p_resultado}
            else:
                # Si se creó correctamente, retornar el resultado
                return {'resultado': p_resultado}
        else:
            return {'error': 'Error al ejecutar el procedimiento almacenado'}

    except Exception as e:
        # Revertir cualquier cambio en caso de error
        db.session.rollback()
        return {'error': str(e)}


#obtener detalles del proyecto /(GET)
@jwt_required()
def obtener_proyectos():
    try:
        idUsuario = get_jwt_identity()  # Obtener el ID del usuario autenticado

        # Filtrar proyectos por el ID del usuario
        proyectos = Proyecto.query.filter_by(idUsuario=idUsuario).all()

        if not proyectos:
            return jsonify({'mensaje': 'Sin proyectos pendientes'}), 200

        proyectos_lista = [
            {
                'id': proyecto.id,
                'nombre': proyecto.nombre,
                'descripcion': proyecto.descripcion,
                'fechaInicio': proyecto.fechaInicio.strftime('%Y-%m-%d'),
                'fechaFinPrevista': proyecto.fechaFinPrevista.strftime('%Y-%m-%d'),
                'estado': proyecto.estado,
                'idUsuario': proyecto.idUsuario
            } for proyecto in proyectos
        ]

        return jsonify(proyectos_lista), 200

    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

#Agregar ua un colaborador a un proyecto (POST) 
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
                return {'p_resultado': 'Éxito: Usuario agregado como colaborador al proyecto'}
            else:
                return {'p_resultado': 'Error: El usuario ya es colaborador del proyecto'}
        else:
            return {'p_resultado': 'Error: El proyecto o el usuario especificado no existen'}

    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}
#EliniarProyectoxd   

def eliminar_proyecto(id_proyecto, id_usuario):
    try:
        # Verificar si el usuario tiene permisos sobre el proyecto
        proyecto = Proyecto.query.filter_by(id=id_proyecto, idUsuario=id_usuario).first()
        if not proyecto:
            return {'error': 'No tiene permisos para eliminar este proyecto'}, 403

        # Llamar al procedimiento almacenado para eliminar el proyecto
        sql = text("CALL EliminarProyecto(:p_idProyecto, @p_resultado)")
        db.session.execute(sql, {'p_idProyecto': id_proyecto})

        # Confirmar los cambios en la base de datos
        db.session.commit()

        # Obtener el resultado del procedimiento almacenado
        resultado = db.session.execute(text("SELECT @p_resultado")).fetchone()[0]

        # Retornar el resultado correctamente formateado
        return {'resultado': resultado}

    except SQLAlchemyError as e:
        # Revertir cualquier cambio en caso de error
        db.session.rollback()
        return {'error': str(e)}, 500

    except Exception as e:
        # Cualquier otro error
        return {'error': str(e)}, 500
    
#Obtener detalles de todos los proyectos 