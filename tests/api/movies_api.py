from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL

class MoviesAPI(CustomRequester):
    """
    Класс для работы с API фильмов.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)

    def get_movies(self, params=None, expected_status=200):
        """
        Получение списка фильмов с возможностью фильтрации.
        :param params: Словарь с query-параметрами (например, фильтрация по цене, жанру и т.д.).
        :param expected_status: Ожидаемый статус-код ответа.
        """
        return self.send_request(
            method="GET",
            endpoint="/movies",
            params=params,
            expected_status=expected_status,

        )

    def get_movie_by_id(self, movie_id, expected_status=200):
        """
        Получение данных о фильме по его ID.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код ответа.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, movie_data, token, expected_status=201):
        """
        Создание нового фильма.
        :param movie_data: Данные для создания фильма.
        :param token: JWT токен для авторизации.
        :param expected_status: Ожидаемый статус-код ответа.
        """
        self.headers["Authorization"] = f"Bearer {token}"
        return self.send_request(
            method="POST",
            endpoint="movies",
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, token, expected_status=204):
        """
        Удаление фильма по ID.
        :param movie_id: ID фильма.
        :param token: JWT токен для авторизации.
        :param expected_status: Ожидаемый статус-код ответа.
        """
        self.headers["Authorization"] = f"Bearer {token}"
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )
