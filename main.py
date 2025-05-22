from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, SessionLocal, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/jazeltodo", response_model=list[schemas.JazelTodoOut])
def read_todos(db: Session = Depends(get_db)):
    return db.query(models.JazelTodo).all()

@app.get("/jazeltodo/{todo_id}", response_model=schemas.JazelTodoOut)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.JazelTodo).get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/jazeltodo", response_model=schemas.JazelTodoOut)
def create_todo(todo: schemas.JazelTodoCreate, db: Session = Depends(get_db)):
    db_todo = models.JazelTodo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/jazeltodo/{todo_id}", response_model=schemas.JazelTodoOut)
def update_todo(todo_id: int, todo: schemas.JazelTodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(models.JazelTodo).get(todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/jazeltodo/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.JazelTodo).get(todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Deleted"}
