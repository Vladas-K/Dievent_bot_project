import os

import pytest
from dotenv import load_dotenv
from rest_framework.test import APIClient

from ..models import Event, TelegramUser

# Загружаем токен из .env
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_token():
    client = APIClient()
    client.credentials(HTTP_BOT_TOKEN=BOT_TOKEN)  # Добавляем токен в заголовок
    return client


@pytest.fixture
def event():
    return Event.objects.create(
        title="Django Meetup",
        description="Встреча Django-разработчиков",
        date_time="2025-05-01T18:00:00Z",
        location="Москва",
        company_info="Django Russia",
        dress_code="Casual"
    )


@pytest.fixture
def telegram_user():
    return TelegramUser.objects.create(
        user_id="12345",
        username="testuser",
        first_name="Test",
        last_name="User"
    )


def test_get_events(api_client, event):
    response = api_client.get("/api/events/")
    assert response.status_code == 200
    assert response.data[0]["title"] == "Django Meetup"


def test_get_users(api_client_with_token, telegram_user):
    response = api_client_with_token.get("/api/users/")
    assert response.status_code == 200
    assert response.data[0]["user_id"] == "12345"


def test_create_telegram_user(api_client_with_token):
    payload = {
        "user_id": "54321",
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "subscribed": True
    }
    response = api_client_with_token.post("/api/users/", payload, format="json")
    assert response.status_code == 201
    assert TelegramUser.objects.filter(user_id="54321").exists()


def test_create_existing_telegram_user(api_client_with_token, telegram_user, caplog):
    payload = {
        "user_id": "12345",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "subscribed": True
    }
    with caplog.at_level("WARNING"):
        response = api_client_with_token.post("/api/users/", payload, format="json")
        assert response.status_code == 400
        assert "уже существует" in caplog.text
