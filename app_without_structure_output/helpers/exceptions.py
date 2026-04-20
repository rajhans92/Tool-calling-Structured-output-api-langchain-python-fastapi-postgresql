from fastapi import Request, HTTPException, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ExceptionHandlers:

    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "type": "HTTPException"
            }
        )

    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "Invalid request data",
                "details": exc.errors(),
                "type": "RequestValidationError"
            }
        )

    @staticmethod
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content={
                "error": str(exc),
                "type": "ValueError"
            }
        )

    @staticmethod
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "details": str(exc),
                "type": "GeneralException"
            }
        )