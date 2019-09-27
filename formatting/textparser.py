import csv
import time
from json import JSONDecodeError
from googletrans import Translator


translator = Translator()

file = open('formattedfakenews.txt', "w", encoding="utf8")


with open("theonion.txt", encoding="utf8") as f:
    lines = f.readlines()
    for line in lines:
            translated = translator.translate(line, dest='nl')
            print(translated.text)


