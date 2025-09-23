import requests
import pytest

BASE_URL = "http://localhost:8000/index.php?rest_route=" # передаем url
AUTH = ("Firstname.LastName", "123-Test")  # передаем аутентификацию админа имя и пароль для входа
HEADERS = {"Content-Type": "application/json"} # передаем что хотим взять


def test_update_user():
    user_id = 1
    """Позитивный тест на обновление информации о пользователе"""
    url = f"{BASE_URL}/wp/v2/users/{user_id}"
    data = {
        "name": "Updated Test Useres",
        "first_name": "Updated",
        "last_name": "User",
        "user_id": 1
    } # сюда передаем данные, которые затем хотим взять с response по запросу requests

    response = requests.put(url, json=data, auth=AUTH, headers=HEADERS)

    # Проверки
    assert response.status_code == 200 # проверяем что вошли
    assert response.json()["name"] == "Updated Test Useres" # сравниваем name
    assert response.json()["first_name"] == "Updated" # сравниваем first_name
    assert response.json()["last_name"] == "User" # сравниваем last_name
    assert response.json()["id"] == 1 # сравниваем id

    print(data) # для печати

    # в базе данных обновляется на Updated Test Useres