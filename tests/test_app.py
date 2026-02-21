import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from server.app import app
from server.models import db
import json


@pytest.fixture(scope="module")
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

# Endpoint tests
def test_get_workouts(test_client):
    response = test_client.get('/workouts')
    assert response.status_code == 200

def test_post_workout(test_client):
    data = {
        "date": "2026-02-20",
        "duration_minutes": 30,
        "notes": "Morning workout"
    }
    response = test_client.post('/workouts', data=json.dumps(data), content_type='application/json')
    assert response.status_code in [200, 201, 422]

# Edge case: invalid workout
    data = {
        "date": "2026-02-21",
        "duration_minutes": 0,
        "notes": ""
    }
    response = test_client.post('/workouts', data=json.dumps(data), content_type='application/json')
    assert response.status_code in [400, 422]

def test_get_exercises(test_client):
    response = test_client.get('/exercises')
    assert response.status_code == 200

def test_post_exercise(test_client):
    data = {
        "name": "Push Up",
        "category": "Strength",
        "equipment_needed": False
    }
    response = test_client.post('/exercises', data=json.dumps(data), content_type='application/json')
    assert response.status_code in [200, 201, 422]

# Edge case: invalid exercise
    data = {
        "name": "",
        "category": "Invalid",
        "equipment_needed": False
    }
    response = test_client.post('/exercises', data=json.dumps(data), content_type='application/json')
    assert response.status_code in [400, 422]

def test_add_exercise_to_workout(test_client):
    # This test assumes valid workout and exercise IDs exist
    data = {
        "reps": 10,
        "sets": 2,
        "duration_seconds": 60
    }
    response = test_client.post('/workouts/1/exercises/1/workout_exercises', data=json.dumps(data), content_type='application/json')
    assert response.status_code in [200, 201, 422]

# Edge case: invalid reps
    data = {
        "reps": 0,
        "sets": 1,
        "duration_seconds": 60
    }
    response = test_client.post('/workouts/1/exercises/1/workout_exercises', data=json.dumps(data), content_type='application/json')
    assert response.status_code in [400, 422]

def test_get_single_workout(test_client):
    # Create a workout first
    data = {"date": "2026-02-22", "duration_minutes": 45, "notes": "Evening workout"}
    post_resp = test_client.post('/workouts', data=json.dumps(data), content_type='application/json')
    workout_id = post_resp.get_json().get('id', 1)
    # Get the workout
    response = test_client.get(f'/workouts/{workout_id}')
    assert response.status_code == 200
    assert response.get_json().get('id') == workout_id

def test_delete_workout(test_client):
    # Create a workout to delete
    data = {"date": "2026-02-23", "duration_minutes": 20, "notes": "Delete me"}
    post_resp = test_client.post('/workouts', data=json.dumps(data), content_type='application/json')
    workout_id = post_resp.get_json().get('id', 1)
    # Delete the workout
    response = test_client.delete(f'/workouts/{workout_id}')
    assert response.status_code == 200
    # Try to get it again
    response = test_client.get(f'/workouts/{workout_id}')
    assert response.status_code == 404

def test_get_single_exercise(test_client):
    # Create an exercise first
    data = {"name": "Sit Up", "category": "Strength", "equipment_needed": False}
    post_resp = test_client.post('/exercises', data=json.dumps(data), content_type='application/json')
    exercise_id = post_resp.get_json().get('id', 1)
    # Get the exercise
    response = test_client.get(f'/exercises/{exercise_id}')
    assert response.status_code == 200
    assert response.get_json().get('id') == exercise_id

def test_delete_exercise(test_client):
    # Create an exercise to delete
    data = {"name": "Delete Me", "category": "Strength", "equipment_needed": False}
    post_resp = test_client.post('/exercises', data=json.dumps(data), content_type='application/json')
    exercise_id = post_resp.get_json().get('id', 1)
    # Delete the exercise
    response = test_client.delete(f'/exercises/{exercise_id}')
    assert response.status_code == 200
    # Try to get it again
    response = test_client.get(f'/exercises/{exercise_id}')
    assert response.status_code == 404
