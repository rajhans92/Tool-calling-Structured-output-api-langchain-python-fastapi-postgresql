from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.helpers.exceptions import ExceptionHandlers



app = FastAPI()

app.add_exception_handler(HTTPException, ExceptionHandlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, ExceptionHandlers.validation_exception_handler)
app.add_exception_handler(ValueError, ExceptionHandlers.value_error_handler)
app.add_exception_handler(Exception, ExceptionHandlers.global_exception_handler)


@app.get("/")
def read_root():
    return {"Hello": "World"}