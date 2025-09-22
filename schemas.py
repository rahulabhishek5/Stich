from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -----------------------
# User Schemas
# -----------------------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "user"

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

# -----------------------
# Class Schemas
# -----------------------
class ClassCreate(BaseModel):
    name: str

class ClassOut(BaseModel):
    id: int
    name: str
    teacher_id: int

    model_config = {"from_attributes": True}

# -----------------------
# Student Schemas
# -----------------------
class StudentCreate(BaseModel):
    name: str
    class_id: int
    qr_code: str
    email: Optional[str] = None

class StudentOut(BaseModel):
    id: int
    name: str
    class_id: int
    qr_code: str
    email: Optional[str] = None

    model_config = {"from_attributes": True}

# -----------------------
# Period Schemas
# -----------------------
class PeriodCreate(BaseModel):
    class_id: int
    start_time: datetime
    end_time: datetime
    token: Optional[str] = None  # optional, auto-generated if not provided

class PeriodOut(BaseModel):
    id: int
    class_id: int
    start_time: datetime
    end_time: datetime
    token: str

    model_config = {"from_attributes": True}

# -----------------------
# Attendance Schemas
# -----------------------
class AttendanceCreate(BaseModel):
    student_id: int
    period_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[str] = "present"
    timestamp: Optional[str] = None  # ISO format string

class AttendanceOut(BaseModel):
    id: int
    student_id: int
    period_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str
    timestamp: datetime

    model_config = {"from_attributes": True}
