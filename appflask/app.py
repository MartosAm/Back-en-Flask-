#app.py
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from rutas.api_rutas import api_rutas
from dbconfig.database import db
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/mark1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '18902N9XN2912NX12'

logging.basicConfig(level=logging.DEBUG)
db.init_app(app)
app.logger.info('Conexión a la base de datos establecida correctamente')

jwt = JWTManager(app)
CORS(app)
app.register_blueprint(api_rutas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
