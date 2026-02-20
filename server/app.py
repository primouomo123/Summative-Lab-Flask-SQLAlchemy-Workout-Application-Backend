from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercises

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
        '<h1>Welcome to the Workout Tracker API</h1><p>Use the endpoints to manage your workouts and exercises.</p>')

# List all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    pass

# Stretch goal: include reps/sets/duration data from WorkoutExercises
# Show a single workout with its associated exercises
@app.route('/workouts/<id>', methods=['GET'])
def get_workout(id):
    pass

# Create a workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    pass

# Stretch goal: delete associated WorkoutExercises
# Delete a workout
@app.route('/workouts/<id>', methods=['DELETE'])
def delete_workout(id):
    pass

# List all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    pass

# Show an exercise and associated workouts
@app.route('/exercises/<id>', methods=['GET'])
def get_exercise(id):
    pass

# Create an exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    pass

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