from pydantic import BaseModel

class OperationBase(BaseModel):
    expression: str


class OperationResponse(OperationBase):
    id: int
    result: float

    class Config:
        from_attributes = True  # Updated from 'orm_mode'
