"""
Dynamic settings loader based on DJANGO_ENV variable.

Options:
- dev  → atomic_habits_tracker.settings.dev
- prod → atomic_habits_tracker.settings.prod
- ci   → atomic_habits_tracker.settings.ci
"""

import os

env = os.environ.get("DJANGO_ENV", "dev").lower()

if env == "prod":
    from .prod import *
elif env == "ci":
    from .ci import *
else:
    from .dev import *
