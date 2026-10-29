def calculate_streak(habit_checkins: list) -> int:
    """Вычисляет текущую серию последовательных выполнений привычки."""
    streak = 0

    for checkin in reversed(habit_checkins):
        if checkin:
            streak += 1
        else:
            break


    print(f"Текущая серия: {streak}")
    return streak