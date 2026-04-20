from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth, users, notes

# Create all database tables automatically
# This reads all models that inherit from Base and creates their tables
# if they don't already exist
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI app instance
app = FastAPI(
    title="Notes API",
    description="A fully authenticated Notes API built with FastAPI, PostgreSQL and JWT",
    version="1.0.0"
)


# ==============================
#         MIDDLEWARE
# ==============================

# CORS — controls which frontends are allowed to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # In production replace * with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
#         ROUTERS
# ==============================

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(notes.router)


# ==============================
#         ROOT ENDPOINT
# ==============================

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Notes API",
        "docs": "Visit /docs to explore the API"
    }