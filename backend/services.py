import jwt as _jwt
import database as _database, models as _models, schemas as _schemas
import passlib.hash as _hash
import sqlalchemy.orm as _orm
import fastapi as _fastapi
import fastapi.security as _security
import datetime as _dt
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "myJWtSecret"

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    user_obj = _models.User(
        email=user.email,hashed_password=_hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)
    token = _jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")

async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email, db)
    if not user:
        return False
    
    if not user.verify_password(password):
        return False
    
    return user


async def get_current_user(
        db: _orm.Session = _fastapi.Depends(get_db),
        token: str = _fastapi.Depends(oauth2schema)
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])

    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or password"
        )
    return _schemas.User.from_orm(user)


async def create_post(user: _schemas.UserCreate, db: _orm.Session, post: _schemas.BlogCreate):
    post_obj = _models.Blog(
        title=post.title,anons=post.anons,text=post.text, owner_id=user.id
    )
    db.add(post_obj)
    db.commit()
    db.refresh(post_obj)
    return post_obj


async def get_post(
        db: _orm.Session
       
):
    blog = db.query(_models.Blog).all()
    json_compatible_item_data = jsonable_encoder(blog)
    return JSONResponse(content=json_compatible_item_data)
