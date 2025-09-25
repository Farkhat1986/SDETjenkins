import requests
import pytest
# получаю данные из папки config файла settings
from config.settings import BASE_URL, AUTH, HEADERS, TEST_USER_ID



def test_create_user():

    """Тест для создания пользователя"""

    global CREATED_USER_ID

    # создаю сущность Test User8

    url = f"{BASE_URL}/wp/v2/users"
    data = {
        "username": "testuser8",
        "email": "testuser8@example.com",
        "password": "securepassword123",
        "name": "Test User8",
        "roles": ["subscriber"]
    }

    response = requests.post(url, json=data, auth=AUTH, headers=HEADERS)

    assert response.status_code == 201
    assert response.json()["username"] == "testuser8"
    assert response.json()["email"] == "testuser8@example.com"
    assert "subscriber" in response.json()["roles"]

    CREATED_USER_ID = response.json()["id"]
    print(f"Создан пользователь с ID: {CREATED_USER_ID}")


def test_update_user():

    """Тест для обновления информации пользователя"""

    user_id = 4

    url = f"{BASE_URL}/wp/v2/users/{user_id}"
    data = {
        "name": "Updated Test User8",
        "first_name": "Updated8",
        "last_name": "User8"
    }

    response = requests.put(url, json=data, auth=AUTH, headers=HEADERS)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Test User8"
    assert response.json()["first_name"] == "Updated8"
    assert response.json()["last_name"] == "User8"
    assert response.json()["id"] == 4


def test_get_user():

    """Тест для получения информации пользователя"""

    url = f"{BASE_URL}/wp/v2/users/{TEST_USER_ID}"

    response = requests.get(url, auth=AUTH, timeout=10)
    assert response.status_code == 200

    user_data = response.json()
    assert user_data["id"] == TEST_USER_ID
    assert user_data["slug"] == "debug_test_user"


def test_user_exists():

    """Tecт проверка, что пользователь существует"""

    url = f"{BASE_URL}/wp/v2/users/{TEST_USER_ID}"
    response = requests.get(url, auth=AUTH)

    assert response.status_code != 404, "Пользователь не найден"
    assert response.status_code == 200, f"Ошибка сервера: {response.status_code}"


def test_delete_user():

    """Тест для удаления пользователя"""

    user_id = CREATED_USER_ID or 2

    url = f"{BASE_URL}/wp/v2/users/{user_id}"
    params = {"force": "true", "reassign": "1"} # в параметре указываю 1 для передачи всех данных admin

    response = requests.delete(url, auth=AUTH, headers=HEADERS, params=params)
    assert response.status_code in [200, 202, 204], f"Ошибка при удалении: {response.status_code}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])