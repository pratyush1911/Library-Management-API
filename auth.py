from fastapi import APIRouter, Depends,HTTPException
from jose import jwt, JWTError 
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .models import LoginRequest
from passlib.context import CryptContext

router=APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
     )

def hash_password(password:str):
     return pwd_context.hash(password)

USERS = {
    "Admin": {
        "password": hash_password("password123"),
        "role": "admin"
    },

    "Alice": {
        "password": hash_password("alice123"),
        "role": "member"
    }
}

SECRET_KEY = "this-is-my-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password:str, hashed_password:str):
     return pwd_context.verify(
    plain_password,
    hashed_password )

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return { 
            "username": username,
            "role": role
        }
    
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
def get_current_user(
    token: str = Depends(oauth2_scheme)):
      return verify_token(token)

def get_current_admin(current_user = Depends(get_current_user)):
     if current_user["role"] == "admin":
          return current_user
     raise HTTPException(status_code=403, detail="Admin access required.")

@router.post("/login")
def login(credentials: LoginRequest):
        user = USERS.get(credentials.username)
        if user is None:
             raise HTTPException(status_code=401, detail="Invalid username or password")
        if verify_password(credentials.password, user["password"]): 
             token = create_access_token(
              {
                 "sub": credentials.username,
                 "role": user["role"]
              }  )

             return {
                  "access_token": token,
                  "token_type": "bearer"
                    }
        raise HTTPException(status_code=401, detail="Invalid username or password")