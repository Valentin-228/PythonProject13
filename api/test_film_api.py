from api.api_manager import ApiManager
import uuid

class TestMoviesAPI:

    def test_get_movies(self, api_manager: ApiManager):
        """
        Тест на получение списка фильмов.
        """
        response = api_manager.movies_api.get_movies(expected_status=200)
        response_data = response.json()

        # Проверяем, что в ответе есть ключ 'movies' с не пустым списком
        assert "movies" in response_data, "Expected 'movies' in response data"
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

    def test_create_movie(self, api_manager: ApiManager, valid_movie_data, super_admin_token: str):
        """
        Тест на создание фильма.
        """
        response = api_manager.movies_api.create_movie(valid_movie_data, super_admin_token, expected_status=201)
        response_data = response.json()
        # Проверяем, что в ответе есть 'id' (т.е. фильм успешно создан)
        assert "id" in response_data

    def test_create_movie_without_image(self, api_manager: ApiManager, min_valid_movie_data, super_admin_token: str):
        """
        Создание фильма только с обязательными полями.
        """
        response = api_manager.movies_api.create_movie(min_valid_movie_data, super_admin_token, expected_status=201)
        response_data = response.json()
        assert "id" in response_data

    def test_delete_movie(self, api_manager: ApiManager, valid_movie_data, super_admin_token: str):
        """
        Тест на удаление фильма.
        """
        # Создаем фильм
        create_response = api_manager.movies_api.create_movie(valid_movie_data, super_admin_token, expected_status=201)
        movie_id = create_response.json().get("id")
        # Удаляем фильм
        delete_response = api_manager.movies_api.delete_movie(movie_id, super_admin_token, expected_status=200)

        # Проверяем, что фильм был удален, делая запрос на получение фильма
        get_response = api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
        response_data = get_response.json()

        # Проверяем, что в ответе есть сообщение об ошибке
        assert "message" in response_data, "Expected 'message' in response data"

    def test_create_movie_invalid(self, api_manager: ApiManager, invalid_movie_data, super_admin_token: str):
        """
        Тест на создание фильма.
        """
        response = api_manager.movies_api.create_movie(invalid_movie_data, super_admin_token, expected_status=400)
        assert response.status_code == 400
        response_data = response.json()


    def test_delete_invalid_movie(self, api_manager: ApiManager, super_admin_token: str):
        """
        Тест на удаление фильма.
        """
        # Несуществующий фильм

        none_movie_id = 11111111
        # Удаляем фильм
        delete_response = api_manager.movies_api.delete_movie(none_movie_id, super_admin_token, expected_status=404)
        assert delete_response.status_code == 404

