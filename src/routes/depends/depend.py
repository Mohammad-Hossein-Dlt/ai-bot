from src.infra.context.app_context import AppContext
from typing import Callable, Any

Depends: Callable[..., Any] = lambda: None
inject: Callable[..., Any] = lambda func: func

if AppContext.platform == "Api":
    from fastapi import Depends as _Depends
    Depends = _Depends
else:
    from fast_depends import Depends as _Depends, inject as _inject
    Depends = _Depends
    inject = _inject