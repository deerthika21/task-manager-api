from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.auth import (
    hash_password,
    verify_password,
    create_access_token
)
from fastapi.security import OAuth2PasswordBearer
from fastapi import Header
from app.auth import verify_token
from app.models import Task
from app.schemas import TaskCreate, TaskResponse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Database Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    user_id = verify_token(token)

    return user_id


# Register API
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    return {"message": "User registered successfully"}


# Login API
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {"user_id": db_user.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# Create Task
@router.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    new_task = Task(
        title=task.title,
        owner_id=user_id
    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return {
        "message": "Task created successfully"
    }

# Get All Tasks
@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    completed: bool = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    query = db.query(Task).filter(
        Task.owner_id == user_id
    )

    # Filtering
    if completed is not None:
        query = query.filter(
            Task.completed == completed
        )

    tasks = query.offset(skip).limit(limit).all()

    return tasks   

# Get Single Task
@router.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task   

# Update Task
@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.completed = True

    db.commit()

    return {
        "message": "Task marked completed"
    } 

# Delete Task
@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)

    db.commit()

    return {
        "message": "Task deleted successfully"
    }       