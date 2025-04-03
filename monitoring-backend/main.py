from starlette.responses import JSONResponse

from fastapi import FastAPI, Request
from app.domain.common.exceptions import DomainException

app = FastAPI()


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message, "code": exc.code},
    )
