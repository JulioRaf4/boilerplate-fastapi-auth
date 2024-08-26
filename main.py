from fastapi import FastAPI
from auth.routes import router as auth_router
from service import routes

app = FastAPI()

app.include_router(routes.router)
app.include_router(auth_router, prefix="/auth")
