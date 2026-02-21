# Workout Tracker API

## Project Description
A Flask and SQLAlchemy-based backend for tracking workouts and exercises. The API allows you to create, view, and manage workouts, exercises, and their associations, including reps, sets, and duration. It includes database constraints, model validations, and schema validations for robust data integrity.

## Installation Instructions
1. Clone the repository:
```bash
git clone <repo-url>
cd Summative-Lab-Flask-SQLAlchemy-Workout-Application-Backend
```
2. Install dependencies using pipenv:
```bash
pipenv install
pipenv shell
```
3. Run database migrations:
```bash
server/flask db upgrade
```

or:
```bash
cd server
flask db upgrade
```

4. Seed the database with sample data:
```bash
python server/seed.py
```

or:

```bash
cd server
python seed.py
```

## Run Instructions
Start the Flask development server:
```bash
python server/app.py
```

or:
```bash
cd server
python app.py
```

The API will be available at http://localhost:5555

## API Endpoints

### Workouts
- `GET /workouts` — List all workouts
- `GET /workouts/<id>` — Show a single workout with its associated exercises (stretch: include reps/sets/duration)
- `POST /workouts` — Create a workout
- `DELETE /workouts/<id>` — Delete a workout (stretch: delete associated WorkoutExercises)

### Exercises
- `GET /exercises` — List all exercises
- `GET /exercises/<id>` — Show an exercise and associated workouts
- `POST /exercises` — Create an exercise
- `DELETE /exercises/<id>` — Delete an exercise (stretch: delete associated WorkoutExercises)

### WorkoutExercises
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` — Add an exercise to a workout, including reps/sets/duration

## Example curl Commands

### Workouts

- List all workouts:
  ```bash
  curl -X GET http://localhost:5555/workouts
  ```

- Get a single workout:
  ```bash
  curl -X GET http://localhost:5555/workouts/1
  ```

- Create a workout:
  ```bash
  curl -X POST http://localhost:5555/workouts -H "Content-Type: application/json" -d '{"date": "2026-02-20", "duration_minutes": 30, "notes": "Morning workout"}'
  ```

- Delete a workout:
  ```bash
  curl -X DELETE http://localhost:5555/workouts/3
  ```

### Exercises

- List all exercises:
  ```bash
  curl -X GET http://localhost:5555/exercises
  ```

- Get a single exercise:
  ```bash
  curl -X GET http://localhost:5555/exercises/1
  ```

- Create an exercise:
  ```bash
  curl -X POST http://localhost:5555/exercises -H "Content-Type: application/json" -d '{"name": "Leg Raise", "category": "Strength", "equipment_needed": false}'
  ```

- Delete an exercise:
  ```bash
  curl -X DELETE http://localhost:5555/exercises/5
  ```

### WorkoutExercises (Add Exercise to Workout)

- Add an exercise to a workout:
  ```bash
  curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises -H "Content-Type: application/json" -d '{"reps": 10, "sets": 2, "duration_seconds": 60}'
  ```

## Notes
- All endpoints require and return JSON data.
- Database constraints and validations ensure data integrity.
- Marshmallow schemas are used for serialization and validation.

