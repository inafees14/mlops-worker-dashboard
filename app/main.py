from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import admin
from app.services.seeder import seed_if_empty

from app.core.database import Base, engine
from app.api import health, seed, events, metrics

app = FastAPI(title="AI Worker Productivity Dashboard")

Base.metadata.create_all(bind=engine)
seed_if_empty()

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Home route
@app.get("/")
def dashboard():
    return FileResponse("app/static/index.html")

app.include_router(health.router)
app.include_router(health.router, prefix="/api")
app.include_router(seed.router)
app.include_router(events.router)
app.include_router(metrics.router)
app.include_router(admin.router)
