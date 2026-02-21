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

## Notes
- All endpoints require and return JSON data.
- Database constraints and validations ensure data integrity.
- Marshmallow schemas are used for serialization and validation.

