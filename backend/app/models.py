from sqlalchemy import Column, Integer, String, Text, ARRAY, Enum as SQLEnum
from app.database import Base
import enum

class HolidayType(str, enum.Enum):
    ECO = "eco"
    NATIONAL = "national"
    WORLD = "world"

class Region(str, enum.Enum):
    RUSSIA = "russia"
    WORLD = "world"

class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)  # 0-11
    type = Column(String, nullable=False)
    region = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    events = Column(Text, nullable=True)  # JSON string
    wikipedia_url = Column(String, nullable=True)

class UserRole:
    USER = 0
    ADMIN = 1

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, nullable=False)      # Фамилия
    first_name = Column(String, nullable=False)     # Имя
    patronymic = Column(String, nullable=True)      # Отчество
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer, default=UserRole.USER)  # 0 - пользователь, 1 - админ