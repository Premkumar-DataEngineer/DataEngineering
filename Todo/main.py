from .database import Base, engine
from .router import auth, todo, admin, users
from fastapi import FastAPI

app = FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/healthy")
async def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(users.router)