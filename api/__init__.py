from flask import Blueprint
from flask_restful import Api

from api.src.resources.categories import CategoryResource
from api.src.resources.users import UserResource
from api.src.resources.login import Login
from api.src.resources.tasks import TaskResource

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

# app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
    
@api_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {'message': f'Usuario autenticado: {current_user}'}, 200

api.add_resource(Login, '/api/login')
api.add_resource(CategoryResource, '/api/categories', '/api/categories/<int:category_id>')
api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
api.add_resource(TaskResource, '/api/tasks', '/api/tasks/<int:task_id>')