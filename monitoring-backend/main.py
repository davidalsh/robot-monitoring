from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.robots import router as robots_router
from app.domain.common.exceptions import DomainException
from cli_attr import LOG_LEVEL, REFRESH_FREQUENCY_HZ
from logger import get_logger

app = FastAPI()

logger = get_logger()
logger.warning(f"WARNING:  RUNNING APP WITH {REFRESH_FREQUENCY_HZ=} AND {LOG_LEVEL=}")


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "code": exc.code, "status": exc.status_code},
    )


origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(robots_router)
