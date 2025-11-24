from celery import shared_task

from habit_instances.services import create_instances_for_all_habits


@shared_task
def generate_daily_instances():
    created = create_instances_for_all_habits()
    return len(created)
