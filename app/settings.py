from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    DATABASE_SCHEME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_DB: str
    DATABASE_PORT: int
    DATABASE_SERVER: str

    @property
    def database_url(self) -> str:
        return (
            f'{self.DATABASE_SCHEME}://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@'
            f'{self.DATABASE_SERVER}:{self.DATABASE_PORT}/{self.DATABASE_DB}'
        )


class AppSettings(BaseSettings):
    LOCAL: str


class Settings(DatabaseSettings, AppSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


settings = Settings()  # type: ignore
