import requests
import pytest
import allure # импортирую allure и создаю далее feature для отчета
# получаю данные из папки config файла settings
from config.settings import BASE_URL, AUTH, HEADERS, TEST_CONFIGURATION


@allure.feature("Create user")
@allure.story("Create user")
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

    with allure.step("Check Status code"):

        assert response.status_code == TEST_CONFIGURATION["STATUS_CODE_FERST"]

    with allure.step("Check username"):
        assert response.json()["username"] == data["username"]

    with allure.step("Check email"):
        assert response.json()["email"] == data["email"]

    with allure.step("Check roles"):
        assert "subscriber" in response.json()["roles"]

    with allure.step("Create user"):
        CREATED_USER_ID = response.json()["id"]
        print(f"Создан пользователь с ID: {CREATED_USER_ID}")

@allure.feature("Update user")
@allure.story("Update user")
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

    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]
    assert response.json()["name"] == data["name"]
    assert response.json()["first_name"] == data["first_name"]
    assert response.json()["last_name"] == data["last_name"]
    assert response.json()["id"] == 4


@allure.feature("Get user")
@allure.story("Get user")
def test_get_user():

    """Тест для получения информации пользователя"""

    url = f"{BASE_URL}/wp/v2/users/{TEST_CONFIGURATION['TEST_USER_ID']}"

    response = requests.get(url, auth=AUTH, timeout=TEST_CONFIGURATION["TIME_OUT"])
    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"]

    user_data = response.json()
    assert user_data["id"] == TEST_CONFIGURATION['TEST_USER_ID']
    assert user_data["slug"] == "debug_test_user"


@allure.feature("Exist user")
@allure.story("Exist user")
def test_user_exists():

    """Tecт проверка, что пользователь существует"""

    url = f"{BASE_URL}/wp/v2/users/{TEST_CONFIGURATION['TEST_USER_ID']}"
    response = requests.get(url, auth=AUTH)

    assert response.status_code != TEST_CONFIGURATION["STATUS_CODE_NOT_FOUND"], "Пользователь не найден"
    assert response.status_code == TEST_CONFIGURATION["STATUS_CODE"], f"Ошибка сервера: {response.status_code}"


@allure.feature("Delete user")
@allure.story("Delete user")
def test_delete_user():

    """Тест для удаления пользователя"""

    user_id = CREATED_USER_ID or 2

    url = f"{BASE_URL}/wp/v2/users/{user_id}"
    params = {"force": "true", "reassign": "1"} # в параметре указываю 1 для передачи всех данных admin

    response = requests.delete(url, auth=AUTH, headers=HEADERS, params=params)
    assert response.status_code in [TEST_CONFIGURATION["STATUS_CODE"], TEST_CONFIGURATION["STATUS_CODE_ACCEPTED"],
                                    TEST_CONFIGURATION["STATUS_CODE_NO_CONTENT"]], \
        f"Ошибка при удалении: {response.status_code}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])