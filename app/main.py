from fastapi import FastAPI

from app.routers import users, workouts, exercises, workout_exercises

app = FastAPI()

app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(workout_exercises.router)