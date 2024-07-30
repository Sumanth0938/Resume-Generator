import os
import uvicorn
from typing import Optional
from fastapi import FastAPI
from infra.database import Base,engine
from routers import resume,user

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(resume.router) 
app.include_router(user.router) 


