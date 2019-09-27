import json
tweetfile = open('trumptweets.txt', encoding="utf8").read()
x = json.loads(tweetfile)
file = open('formattedtrumptweets.txt', "w", encoding="utf8")
for idx, tweet in enumerate(x):
    file.write(tweet['text'] + '\n')
