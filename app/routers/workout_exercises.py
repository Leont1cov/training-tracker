from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import WorkoutExerciseCreate, WorkoutExerciseResponse
from app.services.workout_exercises import post_workout_exercises, get_workout_exercises, get_workout_exercise, \
    patch_workout_exercise, del_workout_exercise

router = APIRouter()

@router.post('/workout-exercises', response_model=WorkoutExerciseResponse)
def create_workout_exercises(data_workout_exercises: WorkoutExerciseCreate, db: Session = Depends(get_db)):
    result = post_workout_exercises(data_workout_exercises, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Workout exercises not found")
    return result

@router.get('/workout-exercises', response_model=list[WorkoutExerciseResponse])
def read_workout_exercises(db: Session = Depends(get_db)):
    return get_workout_exercises(db)

@router.get('/workout-exercises/{id}', response_model=WorkoutExerciseResponse)
def read_workout_exercise(id: int, db: Session = Depends(get_db)):
    result = get_workout_exercise(id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Workout exercise not found")
    return result

@router.patch('/workout-exercises/{id}', response_model=WorkoutExerciseResponse)
def update_workout_exercise(data_workout_exercise: WorkoutExerciseCreate, id: int, db: Session = Depends(get_db)):
    result = patch_workout_exercise(data_workout_exercise, id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Workout exercise not found")
    return result

@router.delete('/workout-exercises/{id}')
def delete_workout_exercise(id: int, db: Session = Depends(get_db)):
    result = del_workout_exercise(id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Workout exercise not found")
    return result