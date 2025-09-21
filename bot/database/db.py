from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)

    requests = relationship("Request", back_populates="user")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    answer = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates="requests")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
