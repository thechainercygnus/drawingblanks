from fastapi import FastAPI

import db_names

app = FastAPI()

project_namer = db_names.ProjectNamer()

@app.get("/names/")
def list_name_modules():
    return {"projects": "generate project names"}


@app.get("/names/projects")
def get_new_project_name():
    return project_namer.get_name()
