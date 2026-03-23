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

# CORS_ALLOW_ORIGINS=* 时不能用 allow_origins=["*"] + credentials（浏览器会拒）。
# 用 allow_origin_regex 匹配常见 Origin，Starlette 会把响应头设为「请求里的 Origin」，可带 Authorization。
_origins = [o.strip() for o in settings.cors_allow_origins.split(",") if o.strip()]
_allow_star = not _origins or _origins == ["*"]
if _allow_star:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://[^\s]+",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/health")
def health():
    return {"ok": True}


app.include_router(auth_router)
app.include_router(activities_router)

