from fastapi import FastAPI
from .app_lifespan import lifespan
# from fastapi.middleware import Middleware
# from src.infra.middlewares.logging_middleware import LoggingMiddleware
# from src.infra.middlewares.prometheus_middleware import PrometheusMiddleware

# middlewares = [
#     Middleware(LoggingMiddleware),
#     Middleware(PrometheusMiddleware),
# ]

app: FastAPI = FastAPI(
    root_path="/api-service",
    lifespan=lifespan,
    # middleware=middlewares,
)