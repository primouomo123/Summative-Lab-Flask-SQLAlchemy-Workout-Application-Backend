from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate, ValidationError

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.boolean, nullable=False)