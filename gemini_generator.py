from .config import WORKOUT_MODEL
from .gemini_client import get_client


def generate_workout_gemini(username: str, age: int, weight: float, goal: str, intensity: str) -> str:
    prompt = f"""
You are the workout-planning component of FitBuddy.

Create a safe, general 7-day wellness-oriented workout plan using:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Preferred intensity: {intensity}

Requirements:
- Return exactly 7 labeled days.
- For each day include: focus, warm-up, main activity/exercises, approximate duration,
  and cooldown/recovery.
- Keep the plan practical and beginner-friendly.
- Do not prescribe extreme exercise, starvation, rapid weight loss, supplements, or medical treatment.
- Do not diagnose injuries or medical conditions.
- If the user's information suggests a medical concern, recommend checking with a qualified
  healthcare professional before exercising.
- Include at least one recovery/rest-oriented day.
- Avoid presenting body weight or appearance as a measure of personal worth.
- State that the plan is general wellness information, not medical advice.

Format with clear headings and bullet points.
"""
    response = get_client().models.generate_content(model=WORKOUT_MODEL, contents=prompt)
    return response.text.strip()
