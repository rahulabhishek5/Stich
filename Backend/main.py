from fastapi import FastAPI, Depends, HTTPException, Header
import firebase_admin
from firebase_admin import auth, credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = FastAPI()

def verify_firebase_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # "Bearer <idToken>"
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

@app.post("/generate_token")
def generate_token(user=Depends(verify_firebase_token)):
    if not user.get("email", "").endswith("teacher.com"):
        raise HTTPException(status_code=403, detail="Not a teacher")
    # Generate and return QR token...
    return {"token": "1234-5678"}