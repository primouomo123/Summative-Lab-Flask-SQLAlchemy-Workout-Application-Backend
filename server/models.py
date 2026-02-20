from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields, validate, ValidationError, RAISE

from datetime import date as dt_date

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


# Join table Model for many-to-many relationship between Workout and Exercise
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
        CheckConstraint('workout_id IN (SELECT id FROM workouts)', name='check_workout_id_valid'),
        CheckConstraint('exercise_id IN (SELECT id FROM exercises)', name='check_exercise_id_valid'),
    )

    # Model Validations to ensure data integrity at the application level
    @validates('reps', 'sets')
    def validate_reps(self, key, value):
        if not isinstance(value, int):
            raise TypeError(f'{key} must be an integer')
        if value <= 0:
            raise ValueError(f'{key} must be a positive integer')
        return value
    
    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        if not isinstance(value, int):
            raise TypeError(f'{key} must be an integer')
        if value < 0:
            raise ValueError(f'{key} must be a non-negative integer')
        return value
    
    @validates('workout_id')
    def validate_workout_id(self, key, value):
        if not isinstance(value, int):
            raise TypeError(f'{key} must be an integer')
        if not Workout.query.get(value):
            raise ValueError(f'{key} must reference an existing workout id')
        return value

    @validates('exercise_id')
    def validate_exercise_id(self, key, value):
        if not isinstance(value, int):
            raise TypeError(f'{key} must be an integer')
        if not Exercise.query.get(value):
            raise ValueError(f'{key} must reference an existing exercise id')
        return value

    # Relationship between WorkoutExercises and Exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Relationship between WorkoutExercises and Workout
    workout = db.relationship('Workout', back_populates='workout_exercises')

    def __repr__(self):
        return f'<WorkoutExercises id={self.id} workout_id={self.workout_id} exercise_id={self.exercise_id} reps={self.reps} sets={self.sets} duration_seconds={self.duration_seconds}>'


# WorkoutExercise Schema for serialization/deserialization
class WorkoutExercisesSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(required=True, validate=validate.Range(min=1))
    sets = fields.Int(required=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(required=True, validate=validate.Range(min=0))

    exercise = fields.Nested(lambda: ExerciseSchema(exclude=('workout_exercises', 'workouts')), dump_only=True)
    workout = fields.Nested(lambda: WorkoutSchema(exclude=('workout_exercises', 'exercises')), dump_only=True)

    class Meta:
        unknown = RAISE  # Raise an error if unknown fields are included in the input data
    
    # Schema Validations to ensure data integrity at the application level
    @validates('workout_id')
    def validate_workout_id(self, value):
        if not Workout.query.get(value):
            raise ValidationError(f'workout_id {value} does not reference an existing workout') 
        return value
    
    @validates('exercise_id')
    def validate_exercise_id(self, value):
        if not Exercise.query.get(value):
            raise ValidationError(f'exercise_id {value} does not reference an existing exercise') 
        return value
    
    @validates('reps')
    def validate_reps(self, value):
        if value <= 0:
            raise ValidationError('reps must be a positive integer')
        return value
    
    @validates('sets')
    def validate_sets(self, value):
        if value <= 0:
            raise ValidationError('sets must be a positive integer')
        return value
    
    @validates('duration_seconds')
    def validate_duration_seconds(self, value):
        if value < 0:
            raise ValidationError('duration_seconds must be a non-negative integer')
        return value


# Exercise Table Model
class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    categories = ('Cardio', 'Strength', 'Flexibility', 'Balance')

    # Table-level constraints to ensure data integrity
    __table_args__ = (
        CheckConstraint('length(name) > 0', name='check_name_length'),
        CheckConstraint(f'category IN ({", ".join(repr(c) for c in categories)})', name='check_category_valid'),
        CheckConstraint('equipment_needed IN (0, 1)', name='check_equipment_needed_boolean'),
    )

    # Model Validations to ensure data integrity at the application level
    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError(f'{key} must be a string')
        if len(value) == 0:
            raise ValueError(f'{key} cannot be empty')
        return value

    @validates('category')
    def validate_category(self, key, value):
        if not isinstance(value, str):
            raise TypeError(f'{key} must be a string')
        if value not in self.categories:
            raise ValueError(f'Invalid {key}: {value}, you must choose from {self.categories}')
        return value
    
    @validates('equipment_needed')
    def validate_equipment_needed(self, key, value):
        if not isinstance(value, bool):
            raise TypeError(f'{key} must be a boolean')
        return value

    # Relationship between Exercise and WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise', cascade='all, delete-orphan')
    
    # Association Proxy to access workouts directly from Exercise through WorkoutExercises
    workouts = association_proxy('workout_exercises', 'workout',
                                 creator=lambda workout_object: WorkoutExercises(workout=workout_object))
    
    def __repr__(self):
        return f'<Exercise id={self.id} name={self.name} category={self.category} equipment_needed={self.equipment_needed}>'


# Exercise Schema for serialization/deserialization
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(Exercise.categories))
    equipment_needed = fields.Bool(required=True)

    workout_exercises = fields.Nested(lambda: WorkoutExercisesSchema(exclude=('exercise',)), many=True, dump_only=True)
    workouts = fields.Nested(lambda: WorkoutSchema(exclude=('workout_exercises', 'exercises')), many=True, dump_only=True)

    class Meta:
        unknown = RAISE  # Raise an error if unknown fields are included in the input data
    
    # Schema Validations to ensure data integrity at the application level
    @validates('name')
    def validate_name(self, value):
        if len(value) == 0:
            raise ValidationError('name cannot be empty')
        return value
    
    @validates('category')
    def validate_category(self, value):
        if value not in Exercise.categories:
            raise ValidationError(f'Invalid category: {value}, you must choose from {Exercise.categories}')
        return value
    
    @validates('equipment_needed')
    def validate_equipment_needed(self, value):
        if not isinstance(value, bool):
            raise ValidationError('equipment_needed must be a boolean')
        return value



