from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

user_db = os.getenv('USER_DATABASE')
password_db = os.getenv('USER_PASSWORD')
name_db = os.getenv('NAME_DATABASE')

engine = create_engine(f'postgresql+psycopg2://{user_db}:{password_db}@localhost:5432/{name_db}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()




