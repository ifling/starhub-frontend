import datetime as dt
import uuid

from pydantic import BaseModel, EmailStr, Field


class WebRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class WebLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class MiniProgramCode(BaseModel):
    code: str = Field(min_length=4, max_length=256)


class UserPublic(BaseModel):
    id: uuid.UUID
    channel: str
    email: str | None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class ActivityCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    type: str = Field(default="副本", max_length=24)
    deadline_at: dt.datetime | None = None
    desc: str | None = Field(default=None, max_length=2000)


class ActivityOut(BaseModel):
    id: uuid.UUID
    code: str
    creator_id: str
    owner_user_id: uuid.UUID | None = None
    title: str
    type: str
    deadline_at: dt.datetime | None
    desc: str | None
    created_at: dt.datetime

    class Config:
        from_attributes = True


class SignupCreate(BaseModel):
    nickname: str = Field(min_length=1, max_length=64)
    role: str | None = Field(default=None, max_length=16)
    note: str | None = Field(default=None, max_length=200)


class SignupOut(BaseModel):
    id: uuid.UUID
    activity_id: uuid.UUID
    nickname: str
    role: str | None
    note: str | None
    created_at: dt.datetime

    class Config:
        from_attributes = True

