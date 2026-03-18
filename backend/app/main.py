from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import settings
from . import models  # noqa: F401
from .routes.activities import router as activities_router


app = FastAPI(title="Starhub API", version="0.1.0")

origins = [o.strip() for o in settings.cors_allow_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True}


app.include_router(activities_router)

