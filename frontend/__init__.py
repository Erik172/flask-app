from flask import Flask, Blueprint
from frontend.views import frontend

# app = Flask(__name__)
frontend_bp = Blueprint('frontend', __name__)
frontend_bp.register_blueprint(frontend)