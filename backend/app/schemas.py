from pydantic import BaseModel, Field


class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class CheckInCreate(BaseModel):
    done: bool


class Habit(BaseModel):
    id: int
    name: str
    check_ins: list[bool] = Field(default_factory=list)


class StreakOut(BaseModel):
    habit_id: int
    streak: int