import requests
import pytest

BASE_URL = "http://localhost:8000/index.php?rest_route="
AUTH = ("Firstname.LastName", "123-Test")
HEADERS = {"Content-Type": "application/json"}

class TestUsersCRUD:
    BASE_URL = "http://localhost:8000/index.php?rest_route="
    AUTH = ("Firstname.LastName", "123-Test")
    HEADERS = {"Content-Type": "application/json"}

    @pytest.fixture
    def test_user_id(self):

        url = f"{self.BASE_URL}/wp/v2/users"
        data = {
            "username": "testuser_crud",
            "email": "crud_test@example.com",
            "password": "testpass123",
            "name": "CRUD Test User",
            "roles": ["subscriber"]
        }

        response = requests.post(url, json=data, auth=self.AUTH, headers=self.HEADERS)
        assert response.status_code == 201
        user_id = response.json()["id"]

        yield user_id


        requests.delete(
            f"{self.BASE_URL}/wp/v2/users/{user_id}?force=true",
            auth=self.AUTH
        )

    def test_create_user(self):
        """Позитивный тест на создание нового пользователя"""
        url = f"{BASE_URL}/wp/v2/users"
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "name": "Test User",
            "roles": ["subscriber"]
        }

        response = requests.post(url, json=data, auth=AUTH, headers=HEADERS)

        # Проверки
        assert response.status_code == 201
        assert response.json()["username"] == "testuser"
        assert response.json()["email"] == "testuser@example.com"
        assert "subscriber" in response.json()["roles"]

        return response.json()["id"]  # Возвращаем ID для следующих тестов

    def test_get_user(test_user_id):
        """Позитивный тест на получение информации о пользователе"""
        url = f"{BASE_URL}/wp/v2/users/{test_user_id}"

        response = requests.get(url, auth=AUTH, headers=HEADERS)

        # Проверки
        assert response.status_code == 200
        assert response.json()["id"] == test_user_id
        assert response.json()["username"] == "testuser"
        assert response.json()["email"] == "testuser@example.com"

    def test_update_user(user_id):
        """Позитивный тест на обновление информации о пользователе"""
        url = f"{BASE_URL}/wp/v2/users/{user_id}"
        data = {
            "name": "Updated Test User",
            "first_name": "Updated",
            "last_name": "User"
        }

        response = requests.put(url, json=data, auth=AUTH, headers=HEADERS)

        # Проверки
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Test User"
        assert response.json()["first_name"] == "Updated"
        assert response.json()["last_name"] == "User"

    def test_delete_user(user_id):
        """Позитивный тест на удаление пользователя"""
        url = f"{BASE_URL}/wp/v2/users/{user_id}?force=true"

        response = requests.delete(url, auth=AUTH, headers=HEADERS)

        # Проверки
        assert response.status_code == 200
        assert response.json()["deleted"] == True

        # Проверяем, что пользователь действительно удален
        get_response = requests.get(f"{BASE_URL}/wp/v2/users/{user_id}", auth=AUTH)
        assert get_response.status_code == 404
