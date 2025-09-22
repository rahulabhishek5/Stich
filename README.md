# 📌 Automated Attendance System for Rural Schools  

An end-to-end digital attendance management system designed for rural schools, ensuring **accuracy, transparency, and accessibility** through **QR codes, geofencing, cloud backups, and reporting**.  

---

## 🚀 Features  

- 👩‍🏫 **Teacher Portal** – Create classes, start sessions, view real-time attendance, export reports.  
- 👨‍🎓 **Student Dashboard** – Log in, check in with QR + geofence, track attendance history.  
- 🏫 **Admin Tools** – Upload rosters, monitor attendance, download reports for compliance.  
- ⚙ **Backend Validation** – Session tokens, geofencing, duplicate prevention, real-time updates.  
- ☁ **Cloud Integration** – Daily sync, monthly backups, government-ready CSV exports.  

---

## 🛠️ Workflow  

### **Teacher/Admin**  
1. Login using school ID + credentials.  
2. Create class (roster via CSV/manual entry).  
3. Start session → system generates unique token (10 min valid).  
4. Monitor real-time check-ins (present/absent).  
5. Close session → finalize attendance → export reports.  

### **Student**  
1. Login with student ID & password.  
2. See active classes in dashboard.  
3. Check-in using QR + geofence validation.  
4. View attendance history.  

### **For Students Without Devices**  
- Teacher manually marks attendance using **teacher GPS + timestamp**.  

### **Backend**  
- Exports **daily & monthly CSV reports**.  

---

## 📊 Reporting & Analytics  

- **Daily CSV** – roll no., student name, status, timestamp.  
- **Monthly Reports** – auto-generated per class, stored in cloud.  
- **Analytics** – class attendance %, teacher efficiency, day-wise comparison.  

---

## 📂 Tech Stack (Suggested)  

- **Frontend**: React / HTML-CSS-JS  
- **Backend**: Node.js / Express  
- **Database**: MongoDB / PostgreSQL  
- **Authentication**: JWT / Firebase Auth  
- **Cloud Storage**: AWS S3 / Firebase / Google Drive API  
- **Geofencing**: GPS-based validation APIs  

---

## 🔑 Roles  

👩‍🏫 **Teacher**  
- Creates account → Creates class → Starts session → Views live check-ins → Exports reports.  

👨‍🎓 **Student**  
- Logs in → Sees dashboard → Checks-in → Gets confirmation → Views history.  

⚙ **Backend**  
- Handles accounts, sessions, validation, DB storage, reporting.  

🏫 **Admin**  
- Uploads rosters → Oversees attendance → Downloads/export reports.  

☁ **Cloud**  
- Auto-stores records → Monthly backups → Safe long-term access.  

---

## 📦 Installation & Setup  

```bash
# Clone the repository
git clone https://github.com/your-username/automated-attendance-system.git

# Navigate to project folder
cd automated-attendance-system

# Install dependencies
npm install

# Run backend
npm start

# For frontend (if React)
cd client
npm install
npm run dev

{ studentID, classID, teacherID, timestamp, location, sessionID, status }


- Validates token, session, geofence, enrollment, duplicate check-ins.  
- Stores attendance in structured DB:  
