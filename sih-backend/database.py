from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

# -------------------------
# 1. Database URL
# -------------------------
DATABASE_URL = "sqlite:///./sih.db"

# -------------------------
# 2. Engine & Session Factory
# -------------------------
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------
# 3. Base class
# -------------------------
Base = declarative_base()

# -------------------------
# 4. Models / Tables
# -------------------------

class User(Base):
    """
    Table: Users
    Stores information about all users (admin, teachers, students).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default="user")  # admin / teacher / student
    password = Column(String, nullable=False)  # hashed password
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    # Teachers can have classes
    classes = relationship("Class", back_populates="teacher")

class Student(Base):
    """
    Table: Students
    Stores information about students, their class, and QR code.
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id"))  # link to Class table
    qr_code = Column(String, unique=True, index=True)  # used for scanning attendance
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    attendance_logs = relationship("AttendanceLog", back_populates="student")
    class_ = relationship("Class", back_populates="students")

class Class(Base):
    """
    Table: Classes
    Stores class information and links to teacher and students.
    """
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"))  # teacher assigned to this class
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    teacher = relationship("User", back_populates="classes")
    students = relationship("Student", back_populates="class_")
    periods = relationship("Period", back_populates="class_")

class Period(Base):
    """
    Table: Periods
    Each class can have multiple periods. Stores period token and timing.
    """
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    token = Column(String, unique=True, index=True)  # generated token for attendance
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    class_ = relationship("Class", back_populates="periods")
    attendance_logs = relationship("AttendanceLog", back_populates="period")

class AttendanceLog(Base):
    """
    Table: Attendance Logs
    Stores each attendance entry: student, period, timestamp, location, status.
    """
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    status = Column(String, default="present")  # present / absent / late / excused

    # Relationships
    student = relationship("Student", back_populates="attendance_logs")
    period = relationship("Period", back_populates="attendance_logs")

# -------------------------
# 5. Initialize DB
# -------------------------
def init_db():
    Base.metadata.create_all(bind=engine)

# -------------------------
# 6. DB Session Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print("Database ready ✅")
