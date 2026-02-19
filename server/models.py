from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
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
    duration_seconds = db.Column(db.Integer, nullable=False)

    # Table-level constraints to ensure data integrity
    __table_args__ = (
        CheckConstraint('reps > 0', name='check_reps_positive'),
        CheckConstraint('sets > 0', name='check_sets_positive'),
        CheckConstraint('duration_seconds >= 0', name='check_duration_non_negative'),
    )

    # Relationship between WorkoutExercises and Exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Relationship between WorkoutExercises and Workout
    workout = db.relationship('Workout', back_populates='workout_exercises')

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # Table-level constraints to ensure data integrity
    __table_args__ = (
        CheckConstraint('length(name) > 0 and length(name) <= 100', name='check_name_length'),
        CheckConstraint("category IN ('Cardio', 'Strength', 'Flexibility', 'Balance')", name='check_category_valid'),
    )

    # Relationship between Exercise and WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise', cascade='all, delete-orphan')
    
    # Association Proxy to access workouts directly from Exercise through WorkoutExercises
    workouts = association_proxy('workout_exercises', 'workout',
                                 creator=lambda workout_object: WorkoutExercises(workout=workout_object))

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(255), nullable=False)

    # Table-level constraints to ensure data integrity
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
        CheckConstraint('length(notes) > 0 and length(notes) <= 255', name='check_notes_length'),
    )

    # Relationship between Workout and WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercises', back_populates='workout', cascade='all, delete-orphan')

    # Association Proxy to access exercises directly from Workout through WorkoutExercises
    exercises = association_proxy('workout_exercises', 'exercise',
                                 creator=lambda exercise_object: WorkoutExercises(exercise=exercise_object))