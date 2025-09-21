# backend/main.py

import os
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, auth
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

# --- 1. INITIALIZATION ---
# Load the secret path from the .env file
load_dotenv()

# Initialize Firebase Admin SDK
creds_path = os.getenv("FIREBASE_CREDS_PATH")
if not creds_path:
    raise ValueError("FIREBASE_CREDS_PATH environment variable not set.")
cred = credentials.Certificate(creds_path)
firebase_admin.initialize_app(cred)

# Initialize FastAPI app
app = FastAPI()

# --- 2. THE DOORMAN (CORS) ---
# This allows your frontend (running on a different address) to talk to your backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all origins. Be more specific in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. THE ID CHECKER (Authorization Dependency) ---
# This is a reusable function that will protect our endpoints.
# It expects a token in the "Authorization: Bearer <token>" header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Verifies Firebase ID token and returns user data if valid."""
    try:
        # This is the function that checks if the token is real and not expired.
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        # If the token is fake or expired, it raises an error.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- 4. YOUR API ENDPOINTS ---
@app.get("/")
def read_root():
    """An unprotected endpoint that anyone can access."""
    return {"message": "Welcome to the Automated Attendance API"}

# This endpoint is PROTECTED. Only logged-in users can access it.
@app.post("/checkin")
async def check_in(current_user: dict = Depends(get_current_user)):
    """
    A protected endpoint for a student to check in.
    The 'current_user' variable is populated by our get_current_user dependency.
    """
    user_uid = current_user.get("uid")
    user_email = current_user.get("email")
    print(f"Authenticated check-in request from user: {user_email} (UID: {user_uid})")

    # Your attendance logic (geolocation, QR validation) will go here.
    return {"status": "success", "message": f"Attendance marked for {user_email}"}