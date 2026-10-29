import os
from fastapi import FastAPI, HTTPException

from app.schemas import CheckInCreate, Habit, HabitCreate, StreakOut
from app.streak import calculate_streak

app = FastAPI(title="Habit Tracker API", version="0.2.0")

# Временное хранилище в памяти. База данных появится позже.
_habits: dict[int, Habit] = {}
_next_id = 1


def _get_habit_or_404(habit_id: int) -> Habit:
    habit = _habits.get(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/habits", response_model=Habit, status_code=201)
def create_habit(payload: HabitCreate):
    global _next_id
    habit = Habit(id=_next_id, name=payload.name)
    _habits[habit.id] = habit
    _next_id += 1
    return habit


@app.get("/habits", response_model=list[Habit])
def list_habits():
    return list(_habits.values())


@app.post("/habits/{habit_id}/checkins", response_model=Habit)
def add_check_in(habit_id: int, payload: CheckInCreate):
    habit = _get_habit_or_404(habit_id)
    habit.check_ins.append(payload.done)
    return habit


@app.get("/habits/{habit_id}/streak", response_model=StreakOut)
def get_streak(habit_id: int):
    habit = _get_habit_or_404(habit_id)
    return StreakOut(habit_id=habit_id, streak=calculate_streak(habit.check_ins))
