from flask import request
from flask_restful import Resource
from api.src.models import db, Task, User, Category
from marshmallow import Schema, fields, ValidationError

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

class TaskSchema(Schema):
    task_title = fields.Str(required=True)
    task_description = fields.Str(required=False, default=None, missing=None)
    task_category = fields.Str(required=True)
    task_status = fields.Str(required=False, default='Sin Empezar', missing='Sin Empezar')
    date_to_end = fields.Date(required=False, default=None, missing=None)

class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id=None):
        current_user = get_jwt_identity()
        if task_id is None:
            user_id = User.query.filter_by(username=current_user).first().user_id
            tasks = Task.query.filter_by(user_id=user_id).all()
            return [task.serialize() for task in tasks], 200
        else:
            task = Task.query.get(task_id)
            if task:
                return task.serialize(), 200
            else:
                return {'message': 'Tarea no encontrada'}, 404
            
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = request.json
        try:
            task_schema = TaskSchema()
            task = task_schema.load(data)
        except ValidationError as err:
            return {'message': 'Error de validación', 'errors': err.messages}, 400
        
        user_id = User.query.filter_by(username=current_user).first().user_id
        # si la categoría no existe, la crea
        category = Category.query.filter_by(category_name=task['task_category']).first()
        if not category:
            new_category = Category(category_name=task['task_category'])
            db.session.add(new_category)
            db.session.commit()
            category_id = new_category.category_id
        else:
            category_id = category.category_id

        new_task = Task(user_id=user_id, category_id=category_id, task_title=task['task_title'], task_description=task['task_description'], task_status=task['task_status'], date_to_end=task['date_to_end'])
        db.session.add(new_task)
        db.session.commit()

        return {'message': 'Tarea creada con éxito'}, 201
    
    @jwt_required()
    def put(self, task_id):
        current_user = get_jwt_identity()
        data = request.json
        try:
            task_schema = TaskSchema()
            task = task_schema.load(data)
        except ValidationError as err:
            return {'message': 'Error de validación', 'errors': err.messages}, 400
        
        user_id = User.query.filter_by(username=current_user).first().user_id
        task = Task.query.get(task_id)
        if task:
            if task.user_id == user_id:
                task.category_id = Category.query.filter_by(category_name=task['task_category']).first().category_id
                task.task_title = task['task_title']
                task.task_description = task['task_description']
                task.task_status = task['task_status']
                task.date_to_end = task['date_to_end']
                db.session.commit()
                return {'message': 'Tarea actualizada con éxito'}, 200
            
            else:
                return {'message': 'No tienes permisos para actualizar esta tarea'}, 401
        else:
            return {'message': 'Tarea no encontrada'}, 404
        
    @jwt_required()
    def delete(self, task_id):
        current_user = get_jwt_identity()
        user_id = User.query.filter_by(username=current_user).first().user_id
        task = Task.query.get(task_id)
        if task:
            if task.user_id == user_id:
                db.session.delete(task)
                db.session.commit()
                return {'message': 'Tarea eliminada con éxito'}, 200
            else:
                return {'message': 'No tienes permisos para eliminar esta tarea'}, 401
        else:
            return {'message': 'Tarea no encontrada'}, 404