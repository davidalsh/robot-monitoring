from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.api.robots import router as robots_router
from app.domain.common.exceptions import DomainException
from logger import get_logger

app = FastAPI()

logger = get_logger()


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "code": exc.code, "status": exc.status_code},
    )


app.include_router(robots_router)
