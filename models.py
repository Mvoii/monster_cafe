from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    username: str
    password: str
    role: str


class Reservation(BaseModel):
    user_id: int
    reservation_time: datetime
    meal_status: Optional[str] = "pending"
