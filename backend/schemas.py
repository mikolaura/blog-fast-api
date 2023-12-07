import datetime as _dt

import pydantic as _pydantic



class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True
        from_attributes = True
        allow_population_by_field_name = True


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
        allow_population_by_field_name = True



class _BlogBase(_pydantic.BaseModel):
    title: str
    anons: str
    text: str


class BlogCreate(_BlogBase):
    pass

    class Config:
        orm_mode = True
        from_attributes = True
        allow_population_by_field_name = True



class Blog(_BlogBase):
    id: int
    owner_id: int
    data_created: _dt.datetime
    data_last_updated: _dt.datetime

    class Config:
        orm_mode = True
        from_attributes = True
        allow_population_by_field_name = True
