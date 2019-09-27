import csv
import time
from json import JSONDecodeError
from googletrans import Translator

translator = Translator()

file = open('formattedfakenews.txt', "w", encoding="utf8")

with open('theonion.txt', encoding="utf8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row[5])
            # translated = translator.translate(row[4], dest='nl')
            # file.write(translated.text)


