from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from src.db import db
from src.resources.categories import CategoryResource

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Migrate(app, db)

db.init_app(app)

api.add_resource(CategoryResource, '/categories', '/categories/<int:category_id>')

if __name__ == '__main__':
    app.run(debug=True)
