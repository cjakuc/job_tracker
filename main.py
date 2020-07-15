from fastapi import FastAPI, Request, status, Depends, HTTPException
from pydantic import BaseModel
from routers import job_tracker

# to run the app vvv
# uvicorn main:app --reload

app = FastAPI()

app.include_router(job_tracker.router)