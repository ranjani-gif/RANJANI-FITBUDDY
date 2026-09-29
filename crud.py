from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Plan, User


def save_user(db: Session, data):
    user = db.scalar(select(User).where(User.user_id == data.user_id))
    if user:
        user.username = data.username
        user.age = data.age
        user.weight = data.weight
        user.goal = data.goal
        user.intensity = data.intensity
    else:
        user = User(
            user_id=data.user_id,
            username=data.username,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity,
        )
        db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_plan(db: Session, user_id: str, original_plan: str, nutrition_tip: str):
    plan = Plan(
        user_id=user_id,
        original_plan=original_plan,
        nutrition_tip=nutrition_tip,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_latest_plan(db: Session, user_id: str):
    return db.scalar(
        select(Plan)
        .where(Plan.user_id == user_id)
        .order_by(Plan.id.desc())
    )


def update_plan(db: Session, plan: Plan, updated_plan: str, feedback: str):
    plan.updated_plan = updated_plan
    plan.feedback = feedback
    plan.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(plan)
    return plan


def get_all_users(db: Session):
    return db.scalars(select(User).order_by(User.id.desc())).all()


def get_plans_for_users(db: Session):
    return db.scalars(select(Plan).order_by(Plan.id.desc())).all()


def delete_user(db: Session, user_id: str):
    user = db.scalar(select(User).where(User.user_id == user_id))
    if not user:
        return False
    plans = db.scalars(select(Plan).where(Plan.user_id == user_id)).all()
    for plan in plans:
        db.delete(plan)
    db.delete(user)
    db.commit()
    return True
