from repositories.redis.redis import redis


class RedisSessionRepository:
    def __init__(self):
        self.__SESSION_KEY = "session"
        self.__SELECTED_DATABASE_KEY = "selected_database"
        self.__SESSION_DURATION = 60 * 60  # 15 seconds

    def get_selected_database(self) -> str:
        return redis.get(self.__SELECTED_DATABASE_KEY).decode("utf-8")

    def set_selected_database(self, database: str):
        redis.set(self.__SELECTED_DATABASE_KEY, database)

    def has_session(self) -> bool:
        return redis.exists(self.__SESSION_KEY)

    def add_session(self) -> None:
        redis.setex(
            name=self.__SESSION_KEY, value="active", time=self.__SESSION_DURATION
        )

    def remove_session(self) -> None:
        redis.delete(self.__SESSION_KEY)
