from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields, validate, ValidationError

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


# Join table for many-to-many relationship between Workout and Exercise
class WorkoutExercises(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=True)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # Relationship between Excercise and WorkoutExcercises
    workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise', cascade='all, delete-orphan')
    
    # Association Proxy to access workouts directly from Exercise through WorkoutExercises
    workouts = association_proxy('workout_exercises', 'workout',
                                 creator=lambda workouts_object: WorkoutExercises(workouts=workouts_object))

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(255))