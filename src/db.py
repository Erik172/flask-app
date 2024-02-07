from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

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
            'image_path': self.image_path
        }

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'category_id': self.category_id,
            'category_name': self.category_name
        }

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    task_text = db.Column(db.Text)
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
            'task_text': self.task_text,
            'task_status': self.task_status,
            'date_to_end': self.date_to_end
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
