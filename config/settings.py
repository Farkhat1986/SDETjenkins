# Сюда вынес переменные для использывания в тестах

BASE_URL = "http://localhost:8000/index.php?rest_route="
AUTH = ("Firstname.LastName", "123-Test")
HEADERS = {"Content-Type": "application/json"}

TEST_CONFIGURATION = {
    "CREATED_USER_ID": None,
    "TEST_USER_ID": 3,
    "TIME_OUT": 10,
    "STATUS_CODE": 200,
    "STATUS_CODE_FERST": 201,
    "STATUS_CODE_NOT_FOUND": 404,
    "STATUS_CODE_ACCEPTED": 202,
    "STATUS_CODE_NO_CONTENT": 204,
}