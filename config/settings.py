from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    DATABASE_HOST =  os.getenv('DATABASE_HOST')
    DATABASE_NAME =  os.getenv('DATABASE_NAME')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    DATABASE_URL = os.getenv('DATABASE_URL')


settings = Settings()