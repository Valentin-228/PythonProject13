from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI


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


