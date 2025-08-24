from fastapi import FastAPI
from routes import generate, health

app = FastAPI()

app.include_router(health.router)
app.include_router(generate.router)
