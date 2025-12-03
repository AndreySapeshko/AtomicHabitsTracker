import factory

from habit_instances.models import HabitInstance, HabitInstanceStatus


class HabitInstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HabitInstance

    habit = factory.SubFactory("habits.tests.factory.HabitFactory")
    scheduled_datetime = factory.Faker("date_time_this_year")
    confirm_deadline = factory.Faker("date_time_this_year")
    fix_deadline = factory.Faker("date_time_this_year")
