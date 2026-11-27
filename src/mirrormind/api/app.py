"""Compose HTTP routes. Business work belongs in feature modules."""
from fastapi import FastAPI

from mirrormind import __version__

from .routes import decisions, scenarios, system

app = FastAPI(title="MirrorMind", version=__version__)
app.include_router(system.router)
app.include_router(scenarios.router)
app.include_router(decisions.router)
