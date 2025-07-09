from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from passlib.hash import pbkdf2_sha256  # hashing password

# base setting database
Base = declarative_base()
DATABASE_URL = "sqlite:///poly_messenger.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

