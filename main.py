from fastapi import FastAPI
from auth.routes import router as auth_router
from auth.dependencies import get_db
from auth.models import Base
from auth.database import engine
from service import routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(routes.router)

app.include_router(auth_router, prefix="/auth")
