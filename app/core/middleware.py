import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from core.config import get_settings

settings = get_settings()
logger = logging.getLogger("architech")

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        logger.info("→ %s %s", request.method, request.url.path)
        response = await call_next(request)
        elapsed = time.time() - start
        response.headers["X-Process-Time"] = f"{elapsed:.4f}"
        logger.info("← %s %s → %s (%.3fs)", request.method, request.url.path, response.status_code, elapsed)
        return response


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]
