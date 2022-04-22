import os
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import db_names

SECRET_KEY = os.getenv('SECRET_KEY', 'aMadSwedeINDEED!')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

description="""
Drawing Blanks is a tool for helping me name things when I am lacking an idea.

## Names

Generate useful names for random needs

### Projects

Generate new project names.

* **Simple** Create a simple 3 word, hyphenated project name.
* **Custom** Parameter rich capabilities to create just the right random project name. (_not implemented_)
"""

tags_metadata = [
    {
        "name": "Authorization",
        "description": "These endpoints handle the authorization flows."
    },
    {
        "name": "Names",
        "description": "Leverages WordsAPI to generate various names. **REQUIRES RAPID API ACCOUNT**",
        "externalDocs": {
            "description": "WordsAPI",
            "url": "https://rapidapi.com/dpventures/api/wordsapi",
        },
    },
]

# Replace with SQLite Database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Drawing Blanks",
    description=description,
    version="0.0.1",
    contact = {
        "name": "Bryce Jenkins",
        "url": "https://brycejenkins.net",
        "email": "bryce@brycejenkins.net"
    },
    openapi_tags=tags_metadata,
)
v1 = FastAPI(docs_url="/")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    ## Replace with Database Lookup
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@v1.post("/token/", response_model=Token, tags=["Authorization"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@v1.get("/users/me/", response_model=User,tags=["Authorization"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@v1.get("/names/available", tags=["Names"])
def list_available_name_generators():
    return {"projects": {
        "simple": "/names/projects/simple",
        "custom": ""
    }}

project_namer = db_names.ProjectNamer()

@v1.get("/names/projects/simple", tags=["Names"])
def get_new_project_name(token: str = Depends(oauth2_scheme)):
    return project_namer.get_name()

app.mount("/api/v1", v1)
