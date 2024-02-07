from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from datetime import timedelta

from src.db import db
from src.resources.categories import CategoryResource
from src.resources.users import UserResource
from src.resources.login import Login

from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret' # Cambiar por un valor secreto
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)
jwt = JWTManager(app)

Migrate(app, db)

db.init_app(app)
    
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {'message': f'Usuario autenticado: {current_user}'}, 200

api.add_resource(Login, '/login')
api.add_resource(CategoryResource, '/categories', '/categories/<int:category_id>')
api.add_resource(UserResource, '/users', '/users/<int:user_id>')

#TODO: Agregar recursos para User, Task y Login

if __name__ == '__main__':
    app.run(debug=True)
