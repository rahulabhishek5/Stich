from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import crud
import auth
from database import init_db, get_db
import schemas

app = FastAPI(title="SIH Automated Attendance API")

# -----------------------
# Startup event: create tables
# -----------------------
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "SIH backend running ✅"}

# -----------------------
# Token endpoint
# -----------------------
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token({"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# -----------------------
# User endpoints
# -----------------------
@app.post("/users", response_model=schemas.UserOut)
def api_create_user(payload: schemas.UserCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_admin)):
    hashed = auth.get_password_hash(payload.password)
    user = crud.create_user(db, payload.name, payload.email, hashed, payload.role)
    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user

@app.get("/users", response_model=list[schemas.UserOut])
def api_list_users(db: Session = Depends(get_db), current_user = Depends(auth.get_current_admin)):
    return crud.get_users(db)

# -----------------------
# Class endpoints
# -----------------------
@app.post("/classes", response_model=schemas.ClassOut)
def api_create_class(payload: schemas.ClassCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_teacher)):
    cls = crud.create_class(db, payload.name, current_user.id)
    return cls

@app.get("/classes", response_model=list[schemas.ClassOut])
def api_list_classes(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    return crud.get_classes(db)

# -----------------------
# Student endpoints
# -----------------------
@app.post("/students", response_model=schemas.StudentOut)
def api_create_student(payload: schemas.StudentCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_teacher)):
    # Ensure the class exists
    cls = crud.get_class_by_id(db, payload.class_id)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    student = crud.create_student(db, payload.name, payload.class_id, payload.qr_code, payload.email)
    if not student:
        raise HTTPException(status_code=400, detail="QR code already assigned")
    return student

@app.get("/students", response_model=list[schemas.StudentOut])
def api_list_students(db: Session = Depends(get_db), current_user = Depends(auth.get_current_teacher)):
    return crud.get_students(db)

# -----------------------
# Period endpoints
# -----------------------
@app.post("/periods", response_model=schemas.PeriodOut)
def api_create_period(payload: schemas.PeriodCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_teacher)):
    # Ensure class exists
    cls = crud.get_class_by_id(db, payload.class_id)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    period = crud.create_period(db, payload.class_id, payload.start_time, payload.end_time, payload.token)
    return period

@app.get("/periods/class/{class_id}", response_model=list[schemas.PeriodOut])
def api_list_periods_for_class(class_id: int, db: Session = Depends(get_db), current_user = Depends(auth.get_current_teacher)):
    return crud.get_periods_for_class(db, class_id)

# -----------------------
# Attendance endpoints
# -----------------------
@app.post("/attendance", response_model=schemas.AttendanceOut)
def api_mark_attendance(payload: schemas.AttendanceCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_teacher)):
    ts = None
    if payload.timestamp:
        try:
            ts = datetime.fromisoformat(payload.timestamp)
        except:
            ts = None
    log = crud.mark_attendance(db, payload.student_id, payload.period_id, payload.latitude, payload.longitude, payload.status or "present", ts)
    if not log:
        raise HTTPException(status_code=404, detail="Student or Period not found")
    return log

@app.get("/attendance/student/{student_id}", response_model=list[schemas.AttendanceOut])
def api_get_attendance_by_student(student_id: int, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    return crud.get_attendance_by_student(db, student_id)

@app.get("/attendance/class/{class_id}", response_model=list[schemas.AttendanceOut])
def api_get_attendance_for_class(class_id: int, db: Session = Depends(get_db), current_user = Depends(auth.get_current_teacher)):
    return crud.get_attendance_for_class(db, class_id)

# -----------------------
# Sync (bulk insert) endpoint
# -----------------------
@app.post("/sync")
def api_sync(records: list[schemas.AttendanceCreate], db: Session = Depends(get_db), current_user = Depends(auth.get_current_teacher)):
    recs = []
    for r in records:
        recs.append({
            "student_id": r.student_id,
            "period_id": r.period_id,
            "timestamp": r.timestamp,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "status": r.status
        })
    inserted = crud.bulk_insert_attendance(db, recs)
    return {"inserted": len(inserted)}

# -----------------------
# Export CSV endpoint
# -----------------------
@app.get("/export/csv")
def api_export_csv(db: Session = Depends(get_db), current_user = Depends(auth.get_current_admin)):
    path = crud.export_attendance_csv(db, path="attendance_export.csv")
    return FileResponse(path, filename="attendance_export.csv")
