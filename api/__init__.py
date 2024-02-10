from flask import Blueprint
from flask_restful import Api

from api.src.resources.categories import CategoryResource
from api.src.resources.users import UserResource
from api.src.resources.login import Login
from api.src.resources.tasks import TaskResource

# app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Login, '/api/login')
api.add_resource(CategoryResource, '/api/categories', '/api/categories/<int:category_id>')
api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
api.add_resource(TaskResource, '/api/tasks', '/api/tasks/<int:task_id>')