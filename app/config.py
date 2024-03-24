from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = Field('', env='DB_HOST')
    DB_PORT: int = Field(121, env='DB_PORT')
    DB_USER: str = Field('', env='DB_USER')
    DB_PASSWORD: str = Field('', env='DB_PASSWORD')
    DB_NAME: str = Field('', env='DB_NAME')
    SECRET_KEY: str = Field(env='SECRET_KEY')
    ALGORITHM: str = Field(env='ALGORITHM')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
