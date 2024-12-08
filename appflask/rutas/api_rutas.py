#rutas/api_rutas.py
from dbconfig.database import db
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

#Importamos las funciones de los controladores

from controladores.colaborador_controlador import eliminar_colaborador, obtener_colaboradores_proyecto
from controladores.comentarios_controlador import agregar_comentario, eliminar_comentario,obtener_comentarios_proyecto_tarea
from controladores.usuario_controlador import  crear_nuevo_usuario,actualizar_usuario,eliminar_usuario, obtener_detalles_usuario, login_usuario
from controladores.proyecto_controlador import crear_nuevo_proyecto, agregar_colaborador, eliminar_proyecto, actualizar_detalles_proyecto, obtener_proyectos
from controladores.documentosCompartiods_controlador import crear_nuevo_documento_compartido, eliminar_documento_compartido,obtener_documentos_compartidos_proyecto
from controladores.tareas_controlador import eliminar_tarea, crear_nueva_tarea,actualizar_detalles_tarea,obtener_todas_tareas_proyecto

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

api_rutas = Blueprint('api_rutas', __name__)

#_____________________________________________________________METODOS POST___________________________________________________________________ 

# para crear un nuevo documento compartido
@api_rutas.route('/api/documentos-compartidos/crear', methods=['POST'])
def crear_documento_compartido():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.json

        # Extraer los datos del JSON
        p_idProyecto = data.get('p_idProyecto')
        p_nombre = data.get('p_nombre')
        p_ubicacion = data.get('p_ubicacion')

        # Llamar a la función del controlador para crear un nuevo documento compartido
        resultado = crear_nuevo_documento_compartido(p_idProyecto, p_nombre, p_ubicacion)

        # Verificar el resultado y enviar la respuesta adecuada
        if 'error' in resultado:
            # Si hay un error, enviar una respuesta de error con el código 500
            return jsonify({'error': resultado['error']}), 500
        else:
            # Si se crea el documento compartido correctamente, enviar una respuesta de éxito con el código 201
            return jsonify(resultado), 201

    except Exception as e:
        # Manejar errores
        return jsonify({'error': str(e)}), 500
