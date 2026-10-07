from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ExerciseResponse, ExerciseCreate
from app.services.exercises import post_exercise, get_exercises, get_exercise, patch_exercise, del_exercise

router = APIRouter()

#создаём упржанение
@router.post("/exercises", response_model=ExerciseResponse)
def create_exercise(exercise_data: ExerciseCreate, db: Session = Depends(get_db)):
    result = post_exercise(exercise_data, db)

    return result

#получаем упражнения
@router.get("/exercises", response_model=list[ExerciseResponse])
def read_exercises(db: Session = Depends(get_db)):
    return get_exercises(db)

#читаем одно упржанение
@router.get("/exercises/{exercise_id}", response_model=ExerciseResponse)
def read_exercise(exercise_id: int, db: Session = Depends(get_db)):
    result = get_exercise(exercise_id, db)

    if not result:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return result

#изменяем
@router.patch("/exercises/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(exercise_data: ExerciseCreate, exercise_id: int, db: Session = Depends(get_db)):
    result = patch_exercise(exercise_data, exercise_id, db)

    if result is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return result

#удаляем
@router.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    result = del_exercise(exercise_id, db)

    if result is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return result
