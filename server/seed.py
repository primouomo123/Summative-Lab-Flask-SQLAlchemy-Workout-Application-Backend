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