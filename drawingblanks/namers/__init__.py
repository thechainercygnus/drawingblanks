import json
import os
import string
from random import choice, randint
from time import sleep

import requests
from dotenv import load_dotenv

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

    def _clean_word(self,word:str):
        clean_word = [letter for letter in word if letter in string.ascii_letters]
        return "".join(clean_word)

    def get_similar_word(self, word):
        url = f"{self.URL}{word}/similarTo"
        response = requests.request("GET", url, headers=self.HEADERS)
        content = json.loads(response.content)
        return choice(content['similarTo']) if content['similarTo'] != [] else word

    def get_name(self, join_symbol: str = '-'):
        name = []
        for token in self.NAME_PATTERN:
            accept_word = False
            part_of_speech = self.SPEECHPART[token]
            querystring = {"partofspeech":part_of_speech,"random":"true","syllablesMax": "5"}
            while not accept_word:
                response = requests.request("GET", self.URL, headers=self.HEADERS, params=querystring)
                content = json.loads(response.content)
                word = content['word']
                if self._clean_word(word) == word:
                    accept_word = True
                else:
                    RATE_LIMITER()
            
            name.append(word)
        return join_symbol.join(name)
