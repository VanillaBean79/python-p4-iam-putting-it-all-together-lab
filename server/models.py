from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String
from config import db, bcrypt



class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_only = ('id', 'username', 'recipes')
    serialize_rules = 0
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', back_populates='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')


    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'

    


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    serialize_only = ('id', 'title', 'instructions', 'minutes_to_complete')
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=True)

    # # Foreign key to the 'users' table (one-to-many relationship)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # # Relationship to the User model (many recipes belong to one user)
    user = db.relationship('User', back_populates='recipes')

    @validates('instructions')
    def validate_instructions(self, key, value):
        if len(value) < 50:
            raise ValueError('Instructions must be at least 50 characters long.')
        return value
    
    
    def __repr__(self):
        return f'<Recipe {self.title}, ID: {self.id}>'
    


