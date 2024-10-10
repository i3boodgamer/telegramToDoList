from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BOT_TOKEN: str = "7957614470:AAG5cvl0MaRk7j3BPrB9i5bFmlsmnfP49B4"
    DB_URL: str = "sqlite:///bot_database.db"

    class Config:
        env_file = ".env"


config = Config()
