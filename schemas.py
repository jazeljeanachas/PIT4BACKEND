from pydantic import BaseModel

class JazelTodoBase(BaseModel):
    title: str
    completed: bool = False

class JazelTodoCreate(JazelTodoBase):
    pass

class JazelTodoUpdate(JazelTodoBase):
    pass

class JazelTodoOut(JazelTodoBase):
    id: int

    class Config:
        orm_mode = True