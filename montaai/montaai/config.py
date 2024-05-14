import os

class Config:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "postgresql://username:password@localhost/dbname")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    REDIS_DB = os.environ.get("REDIS_DB", 0)
