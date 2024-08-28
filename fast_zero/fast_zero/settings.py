from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        # se vc tá importando mais variáveis aqui
        # do que vai realmente usar do .env,
        # tu coloca esse parâmetro extra
        extra='ignore',
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int
