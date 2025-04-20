from repositories.redis import redis


class SessionRepository:
    def __init__(self):
        self.__SESSION_KEY = "session"
        self.__SESSION_DURATION = 60 * 60  # 15 seconds

    def has_session(self) -> bool:
        return redis.exists(self.__SESSION_KEY)

    def add_session(self) -> None:
        redis.setex(
            name=self.__SESSION_KEY, value="active", time=self.__SESSION_DURATION
        )

    def remove_session(self) -> None:
        redis.delete(self.__SESSION_KEY)
