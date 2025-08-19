from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.routers import users

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Proteus API"}

# Run this once in your main.py or a setup script
Base.metadata.create_all(bind=engine)