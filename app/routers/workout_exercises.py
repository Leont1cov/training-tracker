from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Workout
from app.schemas import WorkoutExerciseCreate, WorkoutExerciseResponse
from app.services.workout_exercises import post_workout_exercises, get_workout_exercises, get_workout_exercise, \
    patch_workout_exercise, del_workout_exercise

router = APIRouter()

@router.post('/workout-exercises', response_model=WorkoutExerciseResponse)
def create_workout_exercises(data_workout_exercises: WorkoutExerciseCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    workout = db.get(Workout, data_workout_exercises.workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    if workout.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return post_workout_exercises(data_workout_exercises, db)

@router.get('/workout-exercises', response_model=list[WorkoutExerciseResponse])
def read_workout_exercises(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_workout_exercises(user.id, db)

@router.get('/workout-exercises/{id}', response_model=WorkoutExerciseResponse)
def read_workout_exercise(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = get_workout_exercise(id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Workout exercise not found")

    workout = db.get(Workout, result.workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    if workout.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return result

@router.patch('/workout-exercises/{id}', response_model=WorkoutExerciseResponse)
def update_workout_exercise(data_workout_exercise: WorkoutExerciseCreate, id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    source_data = get_workout_exercise(id, db)
    if source_data is None:
        raise HTTPException(status_code=404, detail="Workout exercise not found")

    workout = db.get(Workout, source_data.workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    if workout.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return patch_workout_exercise(data_workout_exercise, id, db)

@router.delete('/workout-exercises/{id}')
def delete_workout_exercise(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = get_workout_exercise(id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Workout exercise not found")

    workout = db.get(Workout, result.workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout exercise not found")

    if workout.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return del_workout_exercise(id, db)