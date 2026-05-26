from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class StudySpot(Base):
    __tablename__ = "study_spots"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    time_left = Column(Integer)
    has_power = Column(Boolean)
    noise_level = Column(String)
    shared_by = Column(String)
    is_claimed = Column(Boolean, default=False)

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True)

    password = Column(String)

    karma_points = Column(Integer, default=0)