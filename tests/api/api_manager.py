from constants import SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD
from tests.api.auth_api import AuthAPI
from tests.api.movies_api import MoviesAPI
import requests

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session, base_url):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.movies_api = MoviesAPI(session)

        # Метод для входа пользователя (login)

    def authenticate(self):
        login_data = {
            "email": SUPER_ADMIN_USERNAME,
            "password": SUPER_ADMIN_PASSWORD
        }
        response = self.auth_api.login_user(login_data)
        token = response.json().get("accessToken")
        if not token:
            raise KeyError("Access token is missing in the response")
        self._update_session_headers(authorization=f"Bearer {token}")


    class MoviesAPI:
        def __init__(self, base_url):
            self.base_url = base_url

        def get_movies(self, expected_status):
            url = f"{self.base_url}/movies"
            response = requests.get(f"{self.base_url}/movies")
            return response

        def create_movie(self, movie_data, token, expected_status):

            response = requests.post(f"{self.base_url}/movies", json=movie_data, headers=headers)
            return response

        def delete_movie(self, movie_id, token, expected_status):

            response = requests.delete(f"{self.base_url}/movies/{movie_id}", headers=headers)
            return response