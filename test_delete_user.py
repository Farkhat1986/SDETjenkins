import requests
import pytest

BASE_URL = "http://localhost:8000/index.php?rest_route=" # передаем url
AUTH = ("Firstname.LastName", "123-Test")  # передаем аутентификацию админа имя и пароль для входа
HEADERS = {"Content-Type": "application/json"} # передаем что хотим взять


def test_simple_delete():
    """Простой тест удаления"""
    user_id = 2

    # Правильный URL формат
    url = f"{BASE_URL}/wp/v2/users/{user_id}"
    params = {
        "force": "true",
        "reassign": "1"
    }

    response = requests.delete(url, auth=AUTH, headers=HEADERS, params=params)

    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    # Более гибкая проверка
    if response.status_code in [200, 202, 204]:
        print("Удаление успешно")
    elif response.status_code == 404:
        print("Пользователь не найден")
    else:
        print(f"Ошибка: {response.status_code}")