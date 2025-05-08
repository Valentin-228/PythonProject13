
from constants import SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD
from tests.api.api_manager import ApiManager
import uuid

class TestMoviesAPI:

    def test_get_movies(self, api_manager: ApiManager):
        """
        Тест на получение списка фильмов.
        """
        response = api_manager.movies_api.get_movies(expected_status=200)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        response_data = response.json()

        # Проверяем, что в ответе есть ключ 'movies' с не пустым списком
        assert "movies" in response_data, "Expected 'movies' in response data"
        assert isinstance(response_data["movies"], list), "'movies' should be a list"
        assert len(response_data["movies"]) > 0, "Movies list should not be empty"

    def test_get_movies_price(self, api_manager: ApiManager):
        """
        Тест: фильтрация фильмов по цене (minPrice, maxPrice).
        """
        params = {
            "minPrice": 50,
            "maxPrice": 150
        }
        response = api_manager.movies_api.get_movies(params=params, expected_status=200)
        data = response.json()

        for movie in data.get("movies", {}):
            assert 50 <= movie.get("price", None) <= 150, f"Movie price {movie['price']} is out of range"

    def test_create_movie(self, api_manager: ApiManager, super_admin_token: str):
        """
        Тест на создание фильма.
        """
        unique_name = f"Test Movie {uuid.uuid4()}"
        movie_data = {
            "name": unique_name,
            "imageUrl": "https://example.com/movie.jpg",
            "price": 100,
            "description": "A test movie.",
            "location": "MSK",
            "published": True,
            "genreId": 1
        }

        response = api_manager.movies_api.create_movie(movie_data, super_admin_token, expected_status=201)

        response_data = response.json()

        # Проверяем, что в ответе есть 'id' (т.е. фильм успешно создан)
        assert "id" in response_data, "Movie ID is missing in the response"
        assert isinstance(response_data["id"], int), "Movie ID should be an integer"

    def test_create_movie_without_image(self, api_manager: ApiManager, super_admin_token: str):
        """
        Создание фильма только с обязательными полями.
        """
        unique_name = f"Test Minimal Movie {uuid.uuid4()}"
        movie_data = {
            "name": unique_name,
            "price": 100,
            "description": "Минимальный набор полей",
            "location": "MSK",
            "published": False,
            "genreId": 1
        }

        response = api_manager.movies_api.create_movie(movie_data, super_admin_token, expected_status=201)
        response_data = response.json()

        assert response.status_code == 201
        assert "id" in response_data
        assert response_data["name"] == unique_name

    def test_delete_movie(self, api_manager: ApiManager, super_admin_token: str):
        """
        Тест на удаление фильма.
        """
        unique_name = f"Test Movie {uuid.uuid4()}"
        movie_data = {
            "name": unique_name,
            "imageUrl": "https://example.com/movie.jpg",
            "price": 100,
            "description": "A movie to delete.",
            "location": "MSK",
            "published": True,
            "genreId": 1
        }

        # Создаем фильм
        create_response = api_manager.movies_api.create_movie(movie_data, super_admin_token, expected_status=201)
        movie_id = create_response.json().get("id")

        # Удаляем фильм
        delete_response = api_manager.movies_api.delete_movie(movie_id, super_admin_token, expected_status=200)


        # Проверяем, что фильм был удален, делая запрос на получение фильма
        get_response = api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert get_response.status_code == 404, f"Expected 404, got {get_response.status_code}"
        response_data = get_response.json()

        # Проверяем, что в ответе есть сообщение об ошибке
        assert "message" in response_data, "Expected 'message' in response data"
        assert response_data["message"] == "Фильм не найден", f"Expected 'Фильм не найден', but got {response_data['message']}"