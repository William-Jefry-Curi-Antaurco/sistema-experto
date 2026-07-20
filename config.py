import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def required_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        raise RuntimeError(
            f"Falta la variable de entorno obligatoria: {name}"
        )

    return value.strip()


class Config:
    SECRET_KEY = required_env("SECRET_KEY")

    DB_HOST = required_env("DB_HOST")
    DB_PORT = required_env("DB_PORT")
    DB_DATABASE = required_env("DB_DATABASE")
    DB_USERNAME = required_env("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    _DB_USERNAME_ENCODED = quote_plus(DB_USERNAME)
    _DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{_DB_USERNAME_ENCODED}:"
        f"{_DB_PASSWORD_ENCODED}"
        f"@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
        "?charset=utf8mb4"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }