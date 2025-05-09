
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




@pytest.fixture(scope="session")
def auth_session(api_manager):
    api_manager.auth_api.authenticate()
    return api_manager

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

