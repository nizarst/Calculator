from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from app.database import SessionLocal, engine
from app.models import Base, Operation
from app.schemas import OperationBase, OperationResponse
import io
import pandas as pd

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# RPN evaluation function
def evaluate_rpn(expression: str) -> float:
    stack = []
    operators = {'+': lambda x, y: x + y,
                 '-': lambda x, y: x - y,
                 '*': lambda x, y: x * y,
                 '/': lambda x, y: x / y}

    for token in expression.split():
        if token in operators:
            y, x = stack.pop(), stack.pop()
            stack.append(operators[token](x, y))
        else:
            stack.append(float(token))
    
    return stack[0]

@app.post("/calculate", response_model=OperationResponse)
def calculate(operation: OperationBase):
    db: Session = SessionLocal()
    try:
        result = evaluate_rpn(operation.expression)
        db_operation = Operation(expression=operation.expression, result=result)
        db.add(db_operation)
        db.commit()
        db.refresh(db_operation)
        return db_operation
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/export")
def export_data():
    db: Session = SessionLocal()
    try:
        operations = db.query(Operation).all()

        # Convert the data to a pandas DataFrame
        data = []
        for operation in operations:
            data.append({
                "id": operation.id,
                "expression": operation.expression,
                "result": operation.result
            })
        df = pd.DataFrame(data)

        # Create a CSV file in memory
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        # Create a StreamingResponse to send the CSV file
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment;filename=operations.csv"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()