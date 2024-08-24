from fastapi import FastAPI
from auth.routes import router as auth_router
from service import routes

app = FastAPI()

app.include_router(routes.router)
app.include_router(auth_router, prefix="/auth")
""" 
curl -X GET "http://127.0.0.1:8000/index" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqdWxpb0BqdWxpby5jb20iLCJleHAiOjE3MjQ1NDIzNjR9.nYFy7jEI88rOaDU1num7he52nKNpah0WpFLL8BQHznU"

curl -X GET "http://127.0.0.1:8000/auth/logout" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqdWxpb0BqdWxpby5jb20iLCJleHAiOjE3MjQ1NDIzNjR9.nYFy7jEI88rOaDU1num7he52nKNpah0WpFLL8BQHznU"

"""