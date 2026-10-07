from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import WorkoutResponse, WorkoutCreate
from app.services.workouts import post_workout, get_workouts, get_workout, patch_workout, del_workout

router = APIRouter()

#создаём тренировку
@router.post("/workouts", response_model=WorkoutResponse)
def create_workout(workout_data: WorkoutCreate, db: Session = Depends(get_db)):
    result = post_workout(workout_data, db)

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    return result

#читаем все тренировки
@router.get("/workouts", response_model=list[WorkoutResponse])
def read_workouts(db: Session = Depends(get_db)):
    return get_workouts(db)

#читаем 1 тренировку по id
@router.get("/workouts/{workout_id}", response_model=WorkoutResponse)
def read_workout(workout_id: int, db: Session = Depends(get_db)):
    return get_workout(workout_id, db)

#меняем данные тренировки
@router.patch("/workouts/{workout_id}", response_model=WorkoutResponse)
def update_workout(work_data: WorkoutCreate, workout_id: int, db: Session = Depends(get_db)):
    return patch_workout(work_data, workout_id, db)

#удаляем тренировку
@router.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    del_workout(workout_id, db)