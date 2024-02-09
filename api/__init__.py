from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from datetime import timedelta

from api.src.db import db
from api.src.resources.categories import CategoryResource
from api.src.resources.users import UserResource
from api.src.resources.login import Login
from api.src.resources.tasks import TaskResource

from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret' # Cambiar por un valor secreto
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
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
api.add_resource(TaskResource, '/tasks', '/tasks/<int:task_id>')

if __name__ == '__main__':
    app.run(debug=True)