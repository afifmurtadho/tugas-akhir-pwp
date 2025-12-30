import os
from dotenv import load_dotenv

load_dotenv('.flaskenv')

class Config:
    SECRET_KEY = "zoo-management-secret-key-2025"

    DB_HOST = os.getenv("DB_HOST")
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
