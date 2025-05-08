
from film_generator.film_generator import DataGenerator
import pytest
import requests
from api.api_manager import ApiManager
from constants import BASE_URL
from constants import SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session=session, base_url=BASE_URL)




@pytest.fixture(scope="module")
def super_admin_token(api_manager: ApiManager):
    """
    Фикстура для получения токена SUPER_ADMIN.
    """
    login_data = {
        "email": SUPER_ADMIN_USERNAME,
        "password": SUPER_ADMIN_PASSWORD
    }
    login_response = api_manager.auth_api.login_user(login_data, expected_status=200)
    token = login_response.json().get("accessToken")
    return token

@pytest.fixture(scope="module")
def authenticate(self, user_creds):
    login_data = {
        "email": user_creds[0],
        "password": user_creds[1]
    }

    response = self.login_user(login_data)
    # Извлечение токена из ответа
    response_json = response.json()
    if "accessToken" not in response_json:
        raise KeyError("Access token is missing in the response")

    token = response_json["accessToken"]
    self._update_session_headers(authorization=f"Bearer {token}")

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture
def valid_movie_data():
    return {
        "name": DataGenerator.generate_movie_name(),
        "imageUrl": DataGenerator.generate_image_url(),
        "price": DataGenerator.generate_price(),
        "description": DataGenerator.generate_description(),
        "location": DataGenerator.generate_location(),
        "published": DataGenerator.generate_published(),
        "genreId": DataGenerator.generate_genre_id()
    }


@pytest.fixture
def invalid_movie_data():
    return {
        "name": 123,
        "imageUrl": DataGenerator.generate_image_url(),
        "price": DataGenerator.generate_price(),
        "description": DataGenerator.generate_description(),
        "location": "Москва",
        "published": DataGenerator.generate_published(),
        "genreId": DataGenerator.generate_genre_id()
    }

@pytest.fixture
def min_valid_movie_data():
    return {
        "name": DataGenerator.generate_movie_name(),
        "price": DataGenerator.generate_price(),
        "description": DataGenerator.generate_description(),
        "location": DataGenerator.generate_location(),
        "published": DataGenerator.generate_published(),
        "genreId": DataGenerator.generate_genre_id()
    }

