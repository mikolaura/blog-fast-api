from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from fastapi.middleware.cors import CORSMiddleware

import services as _services, schemas as _schemas
from database import Base, engine

app = _fastapi.FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_tables():
    Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():
    create_tables()


@app.post("/users")
async def create(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user: 
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")
    user_ = await _services.create_user(user, db)
    return await _services.create_token(user_)
    

@app.post("/api/token")
async def create_token(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),):
    user = await _services.authenticate_user(form_data.username, form_data.password,db)
    
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid credentials")
    
    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@app.post("/api/post")
async def create_post(post: _schemas.BlogCreate ,user: _schemas.User = _fastapi.Depends(_services.get_current_user), db:_orm.Session = _fastapi.Depends(_services.get_db) ):
    return await _services.create_post(user,db,post)


@app.get("/api/post", response_model=List[_schemas.Blog])
async def get_post( db: _orm.Session = _fastapi.Depends(_services.get_db),):
    return await _services.get_post(db)