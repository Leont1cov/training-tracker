from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Workout
from app.schemas import WorkoutResponse, WorkoutCreate

router = APIRouter()

#создать тренировку
@router.post("/workouts", response_model=WorkoutResponse)
def create_workout(workout_data: WorkoutCreate, db: Session = Depends(get_db)):
    user = db.get(User, workout_data.user_id) #находим user_id

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    workout = Workout(user_id=workout_data.user_id, title=workout_data.title, completed=workout_data.completed)

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return workout

#читаем все тренировки
@router.get("/workouts", response_model=list[WorkoutResponse])
def read_workouts(db: Session = Depends(get_db)):
    workouts = db.query(Workout).all()
    return workouts

#читаем 1 тренировку по id
@router.get("/workouts/{workout_id}", response_model=WorkoutResponse)
def read_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    return workout

#меняем данные тренировки
@router.patch("/workouts/{workout_id}", response_model=WorkoutResponse)
def update_workout(work_data: WorkoutCreate, workout_id: int, db: Session = Depends(get_db)):
    workout = db.get(Workout, workout_id)

    data = work_data.model_dump(exclude_unset=True)

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    for field, values in data.items():
        setattr(workout, field, values)

    db.commit()
    db.refresh(workout)

    return workout

#удаляем тренировку
@router.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    db.delete(workout)
    db.commit()