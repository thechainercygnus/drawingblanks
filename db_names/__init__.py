import json
import os
import string
from random import choice, randint
from time import sleep

import requests
from dotenv import load_dotenv
from schemas import ProjectName, Word

load_dotenv()
RATE_LIMITER = lambda : sleep((randint(1, 6) / 10))



class BaseNamer:
    NAME_PATTERN = None



class ProjectNamer(BaseNamer):
    SPEECHPART = ("noun","verb","adjective")
    URL = "https://wordsapiv1.p.rapidapi.com/words/"
    HEADERS = {
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com",
        "X-RapidAPI-Key": os.environ['RAPID_API_KEY']
    }

    def __init__(self, name_pattern = (1,2,0)):
        self.NAME_PATTERN = name_pattern

    def _clean_word(self, word: Word):
        for character in word.word:
            if character.lower() not in string.ascii_lowercase:
                return False
        return True

    def get_similar_word(self, word):
        url = f"{self.URL}{word}/similarTo"
        response = requests.get(url, headers=self.HEADERS)
        content = json.loads(response.content)
        return choice(content['similarTo']) if content['similarTo'] != [] else word

    def get_definition(self, word: Word) -> Word:
        url = f"{self.URL}{word}/definitions"
        response = requests.get(url, headers=self.HEADERS)
        content = json.loads(response.content)
        if 'definitions' in content.keys():
            word.definition = content['definitions']

        return word

    def get_name(self, join_symbol: str = '-') -> ProjectName:
        name = ProjectName()
        for token in self.NAME_PATTERN:
            accept_word = False
            part_of_speech = self.SPEECHPART[token]
            querystring = {"partofspeech":part_of_speech,"random":"true","syllablesMax": "5"}
            while not accept_word:
                response = requests.get(self.URL, headers=self.HEADERS, params=querystring)
                content = json.loads(response.content)
                word = Word(word=content['word'],part_of_speech=part_of_speech)
                if self._clean_word(word):
                    word = self.get_definition(word)
                    accept_word = True
                else:
                    RATE_LIMITER()
            
            name.words.append(word)
        name.name = join_symbol.join([i.word for i in name.words])
        return name
