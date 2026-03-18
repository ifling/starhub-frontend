from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import swagger_ui_bundle

from .settings import settings
from . import models  # noqa: F401
from .routes.activities import router as activities_router


app = FastAPI(
    title="Starhub API",
    version="0.1.0",
    swagger_ui_parameters={"persistAuthorization": True},
    swagger_js_url="/swagger/swagger-ui-bundle.js",
    swagger_css_url="/swagger/swagger-ui.css",
    swagger_favicon_url="/swagger/favicon-32x32.png",
)

app.mount("/swagger", StaticFiles(directory=swagger_ui_bundle.swagger_ui_3_path), name="swagger")

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

