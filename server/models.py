from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate, ValidationError

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)