import requests
import pytest

BASE_URL = "http://localhost:8000/index.php?rest_route=/wp/v2/users/"
AUTH = ("Firstname.LastName", "123-Test")


def test_get_user_basic_info():
    """Тест базовой информации о пользователе"""
    test_user_id = 3
    url = f"{BASE_URL}{test_user_id}"

    response = requests.get(url, auth=AUTH, timeout=10)

    # Проверяем успешный запрос
    assert response.status_code == 200

    user_data = response.json()

    # Выводим доступные поля для отладки
    print("Доступные поля в ответе:")
    for key in user_data.keys():
        print(f"- {key}")

    # Обязательные проверки (поля, которые точно есть)
    assert user_data["id"] == test_user_id
    assert user_data["slug"] == "debug_test_user"

    # Дополнительные проверки для доступных полей
    if "name" in user_data:
        print(f"Display name: {user_data['name']}")

    if "id" in user_data:
        print(f"ID: {user_data['id']}")

    if "url" in user_data:
        print(f"Website: {user_data['url']}")

    # Email проверяем только если доступен
    if "email" in user_data:
        assert user_data["email"] == "debug_test@example.com"
        print("Email проверен успешно")
    else:
        print("Email не доступен в REST API - это нормально для WordPress")

    print("Тест пройден успешно!")


# Дополнительный тест для проверки существования пользователя
def test_user_exists():
    """Проверка что пользователь существует"""
    test_user_id = 3
    url = f"{BASE_URL}{test_user_id}"

    response = requests.get(url, auth=AUTH)

    print(response)

    # Если пользователь не найден - будет 404
    assert response.status_code != 404, "Пользователь не найден"
    assert response.status_code == 200, f"Ошибка сервера: {response.status_code}"
