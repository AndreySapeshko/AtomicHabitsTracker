from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Habit


@receiver(post_save, sender=Habit)
def clear_habit_cache(sender, instance, **kwargs):
    pk = instance.id
    cache.delete(f"habit_stats_{pk}")
    cache.delete(f"habit_details_{pk}")
