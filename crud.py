from sqlalchemy.orm import Session
from sqlalchemy import func, case
from database import User, Student, Class, Period, AttendanceLog
from datetime import datetime
import csv

# -------------------------
# Users
# -------------------------
def create_user(db: Session, name: str, email: str, password_hashed: str, role: str = "user"):
    """
    Create a new user (admin/teacher/student)
    """
    if db.query(User).filter(User.email == email).first():
        return None
    user = User(name=name, email=email, password=password_hashed, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# -------------------------
# Students
# -------------------------
def create_student(db: Session, name: str, class_id: int, qr_code: str, email: str = None):
    """
    Create a student and assign to a class.
    """
    if db.query(Student).filter(Student.qr_code == qr_code).first():
        return None
    student = Student(name=name, class_id=class_id, qr_code=qr_code, email=email)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_students(db: Session):
    return db.query(Student).all()

def get_student_by_qr(db: Session, qr_code: str):
    return db.query(Student).filter(Student.qr_code == qr_code).first()

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


# -------------------------
# Classes
# -------------------------
def create_class(db: Session, name: str, teacher_id: int):
    """
    Create a class and assign a teacher
    """
    new_class = Class(name=name, teacher_id=teacher_id)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

def get_classes(db: Session):
    return db.query(Class).all()

def get_class_by_id(db: Session, class_id: int):
    return db.query(Class).filter(Class.id == class_id).first()


# -------------------------
# Periods
# -------------------------
def create_period(db: Session, class_id: int, start_time: datetime, end_time: datetime, token: str = None):
    """
    Create a period for a class. Token optional; generated if not provided.
    """
    if not token:
        import uuid
        token = str(uuid.uuid4())
    period = Period(class_id=class_id, start_time=start_time, end_time=end_time, token=token)
    db.add(period)
    db.commit()
    db.refresh(period)
    return period

def get_period_by_token(db: Session, token: str):
    return db.query(Period).filter(Period.token == token).first()

def get_periods_for_class(db: Session, class_id: int):
    return db.query(Period).filter(Period.class_id == class_id).all()


# -------------------------
# Attendance Logs
# -------------------------
def mark_attendance(db: Session, student_id: int, period_id: int, latitude: str = None, longitude: str = None, status: str = "present", timestamp: datetime = None):
    """
    Record attendance for a student in a period.
    """
    if not timestamp:
        timestamp = datetime.utcnow()

    # Check student and period exist
    student = get_student_by_id(db, student_id)
    period = db.query(Period).filter(Period.id == period_id).first()
    if not student or not period:
        return None

    log = AttendanceLog(
        student_id=student_id,
        period_id=period_id,
        timestamp=timestamp,
        latitude=latitude,
        longitude=longitude,
        status=status
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_attendance_by_student(db: Session, student_id: int):
    return db.query(AttendanceLog).filter(AttendanceLog.student_id == student_id).all()

def get_attendance_for_class(db: Session, class_id: int):
    return db.query(AttendanceLog).join(Student).filter(Student.class_id == class_id).all()


# -------------------------
# Bulk insert / offline sync
# -------------------------
def bulk_insert_attendance(db: Session, records: list):
    """
    Accept a list of attendance records for offline sync.
    Each record should be:
        { "student_id": int, "period_id": int, "timestamp": ISO string, "latitude": str, "longitude": str, "status": str }
    """
    inserted = []
    for r in records:
        sid = r.get("student_id")
        pid = r.get("period_id")
        ts = r.get("timestamp")
        lat = r.get("latitude")
        lon = r.get("longitude")
        status = r.get("status", "present")

        # Validate student and period
        if not get_student_by_id(db, sid) or not db.query(Period).filter(Period.id == pid).first():
            continue

        # Parse timestamp
        if ts:
            try:
                ts = datetime.fromisoformat(ts)
            except:
                ts = datetime.utcnow()
        else:
            ts = datetime.utcnow()

        # Avoid duplicates: same student + same period + same timestamp
        exists = db.query(AttendanceLog).filter(
            AttendanceLog.student_id == sid,
            AttendanceLog.period_id == pid,
            AttendanceLog.timestamp == ts
        ).first()
        if exists:
            continue

        log = AttendanceLog(
            student_id=sid,
            period_id=pid,
            timestamp=ts,
            latitude=lat,
            longitude=lon,
            status=status
        )
        db.add(log)
        inserted.append(log)

    db.commit()
    for l in inserted:
        db.refresh(l)
    return inserted


# -------------------------
# Export CSV
# -------------------------
def export_attendance_csv(db: Session, path: str = "attendance_export.csv"):
    """
    Export all attendance logs to a CSV file.
    """
    logs = db.query(AttendanceLog).join(Student).join(Period).order_by(AttendanceLog.timestamp).all()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "log_id", "student_id", "student_name", "class_name",
            "period_id", "period_start", "period_end",
            "timestamp", "latitude", "longitude", "status"
        ])
        for l in logs:
            writer.writerow([
                l.id,
                l.student_id,
                l.student.name if l.student else "",
                l.student.class_.name if l.student and l.student.class_ else "",
                l.period_id,
                l.period.start_time.isoformat() if l.period else "",
                l.period.end_time.isoformat() if l.period else "",
                l.timestamp.isoformat() if l.timestamp else "",
                l.latitude or "",
                l.longitude or "",
                l.status or ""
            ])
    return path


# -------------------------
# Analytics / Summaries
# -------------------------
def attendance_summary_by_student(db: Session):
    """
    Returns total days vs present days for each student.
    """
    q = db.query(
        AttendanceLog.student_id,
        func.count(AttendanceLog.id).label("total_days"),
        func.sum(case([(AttendanceLog.status == "present", 1)], else_=0)).label("present_days")
    ).group_by(AttendanceLog.student_id).all()
    return q
