from .config import TIP_MODEL
from .gemini_client import get_client


def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = f"""
Give one concise, practical nutrition or recovery tip for a general wellness app.
User goal: {goal}

Keep it suitable for a broad audience:
- Encourage balanced meals, hydration, adequate sleep, and regular recovery.
- Do not recommend calorie restriction, fasting, purging, weight-loss drugs, or supplements.
- Do not make medical claims.
- Keep the answer to 3-5 sentences.
"""
    response = get_client().models.generate_content(model=TIP_MODEL, contents=prompt)
    return response.text.strip()