class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(255), nullable=False)

    # Table-level constraints to ensure data integrity
    __table_args__ = (
        CheckConstraint('date <= CURRENT_DATE', name='check_date_not_future'),
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
        CheckConstraint('length(notes) > 0', name='check_notes_length'),
    )

    # Model Validations to ensure data integrity at the application level
    @validates('date')
    def validate_date(self, key, value):
        if not isinstance(value, dt_date):
            raise TypeError(f'{key} must be a datetime.date object')
        if value > dt_date.today():
            raise ValueError(f'{key} cannot be in the future')
        return value
    
    @validates('duration_minutes')
    def validate_duration_minutes(self, key, value):
        if not isinstance(value, int):
            raise TypeError(f'{key} must be an integer')
        if value <= 0:
            raise ValueError(f'{key} must be a positive integer')
        return value
    
    @validates('notes')
    def validate_notes(self, key, value):
        if not isinstance(value, str):
            raise TypeError(f'{key} must be a string')
        if len(value) == 0 or len(value) > 255:
            raise ValueError(f'{key} must be between 1 and 255 characters long')
        return value

    # Relationship between Workout and WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercises', back_populates='workout', cascade='all, delete-orphan')

    # Association Proxy to access exercises directly from Workout through WorkoutExercises
    exercises = association_proxy('workout_exercises', 'exercise',
                                 creator=lambda exercise_object: WorkoutExercises(exercise=exercise_object))
    
    def __repr__(self):
        return f'<Workout id={self.id} date={self.date} duration_minutes={self.duration_minutes} notes={self.notes}>'


# Workout Schema for serialization/deserialization
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(required=True, validate=validate.Length(min=1, max=255))

    workout_exercises = fields.Nested(lambda: WorkoutExercisesSchema(exclude=('workout',)), many=True, dump_only=True)
    exercises = fields.Nested(lambda: ExerciseSchema(exclude=('workout_exercises', 'workouts')), many=True, dump_only=True)

    class Meta:
        unknown = RAISE  # Raise an error if unknown fields are included in the input data
    
    # Schema Validations to ensure data integrity at the application level
    @validates('date')
    def validate_date(self, value):
        # Ensure date is not in the future
        if value > dt_date.today():
            raise ValidationError("Workout date cannot be in the future.")
        return value
    
    @validates('duration_minutes')
    def validate_duration_minutes(self, value):
        if value <= 0:
            raise ValidationError('duration_minutes must be a positive integer')
        return value
    
    @validates('notes')
    def validate_notes(self, value):
        if len(value) == 0 or len(value) > 255:
            raise ValidationError('notes must be between 1 and 255 characters long')
        return value