from flask import request
from flask_restful import Resource
from src.db import db, User
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            users = User.query.all()
            return {'users': [user.serialize() for user in users]}
        else:
            user = User.query.get(user_id)
            if user:
                return user.serialize(), 200
            else:
                return {'message': 'Usuario no encontrado'}, 404
            
    def post(self):
        data = request.json
        try:
            user_schema = UserSchema()
            user = user_schema.load(data)
        except ValidationError as err:
            return {'message': 'Error de validación', 'errors': err.messages}, 400
        
        if User.query.filter_by(username=user['username']).first():
            return {'message': 'El usuario ya existe'}, 400
        
        new_user = User(username=user['username'], password=user['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Usuario creado con éxito'}, 201
    
    def put(self, user_id):
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return {'message': 'Usuario no encontrado'}, 404
        
        try:
            user_schema = UserSchema()
            updated_user = user_schema.load(data)
        except ValidationError as err:
            return {'message': 'Error de validación', 'errors': err.messages}, 400
        
        if User.query.filter_by(username=updated_user['username']).first():
            return {'message': 'El usuario ya existe'}, 400
        
        if updated_user['password'] == user.password:
            return {'message': 'La contraseña no puede ser la misma'}, 400
        
        if updated_user['image_path'] is not None:
            user.image_path = updated_user['image_path']
        
        user.username = updated_user['username']
        user.password = updated_user['password']
        db.session.commit()
        return {'message': 'Usuario actualizado con éxito'}, 200
    
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'Usuario no encontrado'}, 404
        
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Usuario eliminado con éxito'}, 200