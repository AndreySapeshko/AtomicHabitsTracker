from .basic import router as basic_router
from .bind import router as bind_router
from .callbacks import router as callback_router
from .habits import router as habits_router
from .help import router as help_router
from .profile import router as profile_router
from .today import router as today_router


def get_handlers():
    return [
        bind_router,
        basic_router,
        callback_router,
        profile_router,
        habits_router,
        today_router,
        help_router,
    ]
