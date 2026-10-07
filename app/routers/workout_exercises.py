from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import WorkoutExercise, Workout, Exercise
from app.schemas import WorkoutExerciseCreate, WorkoutExerciseResponse

router = APIRouter()

@router.post('/workout-exercises', response_model=WorkoutExerciseResponse)
def create_workout_exercises(data_workout_exercises: WorkoutExerciseCreate, db: Session = Depends(get_db)):
    workout = db.get(Workout, data_workout_exercises.workout_id) #первый параметр -> в какой модели ищем, второй параметр -> значение id по которому ищем
    exercise = db.get(Exercise, data_workout_exercises.exercise_id)

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout ID not found")
    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise ID not found")

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

@router.get('/workout-exercises', response_model=list[WorkoutExerciseResponse])
def read_workout_exercises(db: Session = Depends(get_db)):
    workout_exercises = db.query(WorkoutExercise).all()
    return workout_exercises

@router.get('/workout-exercises/{id}', response_model=WorkoutExerciseResponse)
def read_workout_exercise(id: int, db: Session = Depends(get_db)):
    workout = db.query(WorkoutExercise).filter(WorkoutExercise.id == id).first()
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout ID not found")
    return workout

@router.patch('/workout-exercises/{id}', response_model=WorkoutExerciseResponse)
def update_workout_exercise(data_workout_exercise: WorkoutExerciseCreate, id: int, db: Session = Depends(get_db)):
    workout = db.get(WorkoutExercise, id)
    data = data_workout_exercise.model_dump(exclude_unset=True)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout ID not found")

    for field, value in data.items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)

    return workout

@router.delete('/workout-exercises/{id}')
def delete_workout_exercise(id: int, db: Session = Depends(get_db)):
    workout = db.query(WorkoutExercise).filter(WorkoutExercise.id == id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout ID not found")
    db.delete(workout)
    db.commit()