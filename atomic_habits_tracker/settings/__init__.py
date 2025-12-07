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
    print("✅ DJANGO SETTINGS: PROD")
    from .prod import *
elif env == "ci":
    print("✅ DJANGO SETTINGS: CI")
    from .ci import *
else:
    print("✅ DJANGO SETTINGS: DEV")
    from .dev import *
