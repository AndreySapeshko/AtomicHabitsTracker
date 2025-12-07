import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create_user(
        email="TEST@EXAMPLE.COM",
        password="password123",
    )

    assert user.email == "TEST@example.com"  # Django нормализует домен
    assert user.check_password("password123")
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_without_email_raises_error():
    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="123456")


@pytest.mark.django_db
def test_create_superuser_success():
    superuser = User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass",
    )

    assert superuser.is_staff is True
    assert superuser.is_superuser is True
    assert superuser.check_password("adminpass")


@pytest.mark.django_db
def test_create_superuser_without_staff_flag_raises_error():
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass",
            is_staff=False,
        )


@pytest.mark.django_db
def test_create_superuser_without_superuser_flag_raises_error():
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass",
            is_superuser=False,
        )


@pytest.mark.django_db
def test_user_str_returns_email():
    user = User.objects.create_user(
        email="strtest@example.com",
        password="123456",
    )

    assert str(user) == "strtest@example.com"
