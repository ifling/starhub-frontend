from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import User
from ..schemas import MiniProgramCode, TokenResponse, UserPublic, WebLogin, WebRegister
from ..security import create_access_token, hash_password, verify_password
from ..settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])

CHANNEL_WEB = "web"
CHANNEL_WEIXIN_MP = "weixin_mp"
CHANNEL_QQ_MP = "qq_mp"


def _token_for_user(user: User) -> TokenResponse:
    token = create_access_token(user_id=user.id, channel=user.channel)
    return TokenResponse(
        access_token=token,
        user=UserPublic.model_validate(user),
    )


@router.post("/web/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def web_register(payload: WebRegister, db: Session = Depends(get_db)):
    existing = db.execute(select(User).where(User.email == str(payload.email))).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        channel=CHANNEL_WEB,
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        openid=None,
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered") from None
    except OperationalError as e:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Database error (did you run migrations? alembic upgrade head)",
        ) from e
    return _token_for_user(user)


@router.post("/web/login", response_model=TokenResponse)
def web_login(payload: WebLogin, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == str(payload.email).lower())).scalar_one_or_none()
    if not user or user.channel != CHANNEL_WEB or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return _token_for_user(user)


def _exchange_wechat_jscode(code: str) -> str:
    if not settings.wechat_mp_appid or not settings.wechat_mp_secret:
        raise HTTPException(
            status_code=503,
            detail="WeChat mini program is not configured (WECHAT_MP_APPID / WECHAT_MP_SECRET)",
        )
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": settings.wechat_mp_appid,
        "secret": settings.wechat_mp_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    try:
        r = httpx.get(url, params=params, timeout=15.0)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"WeChat API error: {e}") from e

    errcode = data.get("errcode")
    if errcode not in (None, 0):
        raise HTTPException(
            status_code=400,
            detail=data.get("errmsg") or f"WeChat error code {errcode}",
        )
    openid = data.get("openid")
    if not openid:
        raise HTTPException(status_code=400, detail="WeChat did not return openid")
    return str(openid)


def _exchange_qq_jscode(code: str) -> str:
    if not settings.qq_mp_appid or not settings.qq_mp_secret:
        raise HTTPException(
            status_code=503,
            detail="QQ mini program is not configured (QQ_MP_APPID / QQ_MP_SECRET)",
        )
    url = "https://api.q.qq.com/sns/jscode2session"
    params = {
        "appid": settings.qq_mp_appid,
        "secret": settings.qq_mp_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    try:
        r = httpx.get(url, params=params, timeout=15.0)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"QQ API error: {e}") from e

    errcode = data.get("errcode")
    if errcode not in (None, 0):
        raise HTTPException(
            status_code=400,
            detail=data.get("errmsg") or f"QQ error code {errcode}",
        )
    openid = data.get("openid")
    if not openid:
        raise HTTPException(status_code=400, detail="QQ did not return openid")
    return str(openid)


@router.post("/weixin/mp", response_model=TokenResponse)
def auth_weixin_mp(payload: MiniProgramCode, db: Session = Depends(get_db)):
    openid = _exchange_wechat_jscode(payload.code)
    user = db.execute(
        select(User).where(User.channel == CHANNEL_WEIXIN_MP, User.openid == openid)
    ).scalar_one_or_none()
    if not user:
        user = User(
            channel=CHANNEL_WEIXIN_MP,
            email=None,
            password_hash=None,
            openid=openid,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return _token_for_user(user)


@router.post("/qq/mp", response_model=TokenResponse)
def auth_qq_mp(payload: MiniProgramCode, db: Session = Depends(get_db)):
    openid = _exchange_qq_jscode(payload.code)
    user = db.execute(
        select(User).where(User.channel == CHANNEL_QQ_MP, User.openid == openid)
    ).scalar_one_or_none()
    if not user:
        user = User(
            channel=CHANNEL_QQ_MP,
            email=None,
            password_hash=None,
            openid=openid,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return _token_for_user(user)
