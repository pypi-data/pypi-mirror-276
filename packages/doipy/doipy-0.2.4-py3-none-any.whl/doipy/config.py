from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='doipy_')

    # Cordra Testbed Data Repo
    ip: str = '141.5.106.77'
    prefix: str = '21.T11967'
    target_id: str = '21.T11967/service'
    port: int = 9000


settings = Settings()
