from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="citizen")
    points = Column(Integer, default=0)


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    severity = Column(
        String,
        default="LOW",
    )

    status = Column(
        String,
        default="REPORTED",
    )

    latitude = Column(
        String,
        nullable=True,
    )

    longitude = Column(
        String,
        nullable=True,
    )

    image_url = Column(
        String,
        nullable=True,
    )

    priority = Column(
        Integer,
        default=0,
    )

    contractor = Column(
        String,
        nullable=True,
    )

    user_id = Column(
        Integer,
        nullable=True,
    )