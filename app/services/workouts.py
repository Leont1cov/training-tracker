from app.models import Workout, User

#создать тренировку
def post_workout(workout_data, db):
    user = db.get(User, workout_data.user_id)  # находим user_id

    if user is None:
        return None

    workout = Workout(user_id=workout_data.user_id, title=workout_data.title, completed=workout_data.completed)

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return workout

#получить все тренировки
def get_workouts(db):
    workouts = db.query(Workout).all()
    return workouts

#получить тренировку по id
def get_workout(workout_id, db):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    return workout

#изменить тренировку
def patch_workout(work_data,  workout_id, db):
    workout = db.get(Workout, workout_id)
    data = work_data.model_dump(exclude_unset=True)

    if workout is None:
        return None

    for field, values in data.items():
        setattr(workout, field, values)

    db.commit()
    db.refresh(workout)

    return workout

#удалить тренировку
def del_workout(workout_id, db):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()

    if workout is None:
        return None

    db.delete(workout)
    db.commit()