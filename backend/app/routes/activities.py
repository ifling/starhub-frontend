from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Header
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Activity, Signup
from ..schemas import ActivityCreate, ActivityOut, SignupCreate, SignupOut
from ..utils import generate_code


router = APIRouter(prefix="/activities", tags=["activities"])


_CLIENT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,64}$")


def get_client_id(x_client_id: str | None = Header(default=None, alias="X-Client-Id")) -> str:
    if not x_client_id or not _CLIENT_ID_RE.match(x_client_id):
        raise HTTPException(status_code=400, detail="Missing or invalid X-Client-Id")
    return x_client_id


@router.post("", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
def create_activity(payload: ActivityCreate, db: Session = Depends(get_db), client_id: str = Depends(get_client_id)):
    for _ in range(10):
        act = Activity(
            code=generate_code(),
            creator_id=client_id,
            title=payload.title,
            type=payload.type,
            deadline_at=payload.deadline_at,
            desc=payload.desc,
        )
        db.add(act)
        try:
            db.commit()
            db.refresh(act)
            return act
        except IntegrityError:
            db.rollback()
            continue

    raise HTTPException(status_code=500, detail="Failed to generate unique code")


@router.get("/mine", response_model=list[ActivityOut])
def list_my_activities(db: Session = Depends(get_db), client_id: str = Depends(get_client_id)):
    rows = (
        db.execute(
            select(Activity)
            .where(Activity.creator_id == client_id)
            .order_by(Activity.created_at.desc())
        )
        .scalars()
        .all()
    )
    return rows


@router.get("", response_model=list[ActivityOut])
def list_activities(db: Session = Depends(get_db)):
    rows = db.execute(select(Activity).order_by(Activity.created_at.desc())).scalars().all()
    return rows


@router.get("/{activity_id}", response_model=ActivityOut)
def get_activity(activity_id: str, db: Session = Depends(get_db)):
    act = db.get(Activity, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    return act


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: str, db: Session = Depends(get_db), client_id: str = Depends(get_client_id)):
    act = db.get(Activity, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    if act.creator_id != client_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(act)
    db.commit()
    return None


@router.put("/{activity_id}", response_model=ActivityOut)
def update_activity(
    activity_id: str,
    payload: ActivityCreate,
    db: Session = Depends(get_db),
    client_id: str = Depends(get_client_id),
):
    act = db.get(Activity, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    if act.creator_id != client_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    act.title = payload.title
    act.type = payload.type
    act.deadline_at = payload.deadline_at
    act.desc = payload.desc
    db.add(act)
    db.commit()
    db.refresh(act)
    return act


@router.get("/code/{code}", response_model=ActivityOut)
def get_activity_by_code(code: str, db: Session = Depends(get_db)):
    act = db.execute(select(Activity).where(Activity.code == code)).scalar_one_or_none()
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    return act


@router.post("/{activity_id}/signups", response_model=SignupOut, status_code=status.HTTP_201_CREATED)
def create_signup(activity_id: str, payload: SignupCreate, db: Session = Depends(get_db)):
    act = db.get(Activity, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")

    s = Signup(activity_id=act.id, nickname=payload.nickname, role=payload.role, note=payload.note)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("/{activity_id}/signups", response_model=list[SignupOut])
def list_signups(activity_id: str, db: Session = Depends(get_db)):
    act = db.get(Activity, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    rows = (
        db.execute(select(Signup).where(Signup.activity_id == act.id).order_by(Signup.created_at.asc()))
        .scalars()
        .all()
    )
    return rows


@router.delete("/{activity_id}/signups/{signup_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_signup(activity_id: str, signup_id: str, db: Session = Depends(get_db)):
    act = db.get(Activity, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")

    s = db.get(Signup, signup_id)
    if not s or str(s.activity_id) != str(act.id):
        raise HTTPException(status_code=404, detail="Signup not found")
    db.delete(s)
    db.commit()
    return None

