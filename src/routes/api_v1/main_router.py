from fastapi import APIRouter

from src.routes.api_v1.bot_settings._router import router as bot_settings_router
from src.routes.api_v1.discount_code._router import router as discount_code_router
from src.routes.api_v1.meta_data._router import router as meta_data_router
from src.routes.api_v1.payment._router import router as payment_router
from src.routes.api_v1.token_settings._router import router as token_settings_router
from src.routes.api_v1.category._router import router as category_router
from src.routes.api_v1.user._router import router as user_router

from src.routes.api_v1.health_check._router import router as health_check_router
# from src.routes.api_v1.metrics._router import router as metrics_router

ROUTE_PREFIX_VERSION_API = "/api/v1"

main_router_v1 = APIRouter()

main_router_v1.include_router(bot_settings_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(token_settings_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(meta_data_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(category_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(discount_code_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(payment_router, prefix=ROUTE_PREFIX_VERSION_API)
main_router_v1.include_router(user_router, prefix=ROUTE_PREFIX_VERSION_API)

main_router_v1.include_router(health_check_router, prefix=ROUTE_PREFIX_VERSION_API)
# main_router_v1.include_router(metrics_router, prefix=ROUTE_PREFIX_VERSION_API)
