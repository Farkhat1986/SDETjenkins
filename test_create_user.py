import requests
import pytest

BASE_URL = "http://localhost:8000/index.php?rest_route="
AUTH = ("Firstname.LastName", "123-Test")
HEADERS = {"Content-Type": "application/json"}

def test_create_user():
        """Позитивный тест на создание нового пользователя"""
        url = f"{BASE_URL}/wp/v2/users"
        data = {
            "username": "testuser6",
            "email": "testuser6@example.com",
            "password": "securepassword123",
            "name": "Test User6",
            "roles": ["subscriber"]
        }

        response = requests.post(url, json=data, auth=AUTH, headers=HEADERS)

        # Проверки
        assert response.status_code == 201
        assert response.json()["username"] == "testuser6"
        assert response.json()["email"] == "testuser6@example.com"
        assert "subscriber" in response.json()["roles"]