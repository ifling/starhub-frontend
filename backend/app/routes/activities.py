from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_user
from ..models import Activity, Signup, User
from ..schemas import ActivityCreate, ActivityMineOut, ActivityOut, SignupCreate, SignupOut
from ..utils import generate_code


router = APIRouter(prefix="/activities", tags=["activities"])


def _owner_username(db: Session, owner_user_id) -> str | None:
    if owner_user_id is None:
        return None
    u = db.get(User, owner_user_id)
    if not u:
        return None
    return u.username if u.username else None


def _activity_out(db: Session, act: Activity) -> ActivityOut:
    return ActivityOut.model_validate(act, from_attributes=True).model_copy(
        update={"owner_username": _owner_username(db, act.owner_user_id)},
    )


@router.post("", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
def create_activity(
    payload: ActivityCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    uid_str = str(user.id)
    for _ in range(10):
        act = Activity(
            code=generate_code(),
            creator_id=uid_str,
            owner_user_id=user.id,
            title=payload.title,
            type=payload.type,
            deadline_at=payload.deadline_at,
            desc=payload.desc,
            limits=payload.limits,
        )
        db.add(act)
        try:
            db.commit()
            db.refresh(act)
            return _activity_out(db, act)
        except IntegrityError:
            db.rollback()
            continue

    raise HTTPException(status_code=500, detail="Failed to generate unique code")


@router.get("/mine", response_model=list[ActivityMineOut])
def list_my_activities(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # 统计每个活动的报名人数（signups 表记录数）
    signup_counts = (
        select(Signup.activity_id.label("activity_id"), func.count(Signup.id).label("signup_count"))
        .group_by(Signup.activity_id)
        .subquery()
    )

    rows = db.execute(
        select(
            Activity,
            func.coalesce(signup_counts.c.signup_count, 0).label("signup_count"),
        )
        .outerjoin(signup_counts, signup_counts.c.activity_id == Activity.id)
        .where(Activity.owner_user_id == user.id)
        .order_by(Activity.created_at.desc())
    ).all()

    result: list[ActivityMineOut] = []
    for act, signup_count in rows:
        out = _activity_out(db, act).model_dump()
        out["signup_count"] = int(signup_count or 0)
        result.append(ActivityMineOut(**out))
    return result


@router.get("", response_model=list[ActivityOut])
def list_activities(db: Session = Depends(get_db)):
    rows = db.execute(select(Activity).order_by(Activity.created_at.desc())).scalars().all()
    return [_activity_out(db, a) for a in rows]


@router.get("/{activity_id}", response_model=ActivityOut)
def get_activity(activity_id: str, db: Session = Depends(get_db)):
    act = db.get(Activity, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    return _activity_out(db, act)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activity_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    act = db.get(Activity, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    if act.owner_user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(act)
    db.commit()
    return None


@router.put("/{activity_id}", response_model=ActivityOut)
def update_activity(
    activity_id: str,
    payload: ActivityCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    act = db.get(Activity, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    if act.owner_user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    act.title = payload.title
    act.type = payload.type
    act.deadline_at = payload.deadline_at
    act.desc = payload.desc
    act.limits = payload.limits
    db.add(act)
    db.commit()
    db.refresh(act)
    return _activity_out(db, act)


@router.get("/code/{code}", response_model=ActivityOut)
def get_activity_by_code(code: str, db: Session = Depends(get_db)):
    act = db.execute(select(Activity).where(Activity.code == code)).scalar_one_or_none()
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    return _activity_out(db, act)


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

