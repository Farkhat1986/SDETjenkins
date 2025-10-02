# Сюда вынес переменные для использывания в тестах

BASE_URL = "http://wordpress:80/wp-json" #"http://wordpress:80/index.php?rest_route="
AUTH = ("Firstname.LastName", "123-Test")
HEADERS = {"Content-Type": "application/json"}

TEST_CONFIGURATION = {
    "TEST_USER_ID": 1,
    "TIME_OUT": 10,
    "STATUS_CODE": 200,
    "STATUS_CODE_FIRST": 201,
    "STATUS_CODE_NOT_FOUND": 404,
    "STATUS_CODE_ACCEPTED": 202,
    "STATUS_CODE_NO_CONTENT": 204,
}