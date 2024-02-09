from flask import request
from flask_restful import Resource
from api.src.db import db, Category
from marshmallow import Schema, fields, ValidationError

# Define un esquema de Marshmallow para la validación de entrada
class CategorySchema(Schema):
    category_name = fields.Str(required=True)
    category_description = fields.Str(required=False, default=None, missing=None)

class CategoryResource(Resource):
    def get(self, category_id=None):
        if category_id is None:
            # Obtener todas las categorías
            categories = Category.query.all()
            return {'categories': [category.serialize() for category in categories]}
        else:
            # Obtener una categoría por su ID
            category = Category.query.get(category_id)
            if category:
                return category.serialize(), 200
            else:
                return {'message': 'Categoria no encontrada'}, 404

    def post(self):
        data = request.json
        try:
            category_schema = CategorySchema()
            category = category_schema.load(data)
        except ValidationError as err:
            return {'message': 'Error de validación', 'errors': err.messages}, 400
        
        if Category.query.filter_by(category_name=category['category_name']).first():
            return {'message': 'La categoría ya existe'}, 400
        
        new_category = Category(category_name=category['category_name'], category_description=category['category_description'])
        db.session.add(new_category)
        db.session.commit()
        return {'message': 'Categoría creada con éxito'}, 201

    def put(self, category_id):
        data = request.json
        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Categoría no encontrada'}, 404
        
        try:
            category_schema = CategorySchema()
            updated_category = category_schema.load(data)
        except ValidationError as err:
            return {'message': 'Error de validación', 'errors': err.messages}, 400
        
        if Category.query.filter_by(category_name=updated_category['category_name']).first():
            return {'message': 'La categoría ya existe'}, 400
        
        category.category_name = updated_category['category_name']
        category.category_description = updated_category['category_description']
        db.session.commit()
        return {'message': 'Categoría actualizada con éxito'}, 200

    def delete(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Categoría no encontrada'}, 404
        
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Categoría eliminada con éxito'}, 200

