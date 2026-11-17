"""Compose HTTP routes. Business work belongs in feature modules."""
from fastapi import FastAPI

from .routes import scenarios, system

app = FastAPI(title="MirrorMind", version="0.0.1")
app.include_router(system.router)
app.include_router(scenarios.router)
