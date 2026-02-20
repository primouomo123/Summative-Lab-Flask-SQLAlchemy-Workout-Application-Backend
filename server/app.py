from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercises

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return make_response(
        '<h1>Welcome to the Workout Tracker API</h1><p>Use the endpoints to manage your workouts and exercises.</p>')

@app.route('/workouts', methods=['GET'])
def get_workouts():
    pass

@app.route('/workouts/<id>', methods=['GET'])
def get_workout(id):
    pass

@app.route('/workouts', methods=['POST'])
def create_workout():
    pass

@app.route('/workouts/<id>', methods=['DELETE'])
def delete_workout(id):
    pass

@app.route('/exercises', methods=['GET'])
def get_exercises():
    pass

@app.route('/exercises/<id>', methods=['GET'])
def get_exercise(id):
    pass

@app.route('/exercises', methods=['POST'])
def create_exercise():
    pass

@app.route('/exercises', methods=['POST'])
def create_exercise():
    pass

@app.route('/exercises/<id>', methods=['DELETE'])
def delete_exercise(id):
    pass

@app.route('/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)