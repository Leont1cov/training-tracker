from app.models import Workout, Exercise, WorkoutExercise


def post_workout_exercises(data_workout_exercises, db):
    workout = db.get(Workout,data_workout_exercises.workout_id)  # первый параметр -> в какой модели ищем, второй параметр -> значение id по которому ищем
    exercise = db.get(Exercise, data_workout_exercises.exercise_id)

    if workout is None:
        return None
    if exercise is None:
        return None

    workout_exercises = WorkoutExercise(
        workout_id=data_workout_exercises.workout_id,
        exercise_id=data_workout_exercises.exercise_id,
        sets=data_workout_exercises.sets,
        reps=data_workout_exercises.reps,
        weight=data_workout_exercises.weight
    )

    db.add(workout_exercises)
    db.commit()
    db.refresh(workout_exercises)
    return workout_exercises

def get_workout_exercises(user_id, db):
    workout_exercises = db.query(WorkoutExercise.workout_id).filter(WorkoutExercise.workout_id == user_id).all()
    return workout_exercises

def get_workout_exercise(id, db):
    workout = db.query(WorkoutExercise).filter(WorkoutExercise.id == id).first()
    if workout is None:
        return None
    return workout

def patch_workout_exercise(data_workout_exercise, id, db):
    workout = db.get(WorkoutExercise, id)
    data = data_workout_exercise.model_dump(exclude_unset=True)

    if workout is None:
        return None

    for field, value in data.items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)

    return workout

def del_workout_exercise(id, db):
    workout = db.query(WorkoutExercise).filter(WorkoutExercise.id == id).first()

    if workout is None:
        return None

    db.delete(workout)
    db.commit()
    return True