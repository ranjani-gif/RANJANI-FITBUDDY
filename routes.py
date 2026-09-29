from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .config import ADMIN_KEY
from .crud import (
    delete_user,
    get_all_users,
    get_latest_plan,
    save_plan,
    save_user,
    update_plan,
)
from .database import get_db
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"error": None},
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
        user = save_user(db, data)
        workout_plan = generate_workout_gemini(
            user.username, user.age, user.weight, user.goal, user.intensity
        )
        nutrition_tip = generate_nutrition_tip_with_flash(user.goal)
        plan = save_plan(db, user.user_id, workout_plan, nutrition_tip)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "plan": plan,
                "message": None,
                "error": None,
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)},
            status_code=400,
        )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        feedback_data = FeedbackRequest(user_id=user_id, feedback=feedback)
        plan = get_latest_plan(db, feedback_data.user_id)
        if not plan:
            raise HTTPException(status_code=404, detail="No workout plan found for this User ID.")

        from .models import User
        user = db.query(User).filter(User.user_id == feedback_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        revised = update_workout_plan(
            plan.original_plan,
            feedback_data.feedback,
            user.goal,
            user.intensity,
        )
        update_plan(db, plan, revised, feedback_data.feedback)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "plan": plan,
                "message": "Your plan was updated successfully.",
                "error": None,
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)},
            status_code=400,
        )


def _check_admin(key: str | None):
    if not ADMIN_KEY or key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing admin key.")


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    key: str | None = None,
    db: Session = Depends(get_db),
):
    _check_admin(key)
    users = get_all_users(db)
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": users, "key": key},
    )


@router.post("/delete-user")
def remove_user(
    user_id: str = Form(...),
    key: str = Form(...),
    db: Session = Depends(get_db),
):
    _check_admin(key)
    delete_user(db, user_id)
    return RedirectResponse(url=f"/view-all-users?key={key}", status_code=303)


@router.get("/api/health")
def health():
    return {"status": "ok", "service": "FitBuddy"}


@router.get("/api/users")
def api_users(key: str, db: Session = Depends(get_db)):
    _check_admin(key)
    users = get_all_users(db)
    return [
        {
            "user_id": u.user_id,
            "username": u.username,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
        }
        for u in users
    ]
