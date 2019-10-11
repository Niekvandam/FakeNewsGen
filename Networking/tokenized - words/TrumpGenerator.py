import random
import re
import time

import pyttsx3 as pyttsx
import tweepy as tw
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import Sequential
import keras.utils as ku
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.utils as ku
import numpy as np
tokenizer = Tokenizer(filters='\t')


def dataset_preparation(data):
    # basic cleanup
    corpus = data.lower().split("\n")

    # tokenization
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1

    # create input sequences using list of tokens
    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i + 1]
            input_sequences.append(n_gram_sequence)

    # pad sequences
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

    # create predictors and label
    predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
    label = ku.to_categorical(label, num_classes=total_words)

    return predictors, label, max_sequence_len, total_words


def create_model(max_sequence_len, total_words):
    model = Sequential()
    model.add(Embedding(total_words, 10, input_length=max_sequence_len - 1))
    model.add(LSTM(150, return_sequences=True))
    model.add(Dropout(0.0001))
    model.add(LSTM(100))
    model.add(Dense(total_words, activation='softmax'))
    model.load_weights("weights-improvement-74-2.9662-bigger.hdf5")
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model


def generate_text(seed_text, next_words, max_sequence_len):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted = model.predict_classes(token_list, verbose=0)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text


def generate_seed():
    lines = open('formattedtrumptweets.txt', encoding='utf-8').read().splitlines()
    words = random.choice(lines).split()
    if(words == None):
        words = random.choice(lines).split()
    seed = random.choice(words)
    if("https" in seed):
        seed = generate_seed()
    print("seed is:\t" + seed)
    return seed

def validate_tweet(tweet):
    while len(tweet) > 240:
       tweet = tweet[0:max(tweet.rfind(i) for i in "!.?)]}")]
    return tweet

consumer_key = "tRv3Xvjq0iPhgAcTPxgV1k5Zb"
consumer_secret = "o3QQTLvEfxp2sRKdDSuLp55y7kp732qsEh0n386v7NgmzeSDnP"
access_token = "1181490025474736129-Ro305TR554rhxCuuV76PxWerNzogv9"
access_token_secret = "uIJtd0rixGkYVj6YIvXeZPXjhGy1cc6heBK71NZ6g2ht9"


def post_tweet():
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    tweetlength = random.randrange(6,100)
    result = generate_text(generate_seed(), tweetlength, max_sequence_len)
    text = re.sub(r"http\S+", "", result)
    text = validate_tweet(text)
    print(text)
    # engine = pyttsx.init()
    # engine.say(text)
    # engine.runAndWait()
    api.update_status(text)


data = open('formattedtrumptweets.txt', 'r', encoding='utf-8').read()
predictors, label, max_sequence_len, total_words = dataset_preparation(data)
model = create_model(max_sequence_len, total_words)

while True:
    try:
        post_tweet()
    except tw.error.TweepError:
        print(tw.error.TweepError)
    sleepminutes = random.randrange(1,60)
    time.sleep(sleepminutes * 60)

