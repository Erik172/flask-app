from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask import Flask

from api.src.models import db

from datetime import timedelta

from api import api_bp
from frontend import frontend_bp


app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/templates')
app.register_blueprint(api_bp)
app.register_blueprint(frontend_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret' # Cambiar por un valor secreto
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

Migrate(app, db)

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)