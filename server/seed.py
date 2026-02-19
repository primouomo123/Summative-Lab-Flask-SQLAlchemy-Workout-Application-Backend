#!/usr/bin/env python3
from app import app
from models import db, Exercise, Workout, WorkoutExercises
import datetime

with app.app_context():
	# Clear existing data
	WorkoutExercises.query.delete()
	Exercise.query.delete()
	Workout.query.delete()
	# Add sample exercises
	ex1 = Exercise(name="Push Up", category="Strength", equipment_needed=False)
	ex2 = Exercise(name="Squat", category="Strength", equipment_needed=False)
	ex3 = Exercise(name="Jump Rope", category="Cardio", equipment_needed=True)
	# Add sample workouts with date objects
	w1 = Workout(date=datetime.date(2026, 2, 19), duration_minutes=30, notes="Morning workout")
	w2 = Workout(date=datetime.date(2026, 2, 18), duration_minutes=45, notes="Evening workout")
	# Add sample workout-exercise associations
	we1 = WorkoutExercises(workout=w1, exercise=ex1, reps=15, sets=3, duration_seconds=0)
	we2 = WorkoutExercises(workout=w1, exercise=ex2, reps=20, sets=3, duration_seconds=0)
	we3 = WorkoutExercises(workout=w2, exercise=ex3, reps=0, sets=0, duration_seconds=300)
	# Add all to session and commit
	db.session.add_all([ex1, ex2, ex3, w1, w2, we1, we2, we3])
	db.session.commit()