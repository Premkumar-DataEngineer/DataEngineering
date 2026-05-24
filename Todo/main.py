from fastapi import FastAPI
import sys
sys.path.append("/Users/navyadev/Documents/GitHub/DataEngineering/Todo")
from database import engine
from models import Base
from routers import auth, todo, admin, users


app = FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/healthy")
async def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(users.router)