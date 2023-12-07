from database import Base
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import datetime as _dt
class User(Base):
    __tablename__ = 'users'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, index=True)
    hashed_password = _sql.Column(_sql.String)
    blogs = _orm.relationship("Blog", back_populates="owner")
    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
class  Blog(Base):
    __tablename__ = "blogs"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    title = _sql.Column(_sql.String)
    anons = _sql.Column(_sql.String)
    text = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="blogs")
