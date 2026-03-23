from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import swagger_ui_bundle

from .settings import settings
from . import models  # noqa: F401  # User, Activity, Signup
from .routes.activities import router as activities_router
from .routes.auth import router as auth_router


app = FastAPI(
    title="Starhub API",
    version="0.1.0",
    swagger_ui_parameters={"persistAuthorization": True},
    swagger_js_url="/swagger/swagger-ui-bundle.js",
    swagger_css_url="/swagger/swagger-ui.css",
    swagger_favicon_url="/swagger/favicon-32x32.png",
)

app.mount("/swagger", StaticFiles(directory=swagger_ui_bundle.swagger_ui_path), name="swagger")

# 注意：allow_credentials=True 时不能使用 allow_origins=["*"]（浏览器会拒绝），
# 本地 H5 用 127.0.0.1:5173 跨域时若 .env 里是 *，必须把 credentials 关掉才能带上 Authorization。
_origins = [o.strip() for o in settings.cors_allow_origins.split(",") if o.strip()]
_allow_star = not _origins or _origins == ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins if _origins else ["*"],
    allow_credentials=False if _allow_star else True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True}


app.include_router(auth_router)
app.include_router(activities_router)

