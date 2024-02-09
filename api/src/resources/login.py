from flask_restful import Resource
from flask import request
from api.src.models import User
from marshmallow import Schema, fields, ValidationError

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class Login(Resource):
    def post(self):
        data = request.json
        username = data.get('username', None)
        password = data.get('password', None)
        if not username or not password:
            return {'message': 'Usuario o contraseña incorrectos'}, 401

        username_db = User.query.filter_by(username=username).first()
        if not username_db or not username_db.check_password(password):
            return {'message': 'Usuario o contraseña incorrectos'}, 401
        
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200