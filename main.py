from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

import db_names

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

project_namer = db_names.ProjectNamer()

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

@app.get("/users/me", tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/names/", tags=["Names"])
def list_name_modules():
    return {"projects": "generate project names"}


@app.get("/names/projects", tags=["Names"])
def get_new_project_name(token: str = Depends(oauth2_scheme)):
    return project_namer.get_name()

