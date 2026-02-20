#!/usr/bin/env python3
from app import app
from models import db, Exercise, Workout, WorkoutExercises
import datetime

with app.app_context():
	# Clear existing data
	WorkoutExercises.query.delete()
	Exercise.query.delete()
	Workout.query.delete()
	db.session.commit()

	# Add sample exercises
	ex1 = Exercise(name="Push Up", category="Strength", equipment_needed=False)
	ex2 = Exercise(name="Squat", category="Strength", equipment_needed=False)
	ex3 = Exercise(name="Jump Rope", category="Cardio", equipment_needed=True)
	ex4 = Exercise(name="Plank", category="Balance", equipment_needed=False)
	ex5 = Exercise(name="Yoga Stretch", category="Flexibility", equipment_needed=False)

	# Add sample workouts
	w1 = Workout(date=datetime.date(2026, 2, 19), duration_minutes=30, notes="Morning workout")
	w2 = Workout(date=datetime.date(2026, 2, 18), duration_minutes=45, notes="Evening workout")
	w3 = Workout(date=datetime.date(2026, 2, 17), duration_minutes=20, notes="Quick stretch")

	# Add sample workout-exercise associations (reps and sets always at least 1)
	we1 = WorkoutExercises(workout=w1, exercise=ex1, reps=15, sets=3, duration_seconds=60)
	we2 = WorkoutExercises(workout=w1, exercise=ex2, reps=20, sets=3, duration_seconds=60)
	we3 = WorkoutExercises(workout=w2, exercise=ex3, reps=1, sets=1, duration_seconds=300)
	we4 = WorkoutExercises(workout=w2, exercise=ex4, reps=1, sets=3, duration_seconds=60)
	we5 = WorkoutExercises(workout=w3, exercise=ex5, reps=1, sets=2, duration_seconds=120)
	
	# Add all to session and commit
	db.session.add_all([ex1, ex2, ex3, ex4, ex5, w1, w2, w3, we1, we2, we3, we4, we5])
	db.session.commit()

