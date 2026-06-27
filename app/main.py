from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Finance API is working"}