#controladores/usuario_controlador.py
from modelos.model_usuario import Usuario
from dbconfig.database import db
from flask import jsonify, request
from sqlalchemy import text, exc
from sqlalchemy.exc import SQLAlchemyError
import MySQLdb
from flask_jwt_extended import create_access_token

#Crear nuevo usuario a traves e (post)
def crear_nuevo_usuario(p_nombre, p_email, p_contrasena):
    try:
        # Verificar si el correo electrónico ya está en uso
        sql_verificar_email = text("SELECT COUNT(*) FROM Usuarios WHERE email = :email")
        resultado = db.session.execute(sql_verificar_email, {'email': p_email}).scalar()

        if resultado > 0:
            # El correo electrónico ya está en uso
            return {'p_resultado': 'Error: El correo electrónico ya está en uso'}
        else:
            # Insertar el nuevo usuario
            sql_insertar_usuario = text("INSERT INTO Usuarios (nombre, email, contrasena) VALUES (:nombre, :email, :contrasena)")
            db.session.execute(sql_insertar_usuario, {'nombre': p_nombre, 'email': p_email, 'contrasena': p_contrasena})
            db.session.commit()

            # Usuario creado satisfactoriamente
            return {'p_resultado': 'Éxito: Usuario creado satisfactoriamente'}

    except Exception as e:
        # Manejar errores
        db.session.rollback()
        return {'error': str(e)}
#Actualizar un usuario a traves de  (POST), en (PATCH) no funciona
def actualizar_usuario(p_id, p_nuevo_nombre, p_nuevo_email, p_nueva_contrasena):
    try:
        response = []

        # Actualizar la contraseña del usuario si se proporciona
        if p_nueva_contrasena is not None:
            usuario = Usuario.query.filter_by(id=p_id).first()
            if usuario:
                usuario.contrasena = p_nueva_contrasena
                db.session.commit()
                response.append('Contraseña actualizada correctamente')
            else:
                response.append('Error: El usuario no existe o no se proporcionó una nueva contraseña')

        # Actualizar el nombre del usuario si se proporciona
        if p_nuevo_nombre is not None:
            usuario = Usuario.query.filter_by(id=p_id).first()
            if usuario:
                usuario.nombre = p_nuevo_nombre
                db.session.commit()
                response.append('Nombre de usuario actualizado correctamente')
            else:
                response.append('Error: El usuario no existe o no se proporcionó un nuevo nombre')

        # Actualizar el correo electrónico del usuario si se proporciona
        if p_nuevo_email is not None:
            usuario = Usuario.query.filter_by(email=p_nuevo_email).first()
            if usuario and usuario.id != p_id:
                response.append('Error: El nuevo correo electrónico ya está en uso por otro usuario')
            else:
                usuario = Usuario.query.filter_by(id=p_id).first()
                if usuario:
                    usuario.email = p_nuevo_email
                    db.session.commit()
                    response.append('Correo electrónico actualizado correctamente')
                else:
                    response.append('Error: El usuario no existe o no se proporcionó un nuevo correo electrónico')

        return response

    except Exception as e:
        # Manejar errores
        db.session.rollback()
        return str(e)  
#Eliminar  usuario   
def eliminar_usuario(id_usuario):
    try:
        # Verificar si el usuario existe
        usuario = Usuario.query.filter_by(id=id_usuario).first()

        if usuario:
            # Eliminar el usuario
            db.session.delete(usuario)
            db.session.commit()
            return {'resultado': 'Éxito: Usuario eliminado correctamente'}, 200
        else:
            return {'error': 'Error: El usuario no existe'}, 404

    except Exception as e:
        db.session.rollback()
        return {'error': f'Error al eliminar el usuario: {str(e)}'}, 500
#Mostrar detalles del usuario tipo GET
def obtener_detalles_usuario(p_id):
    try:
        # Llamar al procedimiento almacenado
        db.session.execute(
            text("CALL ObtenerDetallesUsuario(:p_id, @p_nombre, @p_email, @p_resultado)"),
            {'p_id': p_id}
        )
        # Obtener los valores de los parámetros OUT
        p_nombre = db.session.execute(text("SELECT @p_nombre")).scalar()
        p_email = db.session.execute(text("SELECT @p_email")).scalar()
        p_resultado = db.session.execute(text("SELECT @p_resultado")).scalar()

        if "Éxito" in p_resultado:
            return {'nombre': p_nombre, 'email': p_email}
        else:
            return {'error': p_resultado}

    except Exception as e:
        return {'error': str(e)}
 #login
# login usuario
def login_usuario(email, contrasena):
    try:
        # Buscar al usuario por email en la base de datos
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            # Verificar la contraseña en texto plano (en un entorno real, se debe usar hashing)
            if usuario.contrasena == contrasena:
                # Generar un token JWT válido por 24 horas
                access_token = create_access_token(identity=str(usuario.id), expires_delta=False)
                return {
                    'access_token': access_token,
                    'user_id': usuario.id,
                    'user_name': usuario.nombre,
                    'message': 'Login exitoso'
                }
            else:
                return {
                    'message': 'Credenciales inválidas'
                }
        else:
            return {
                'message': 'Credenciales inválidas'
            }

    except exc.SQLAlchemyError as e:
        return {
            'message': str(e)
        }