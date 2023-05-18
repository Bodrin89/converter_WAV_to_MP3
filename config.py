import os


class Config:
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:" \
                              f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" \
                              f"{POSTGRES_PORT}/{POSTGRES_DB}"
