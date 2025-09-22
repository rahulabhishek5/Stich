from database import init_db, SessionLocal
import crud
from datetime import datetime, timedelta

# -----------------------
# 1. Initialize DB
# -----------------------
init_db()
db = SessionLocal()

# -----------------------
# 2. Create teacher user
# -----------------------
user_email = "test@example.com"
user = crud.get_user_by_email(db, user_email)
if not user:
    user = crud.create_user(db, name="Test Teacher", email=user_email, password_hashed="hashedpw", role="teacher")
print(f"User: {user.id} | {user.name} | {user.email} | {user.role}")

# -----------------------
# 3. Create a class
# -----------------------
cls_name = "5A"
cls = crud.create_class(db, name=cls_name, teacher_id=user.id)
print(f"Class: {cls.id} | {cls.name} | Teacher ID: {cls.teacher_id}")

# -----------------------
# 4. Create a student
# -----------------------
student_qr = "QR-T1"
student_email = "student1@example.com"
s = crud.create_student(db, name="Student1", class_id=cls.id, qr_code=student_qr, email=student_email)
print(f"Student: {s.id} | {s.name} | Class ID: {s.class_id} | QR: {s.qr_code}")

# -----------------------
# 5. Create a period
# -----------------------
start_time = datetime.utcnow()
end_time = start_time + timedelta(hours=1)
period_token = "TESTTOKEN123"
period = crud.create_period(db, class_id=cls.id, start_time=start_time, end_time=end_time, token=period_token)
print(f"Period: {period.id} | Class ID: {period.class_id} | Token: {period.token}")

# -----------------------
# 6. Mark attendance
# -----------------------
log = crud.mark_attendance(
    db,
    student_id=s.id,
    period_id=period.id,
    latitude=17.38,
    longitude=78.48,
    status="present",
    timestamp=datetime.utcnow()
)
print(f"Attendance Log: {log.id} | Student ID: {log.student_id} | Period ID: {log.period_id} | Status: {log.status}")

# -----------------------
# 7. Print all records for verification
# -----------------------
print("\n--- All Users ---")
for u in crud.get_users(db):
    print(u.id, u.name, u.email, u.role)

print("\n--- All Classes ---")
for c in crud.get_classes(db):
    print(c.id, c.name, c.teacher_id)

print("\n--- All Students ---")
for st in crud.get_students(db):
    print(st.id, st.name, st.class_id, st.qr_code)

print("\n--- All Periods ---")
for p in crud.get_periods_for_class(db, cls.id):
    print(p.id, p.class_id, p.start_time, p.end_time, p.token)

print("\n--- All Attendance Logs ---")
for a in crud.get_attendance_for_class(db, cls.id):
    print(a.id, a.student_id, a.period_id, a.status, a.timestamp)

# -----------------------
# 8. Close DB session
# -----------------------
db.close()
