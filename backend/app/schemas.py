from pydantic import BaseModel


# User Registration Schema
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# User Login Schema
class UserLogin(BaseModel):
    email: str
    password: str


# Task Create Schema
class TaskCreate(BaseModel):
    title: str


# Task Response Schema
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True