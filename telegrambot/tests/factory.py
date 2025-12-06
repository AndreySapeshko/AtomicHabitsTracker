import factory

from users.model_files.profile import TelegramProfile

class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TelegramProfile

    user = factory.SubFactory("users.tests.factory.UserFactory")
    chat_id = factory.Sequence(lambda n: f"{330+n}")
    username = "Tester"
    timezone = "UTC"
    is_active = True
    binding_code = factory.Sequence(lambda n: f"A123b7{n}9")