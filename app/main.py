from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes.projects import router as projects_router


BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "static" / "index.html"


app = FastAPI(
    title="Code2KT",
    description="AI-powered Knowledge Transfer generator for software projects",
    version="0.1.0",

    # Disable FastAPI's public documentation pages.
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


app.include_router(projects_router)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )

    return response


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(INDEX_FILE)


@app.get("/health", include_in_schema=False)
def health():
    # Needed later for deployment / CI/CD health checks.
    return {"status": "healthy"}