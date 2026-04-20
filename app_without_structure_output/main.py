from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app_without_structure_output.helpers.exceptions import ExceptionHandlers
from app_without_structure_output.helpers.config import (
    API_VERSION,
    API_BASE_NAME
)
from app_without_structure_output.routers import chat


app = FastAPI()

app.add_exception_handler(HTTPException, ExceptionHandlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, ExceptionHandlers.validation_exception_handler)
app.add_exception_handler(ValueError, ExceptionHandlers.value_error_handler)
app.add_exception_handler(Exception, ExceptionHandlers.global_exception_handler)


app.include_router(chat.router, prefix=f'/{API_BASE_NAME}/{API_VERSION}')

@app.get("/")
def read_root():
    return {"Hello": "World"}