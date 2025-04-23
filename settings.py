from pydantic_settings import BaseSettings


class Bot(BaseSettings):
    
    WP_USERNAME: str
    WP_PASSWORD: str

    GSHEETS_CREDENTIALS_JSON: str
    PATH_ALL_DOMAINS_JSON: str
    SHEETS_NAME: str

    class Config:
        env_file = '.env'
        extra = 'ignore'

class Settings:

    bot = Bot()

settings = Settings()
