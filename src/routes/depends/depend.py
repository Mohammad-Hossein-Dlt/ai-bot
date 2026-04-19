from src.infra.context.app_context import AppContext
from typing import Callable, Any

Depends: Callable[..., Any] = lambda: None
inject: Callable[..., Any] = lambda func: func

if AppContext.run_platform == "api":
    from fastapi import Depends as _Depends
    Depends = _Depends
elif AppContext.run_platform == "bot":
    from fast_depends import Depends as _Depends, inject as _inject
    Depends = _Depends
    inject = _inject