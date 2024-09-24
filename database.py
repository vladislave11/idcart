from sqlalchemy import Column, Integer, String, BLOB, create_engine, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

Base = declarative_base()
load_dotenv()
DATABASE_NAME = os.getenv("DATABASE_NAME")

engine = create_engine('sqlite:///id_cart.db', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


class Id_Cart(Base):
    __tablename__ = "id_cart"
    isikukood = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    date_of_birth = Column(Integer, nullable=False)
    citizenship = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    photo = Column(BLOB, nullable=True)
    password = Column(String, nullable=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
