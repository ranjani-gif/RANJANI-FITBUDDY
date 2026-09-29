from .config import WORKOUT_MODEL
from .gemini_client import get_client


def update_workout_plan(original_plan: str, feedback: str, goal: str, intensity: str) -> str:
    prompt = f"""
You are updating a general wellness workout plan in FitBuddy.

Goal: {goal}
Preferred intensity: {intensity}

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Return a revised 7-day plan. Apply reasonable feedback while keeping the plan safe.
Do not introduce extreme exercise, restrictive eating, rapid weight-loss instructions,
supplements, or medical treatment. Keep at least one recovery/rest-oriented day.
Clearly label all 7 days and include focus, warm-up, main activity, duration, and cooldown/recovery.
Finish with: "General wellness information — not medical advice."
"""
    response = get_client().models.generate_content(model=WORKOUT_MODEL, contents=prompt)
    return response.text.strip()
