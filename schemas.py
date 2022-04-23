from pydantic import BaseModel


class Word(BaseModel):
    word: str
    part_of_speech: str
    definition: str = None

class ProjectName(BaseModel):
    name: str = None
    words: list[Word] = []
