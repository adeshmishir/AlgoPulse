from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.user import User
from app.routes.profile import router as profile_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AlgoPulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AlgoPulse API is running"}

app.include_router(profile_router, prefix="/api")