# Ruta para crear un nuevo usuario (POST)
@api_rutas.route('/usuarios', methods=['POST'])
def crear_usuario():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.json
        p_nombre = data.get("nombre")
        p_email = data.get("email")
        p_contrasena = data.get("contrasena")
        
        # Llamar a la función del controlador para crear un nuevo usuario
        resultado = crear_nuevo_usuario(p_nombre, p_email, p_contrasena)

        # Verificar el resultado y enviar la respuesta adecuada
        if 'error' in resultado:
            # Si hay un error, enviar una respuesta de error con el código 500
            return jsonify({'error': resultado['error']}), 500
        else:
            # Si se crea el usuario correctamente, enviar una respuesta de éxito con el código 201
            return jsonify({'p_resultado': resultado['p_resultado']}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500    
# Método POST para crear una nueva tarea
# Ruta para crear una nueva tarea a través del procedimiento almacenado
@api_rutas.route('/tareas', methods=['POST'])
@jwt_required()
def crear_tarea():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.json
        p_idProyecto = data.get('p_idProyecto')
        p_nombre = data.get('p_nombre')
        p_descripcion = data.get('p_descripcion')
        p_fechaInicio = data.get('p_fechaInicio')
        p_fechaFinPrevista = data.get('p_fechaFinPrevista')

        # Llamar al controlador para crear una nueva tarea
        resultado = crear_nueva_tarea(p_idProyecto, p_nombre, p_descripcion, p_fechaInicio, p_fechaFinPrevista)

        # Verificar el resultado y enviar la respuesta adecuada
        if 'error' in resultado:
            return jsonify({'error': resultado['error']}), 500
        else:
            return jsonify(resultado), 201  # Código 201: Created

    except Exception as e:
        return jsonify({'error': str(e)}), 500
""""
@api_rutas.route('/tareas/crear', methods=['POST'])
def crear_tarea():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.json

        # Extraer los datos del JSON
        p_idProyecto = data.get('p_idProyecto')
        p_nombre = data.get('p_nombre')
        p_descripcion = data.get('p_descripcion')
        p_fechaInicio = data.get('p_fechaInicio')
        p_fechaFinPrevista = data.get('p_fechaFinPrevista')

        # Llamar a la función del controlador para crear una nueva tarea
        resultado = crear_nueva_tarea(p_idProyecto, p_nombre, p_descripcion, p_fechaInicio, p_fechaFinPrevista)

        # Verificar el resultado y enviar la respuesta adecuada
        if 'error' in resultado:
            # Si hay un error, enviar una respuesta de error con el código 500
            return jsonify({'error': resultado['error']}), 500
        else:
            # Si se crea la tarea correctamente, enviar una respuesta de éxito con el código 201
            return jsonify(resultado), 201

    except Exception as e:
        # Manejar errores
        return jsonify({'error': str(e)}), 500
        """

# Método POST para CrearNuevoProyecto
# Método POST para CrearNuevoProyecto
# Método POST para CrearNuevoProyecto
# Método POST para CrearNuevoProyecto
@api_rutas.route('/proyectos', methods=['POST'])
@jwt_required()
def crear_proyecto():
    try:
        # Obtener el payload del JWT y extraer el ID del usuario
        identity = get_jwt_identity()
        if not isinstance(identity, str):
            raise ValueError("El payload del JWT no contiene un identificador válido")

        id_usuario = int(identity)

        # Obtener datos del cuerpo de la solicitud
        data = request.json
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin_prevista = data.get('fecha_fin_prevista')

        # Validar que las fechas no sean None o vacías
        if not fecha_inicio or not fecha_fin_prevista:
            return jsonify({'error': 'Las fechas son requeridas'}), 400

        # Validar formato de fechas
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin_prevista = datetime.strptime(fecha_fin_prevista, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Se esperaba: YYYY-MM-DD'}), 400

        # Llamar al controlador para crear un nuevo proyecto
        resultado = crear_nuevo_proyecto(id_usuario, nombre, descripcion, fecha_inicio, fecha_fin_prevista)

        # Verificar el resultado y enviar la respuesta adecuada
        if 'error' in resultado:
            return jsonify({'error': resultado['error']}), 500
        else:
            return jsonify(resultado), 201  # Código 201: Created

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500




    #AGREGAR POST
    
    # Ruta para agregar un colaborador a un proyecto
#metodo POST para agregar colaboradores
@api_rutas.route('/colaboradores/agregar', methods=['POST'])
def agregar_colaborador_ruta():
    data = request.json
    p_idProyecto = data.get('idProyecto')
    p_idUsuario = data.get('idUsuario')
    p_rol = data.get('rol')
    
    resultado = agregar_colaborador(p_idProyecto, p_idUsuario, p_rol)
    
    if 'error' in resultado:
        return jsonify({'error': resultado['error']}), 500
    else:
        return jsonify(resultado), 201         
# Ruta para actualizar los campos de un usuario de manera flexible (POST)
@api_rutas.route('/actualizar-usuario', methods=['POST'])
@jwt_required()  # Requiere autenticación JWT
def actualizar_usuario_ruta():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.json
        p_id = data.get('p_id')
        p_nuevo_nombre = data.get('p_nuevo_nombre')
        p_nuevo_email = data.get('p_nuevo_email')
        p_nueva_contrasena = data.get('p_nueva_contrasena')

        # Llamar a la función del controlador para actualizar el usuario
        resultado = actualizar_usuario(p_id, p_nuevo_nombre, p_nuevo_email, p_nueva_contrasena)

        return jsonify({'mensaje': resultado}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Ruta para agregar un comentario a un proyecto o tarea (POST)
@api_rutas.route('/comentarios/agregar', methods=['POST'])
def agregar_comentario_ruta():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.json
        p_idProyecto = data.get('idProyecto')
        p_idTarea = data.get('idTarea')
        p_idUsuario = data.get('idUsuario')
        p_texto = data.get('texto')
        p_fechaHora = data.get('fechaHora')

        # Llamar a la función del controlador para agregar el comentario
        resultado = agregar_comentario(p_idProyecto, p_idTarea, p_idUsuario, p_texto, p_fechaHora)

        # Verificar el resultado y enviar la respuesta adecuada
        if 'error' in resultado:
            # Si hay un error, enviar una respuesta de error con el código 500
            return jsonify({'error': resultado['error']}), 500
        else:
            # Si se agrega el comentario correctamente, enviar una respuesta de éxito con el código 201
            return jsonify(resultado), 201

    except Exception as e:
        # Manejar errores
        return jsonify({'error': str(e)}), 500
#LOGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGIN
# Ruta para el inicio de sesión
@api_rutas.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        contrasena = data.get('contrasena')

        resultado_login = login_usuario(email, contrasena)

        if 'access_token' in resultado_login:
            return jsonify({
                'status': 'success',
                'access_token': resultado_login['access_token'],
                'data': {
                    'user_id': resultado_login['user_id'],
                    'user_name': resultado_login['user_name']
                }
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': resultado_login['message'] if 'message' in resultado_login else 'Credenciales inválidas'
            }), 401

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


#______________________________________METODO PUT_____________________________________________________________________________________
# Ruta para actualizar los detalles de un proyecto (PUT)
@api_rutas.route('/detalles-proyecto/actualizar', methods=['PUT'])
@jwt_required()
def actualizar_detalles_proyecto_ruta():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.json
        p_idProyecto = data.get('idProyecto')
        p_nombre = data.get('nombre')
        p_descripcion = data.get('descripcion')
        p_fechaInicio = data.get('fechaInicio')
        p_fechaFinPrevista = data.get('fechaFinPrevista')

        # Llamar al controlador para actualizar los detalles del proyecto
        resultado = actualizar_detalles_proyecto(p_idProyecto, p_nombre, p_descripcion, p_fechaInicio, p_fechaFinPrevista)

        # Verificar resultado y enviar respuesta adecuada
        if 'error' in resultado:
            return jsonify({'error': resultado['error']}), 500
        else:
            return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
#Ruta pa actualizar los detalles de la tarea apoco no
@api_rutas.route('/tareas/<int:p_idProyecto>/<int:p_idTarea>', methods=['PUT'])
def actualizar_tarea(p_idProyecto, p_idTarea):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.json
        p_nombre = data.get('p_nombre')
        p_descripcion = data.get('p_descripcion')
        p_fechaInicio = data.get('p_fechaInicio')
        p_fechaFinPrevista = data.get('p_fechaFinPrevista')

        # Llamar al controlador para actualizar los detalles de la tarea
        resultado = actualizar_detalles_tarea(p_idProyecto, p_idTarea, p_nombre, p_descripcion, p_fechaInicio, p_fechaFinPrevista)

        # Verificar el resultado y enviar la respuesta adecuada
        if 'error' in resultado:
            return jsonify({'error': resultado['error']}), 500
        else:
            return jsonify(resultado), 201  # Código 201 o 200: OK

    except Exception as e:
        return jsonify({'error': str(e)}), 500
         
#mas metodos
#_______________________________________________METODOS PATCH_________________________________________________________________________________ 
# METODOS Get
# Ruta para obtener los colaboradores de un proyecto (GET)
# Ruta para obtener los colaboradores de un proyecto
@api_rutas.route('/colaboradores/<int:id_proyecto>', methods=['GET'])
def obtener_colaboradores_ruta(id_proyecto):
    try:
        resultado, status_code = obtener_colaboradores_proyecto(id_proyecto)
        return jsonify(resultado), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
#Obtener detalles del proyecto
# Ruta para obtener proyectos del usuario autenticado
# Métodos GET
# Métodos GET
@api_rutas.route('/proyectos', methods=['GET'])
def obtener_proyectos_ruta():
    return obtener_proyectos()


@api_rutas.route('/tareas', methods=['GET'])
@jwt_required()
def obtener_todas_tareas():
    try:
        idProyecto = request.args.get('idProyecto')
        print(f"ID de Proyecto recibido: {idProyecto}")  # Imprime el ID de proyecto para debug

        if not idProyecto:
            return jsonify({'error': 'Falta el parámetro idProyecto'}), 400

        resultado = obtener_todas_tareas_proyecto(idProyecto)

        if 'error' in resultado:
            return jsonify({'error': resultado['error']}), 404
        else:
            return jsonify(resultado['tareas']), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
#Ruta para jalar todas las tareas de un proyecto
# Ruta para obtener todas las tareas

#Obtene rdocumentos compartidos
@api_rutas.route('/proyecto/documentoCompartidos/<int:id_proyecto>', methods=['GET'])
def obtener_documentos_compartidos(id_proyecto):
    resultado = obtener_documentos_compartidos_proyecto(id_proyecto)

    if 'error' in resultado:
        return jsonify({'error': resultado['error']}), 404
    else:
        return jsonify(resultado), 200
@api_rutas.route('/proyecto/comentarios/<int:id_proyecto>/tarea/<int:id_tarea>', methods=['GET'])
def obtener_comentarios(id_proyecto, id_tarea):
    resultado = obtener_comentarios_proyecto_tarea(id_proyecto, id_tarea)

    if 'error' in resultado:
        return jsonify({'error': resultado['error']}), 404
    else:
        return jsonify(resultado), 200
#Obtener todos las tareas del os proyectos
@api_rutas.route('/proyecto/tareas/<int:id_proyecto>', methods=['GET'])
def obtener_tareas_proyecto(id_proyecto):
    resultado = obtener_todas_tareas_proyecto(id_proyecto)
    if 'error' in resultado:
        return jsonify({'error': resultado['error']}), 404
    else:
        return jsonify(resultado), 200
#Obtener usuarios
@api_rutas.route('/usuario/detalles', methods=['GET'])
@jwt_required()
def obtener_detalles_usuario_ruta():
    usuario_id = get_jwt_identity()
    resultado = obtener_detalles_usuario(usuario_id)
    if 'error' in resultado:
        return jsonify({'error': resultado['error']}), 404
    else:
        return jsonify(resultado), 200

#________________________________________________________________________________________________________________________________ 
#_____________________________________________________METODOS DELETE___________________________________________________________________________ 
# Ruta para eliminar a un colaborador de un proyecto
@api_rutas.route('/colaboradores/<int:id_proyecto>/<int:id_usuario>', methods=['DELETE'])
def eliminar_colaborador_api(id_proyecto, id_usuario):
    try:
        # Llamar a la función del controlador para eliminar al colaborador
        resultado, status_code = eliminar_colaborador(id_proyecto, id_usuario)

        # Retornar la respuesta con el código de estado apropiado
        return jsonify(resultado), status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500  
# Ruta para eliminar un comentario por su ID (DELETE)
@api_rutas.route('/comentarios/<int:id_comentario>', methods=['DELETE'])
def eliminar_comentario_ruta(id_comentario):
    try:
        resultado = eliminar_comentario(id_comentario)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
#Eliminar doc compartido
# Ruta para eliminar un documento compartido (DELETE)
@api_rutas.route('/documentos-compartidos/<int:id_documento>', methods=['DELETE'])
def eliminar_documento_compartido_api(id_documento):
    try:
        # Llamar a la función del controlador para eliminar el documento compartido
        resultado = eliminar_documento_compartido(id_documento)

        # Retornar la respuesta con el código de estado adecuado
        if 'error' in resultado:
            return jsonify({'error': resultado['error']}), 500
        else:
            return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Ruta para eliminar un proyecto (DELETE)


@api_rutas.route('/proyectos/<int:id_proyecto>', methods=['DELETE'])
@jwt_required()
def eliminar_proyecto_api(id_proyecto):
    try:
        current_user_id = get_jwt_identity()

        # Llamar al controlador para eliminar el proyecto
        resultado = eliminar_proyecto(id_proyecto, current_user_id)

        # Verificar el resultado y enviar la respuesta adecuada
        if 'error' in resultado:
            return jsonify({'error': resultado['error']}), 500
        else:
            return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ruta para eliminar una tarea
@api_rutas.route('/tareas/<int:id_tarea>', methods=['DELETE'])
def eliminar_tarea_api(id_tarea):
    resultado, status_code = eliminar_tarea(id_tarea)
    return jsonify(resultado), status_code

@api_rutas.route('/eliminar-usuario', methods=['DELETE'])
@jwt_required()  # Requiere autenticación JWT para acceder a esta ruta
def eliminar_usuario_api(id_usuario):
    try:
        current_user_id = get_jwt_identity()

        # Llama a la función del controlador para eliminar usuario
        resultado, status_code = eliminar_usuario(id_usuario)

        # Comprueba si el usuario que intenta eliminar es el mismo que el autenticado
        if current_user_id == id_usuario:
            return jsonify(resultado), status_code
        else:
            return jsonify({'error': 'No tienes permiso para eliminar este usuario'}), 403

    except Exception as e:
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500