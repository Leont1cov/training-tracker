from app.models import Exercise


def post_exercise(exercise_data, db):
    exercise = Exercise(title=exercise_data.title)

    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return exercise

def get_exercises(db):
    exercises = db.query(Exercise).all()
    return exercises

def get_exercise(exercise_id, db):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    return exercise

def patch_exercise(exercise_data, exercise_id, db):
    exercise = db.get(Exercise, exercise_id)
    data = exercise_data.model_dump(exclude_unset=True)

    if exercise is None:
        return None

    for field, value in data.items():
        setattr(exercise, field, value)

    db.commit()
    db.refresh(exercise)

    return exercise

def del_exercise(exercise_id, db):
    exercise = db.get(Exercise, exercise_id)

    if exercise is None:
        return None

    db.delete(exercise)
    db.commit()

    return True