import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from sqlalchemy import MetaData

DATABASE_URL = "sqlite:///./database.db"

engine = _sql.create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
metadata = MetaData()

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()
