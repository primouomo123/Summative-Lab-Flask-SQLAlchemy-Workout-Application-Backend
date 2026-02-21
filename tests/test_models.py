import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from server.models import db, Exercise, Workout, WorkoutExercises
from flask import Flask
import datetime

@pytest.fixture(scope="module")
def test_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="function")
def session(test_app):
    with test_app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()

# Model creation tests
def test_exercise_creation(session):
    ex = Exercise(name="Push Up", category="Strength", equipment_needed=False)
    session.add(ex)
    session.commit()
    assert ex.id is not None

def test_workout_creation(session):
    w = Workout(date=datetime.date.today(), duration_minutes=30, notes="Morning workout")
    session.add(w)
    session.commit()
    assert w.id is not None

def test_workoutexercises_creation(session):
    ex = Exercise(name="Squat1", category="Strength", equipment_needed=False)
    w = Workout(date=datetime.date.today(), duration_minutes=20, notes="Test")
    session.add_all([ex, w])
    session.commit()
    we = WorkoutExercises(workout_id=w.id, exercise_id=ex.id, reps=10, sets=2, duration_seconds=60)
    session.add(we)
    session.commit()
    assert we.id is not None

# Table constraint tests
def test_invalid_reps(session):
    ex = Exercise(name="Jump1", category="Strength", equipment_needed=False)
    w = Workout(date=datetime.date.today(), duration_minutes=10, notes="Test")
    session.add_all([ex, w])
    session.commit()
    with pytest.raises(Exception):
        we = WorkoutExercises(workout_id=w.id, exercise_id=ex.id, reps=0, sets=1, duration_seconds=10)
        session.add(we)
        session.commit()

def test_invalid_sets(session):
    ex = Exercise(name="Jump2", category="Strength", equipment_needed=False)
    w = Workout(date=datetime.date.today(), duration_minutes=10, notes="Test")
    session.add_all([ex, w])
    session.commit()
    with pytest.raises(Exception):
        we = WorkoutExercises(workout_id=w.id, exercise_id=ex.id, reps=1, sets=0, duration_seconds=10)
        session.add(we)
        session.commit()

def test_invalid_duration(session):
    ex = Exercise(name="Jump3", category="Strength", equipment_needed=False)
    w = Workout(date=datetime.date.today(), duration_minutes=10, notes="Test")
    session.add_all([ex, w])
    session.commit()
    with pytest.raises(Exception):
        we = WorkoutExercises(workout_id=w.id, exercise_id=ex.id, reps=1, sets=1, duration_seconds=-1)
        session.add(we)
        session.commit()

# Model validation tests
def test_empty_exercise_name(session):
    with pytest.raises(Exception):
        ex = Exercise(name="", category="Strength", equipment_needed=False)
        session.add(ex)
        session.commit()

def test_invalid_category(session):
    with pytest.raises(Exception):
        ex = Exercise(name="TestInvalid", category="Invalid", equipment_needed=False)
        session.add(ex)
        session.commit()

def test_future_workout_date(session):
    future_date = datetime.date.today() + datetime.timedelta(days=1)
    with pytest.raises(Exception):
        w = Workout(date=future_date, duration_minutes=10, notes="Test")
        session.add(w)
        session.commit()

def test_long_notes(session):
    long_note = "a" * 300
    with pytest.raises(Exception):
        w = Workout(date=datetime.date.today(), duration_minutes=10, notes=long_note)
        session.add(w)
        session.commit()
