from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

import db_names
from schemas import ProjectName

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
        "name": "Names",
        "description": "Leverages WordsAPI to generate various names. **REQUIRES RAPID API ACCOUNT**",
        "externalDocs": {
            "description": "WordsAPI",
            "url": "https://rapidapi.com/dpventures/api/wordsapi",
        },
    },
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
)
v1 = FastAPI(title="Drawing Blanks",
    description=description,
    version="0.0.1",
    contact = {
        "name": "Bryce Jenkins",
        "url": "https://brycejenkins.net",
        "email": "bryce@durish.xyz"
    },
    openapi_tags=tags_metadata,
    docs_url="/")

@v1.get("/names/available", tags=["Names"])
def list_available_name_generators():
    return {"projects": {
        "simple": "/names/projects/simple",
        "custom": ""
    }}

project_namer = db_names.ProjectNamer()

@v1.get("/names/projects/simple", tags=["Names"])
def get_new_project_name() -> ProjectName:
    return project_namer.get_name()


app.mount("/v1", v1)
