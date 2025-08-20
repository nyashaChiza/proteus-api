from decouple import config

class Settings(object):
    DATABASE_URL:str = config('DATABASE_URL','sqlite:////var/data/proteus.db')
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = config("DEBUG", default=False, cast=bool)
    SECRET_KEY: str = config('SECRET_KEY', 'jgcxkvhfxtrzrzrztcxryxycvjvj')
    
    class Config:
        env_file = ".env"

settings = Settings()