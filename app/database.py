import time
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="socialApp",
#             user="postgres",
#             password="Ml050796.", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB connction was soccessful!")
#         break
#     except Exception as error:
#         print("Connection failed ",  error)
#         time.sleep(3)
