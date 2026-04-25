from pydantic import BaseModel, Field
from typing import List, Optional

class HolidayBase(BaseModel):
    name: str = Field(..., description="Название праздника")
    day: int = Field(..., ge=1, le=31, description="День (1-31)")
    month: int = Field(..., ge=0, le=11, description="Месяц (0=Январь, 11=Декабрь)")
    type: str = Field(..., description="Тип (eco, national, world)")
    region: str = Field(..., description="Регион (russia, world)")
    description: str = Field(..., description="Описание праздника")
    events: Optional[List[str]] = Field(default=[], description="Список мероприятий")
    wikipedia_url: Optional[str] = Field(default="", description="Ссылка на Википедию")

class HolidayCreate(HolidayBase):
    pass

class HolidayResponse(HolidayBase):
    id: int
    
    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = ""
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    patronymic: str
    email: str
    role: int
    
    class Config:
        from_attributes = True

class HolidayUpdate(BaseModel):
    name: Optional[str] = None
    day: Optional[int] = None
    month: Optional[int] = None
    type: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None
    events: Optional[List[str]] = None
    wikipedia_url: Optional[str] = None