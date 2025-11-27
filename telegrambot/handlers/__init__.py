from .basic import router as basic_router
from .callbacks import router as callback_router
from .profile import router as profile_router


def get_handlers():
    return [
        basic_router,
        callback_router,
        profile_router,
    ]
