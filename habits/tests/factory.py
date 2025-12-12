import factory

from habits.models import Habit


class HabitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Habit

    user = factory.SubFactory("users.tests.factory.UserFactory")
    action = "Test Action"
    place = "home"
    time_of_day = "08:00"
    is_pleasant = False
    reward_text = "Text reward"
    periodicity_days = 1
    repeat_limit = 21
    is_active = True
