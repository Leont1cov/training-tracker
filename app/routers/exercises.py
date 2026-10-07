from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Exercise
from app.schemas import ExerciseResponse, ExerciseCreate

router = APIRouter()

#создаём упржанение
@router.post("/exercises", response_model=ExerciseResponse)
def create_exercise(exercise_data: ExerciseCreate, db: Session = Depends(get_db)):
    exercise = Exercise(title=exercise_data.title)

    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return exercise

#получаем упражнения
@router.get("/exercises", response_model=list[ExerciseResponse])
def read_exercises(db: Session = Depends(get_db)):
    exercises = db.query(Exercise).all()
    return exercises

#читаем одно упржанение
@router.get("/exercises/{exercise_id}", response_model=ExerciseResponse)
def read_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

#изменяем
@router.patch("/exercises/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(exercise_data: ExerciseCreate, exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.get(Exercise, exercise_id)
    data = exercise_data.model_dump(exclude_unset=True)

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    for field, value in data.items():
        setattr(exercise, field, value)

    db.commit()
    db.refresh(exercise)

    return exercise

#удаляем
@router.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    db.delete(exercise)
    db.commit()
