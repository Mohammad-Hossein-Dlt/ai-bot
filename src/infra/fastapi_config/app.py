from fastapi import FastAPI
from fastapi_swagger import patch_fastapi
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
    docs_url=None,
    swagger_ui_oauth2_redirect_url=None,
    # middleware=middlewares,
)
patch_fastapi(app,docs_url="/swagger")