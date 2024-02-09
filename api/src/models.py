from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.Text, default='https://icons8.com/icon/ABBSjQJK83zf/user')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'image_path': self.image_path,
            'created_at': datetime.strftime(self.created_at, '%Y-%m-%d %H:%M:%S')
        }
    
    def check_password(self, password):
        print(self.password, password)
        return self.password == password
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)
    category_description = db.Column(db.Text, nullable=True, default=None)

    def serialize(self):
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'category_description': self.category_description
        }

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    task_title = db.Column(db.String(255), nullable=False)
    task_description = db.Column(db.Text, nullable=True, default=None)
    task_status = db.Column(db.String(20), default='Sin Empezar')
    date_to_end = db.Column(db.Date, default=None)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))

    def serialize(self):
        return {
            'task_id': self.task_id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'task_title': self.task_title,
            'task_description': self.task_description,
            'task_status': self.task_status,
            'date_to_end': self.date_to_end,
            'created_at': datetime.strftime(self.created_at, '%Y-%m-%d %H:%M:%S')
        }


# Define esquemas de serialización con Marshmallow
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task