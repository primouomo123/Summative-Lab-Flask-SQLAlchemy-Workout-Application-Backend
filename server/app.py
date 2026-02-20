from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercises, ExerciseSchema, WorkoutSchema, WorkoutExercisesSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Home route
@app.route('/')
def home():
    return make_response(
        '<h1>Welcome to the Workout Tracker API</h1><p>Use the endpoints to manage your workouts and exercises.</p>'
        '<ul>'
        '<li>GET /workouts - List all workouts</li>'
        '<li>GET /workouts/&lt;id&gt; - Show a single workout with its associated exercises</li>'
        '<li>POST /workouts - Create a workout</li>'
        '<li>DELETE /workouts/&lt;id&gt; - Delete a workout</li>'
        '<li>GET /exercises - List all exercises</li>'
        '<li>GET /exercises/&lt;id&gt; - Show an exercise and associated workouts</li>'
        '<li>POST /exercises - Create an exercise</li>'
        '<li>DELETE /exercises/&lt;id&gt; - Delete an exercise</li>'
        '<li>POST /workouts/&lt;workout_id&gt;/exercises/&lt;exercise_id&gt;/workout_exercises - Add an exercise to a workout, including reps/sets/duration</li>'
        '</ul>')

# List all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    body = WorkoutSchema(many=True).dump(workouts)
    return jsonify(body), 200

# Stretch goal: include reps/sets/duration data from WorkoutExercises
# Show a single workout with its associated exercises
@app.route('/workouts/<id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if workout:
        body = WorkoutSchema().dump(workout)
        return jsonify(body), 200
    else:
        return jsonify({'error': 'Workout not found'}), 404

# Create a workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        workout_data = request.get_json()
        workout = WorkoutSchema().load(workout_data)
        db.session.add(workout)
        db.session.commit()
        body = WorkoutSchema().dump(workout)
        return jsonify(body), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

# Stretch goal: delete associated WorkoutExercises
# Delete a workout
@app.route('/workouts/<id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if workout:
        db.session.delete(workout)
        db.session.commit()
        return jsonify({'message': 'Workout deleted successfully'}), 200
    else:
        return jsonify({'error': 'Workout not found'}), 404

# List all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    body = ExerciseSchema(many=True).dump(exercises)
    return jsonify(body), 200

# Show an exercise and associated workouts
@app.route('/exercises/<id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise:
        body = ExerciseSchema().dump(exercise)
        return jsonify(body), 200
    else:
        return jsonify({'error': 'Exercise not found'}), 404

# Create an exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        exercise_data = request.get_json()
        exercise = ExerciseSchema().load(exercise_data)
        db.session.add(exercise)
        db.session.commit()
        body = ExerciseSchema().dump(exercise)
        return jsonify(body), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

# Stretch goal: delete associated WorkoutExercises
# Delete an exercise
@app.route('/exercises/<id>', methods=['DELETE'])
def delete_exercise(id):
    pass

# Add an exercise to a workout, including reps/sets/duration
@app.route('/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)