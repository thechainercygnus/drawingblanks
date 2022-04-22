import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from logger import _setup_logging

log = _setup_logging()

DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_PATH = os.getenv("DB_PATH", "./drawingblanks.db")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "drawingblanks")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

if DB_TYPE == 'mysql':
    log.info("Using MySQL for Database")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    CONNECT_ARGS = {"charset": "utf8"}
elif DB_TYPE == "sqlite":
    log.info("Using SQLite3 for Database")
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    CONNECT_ARGS = {"check_same_thread": False}
else:
    log.error(
        "Database %s is not supported, please set the env DB_TYPE to 'sqlite' or 'mysql'", DB_TYPE
    )

engine = create_engine(DATABASE_URL, connect_args=CONNECT_ARGS)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
