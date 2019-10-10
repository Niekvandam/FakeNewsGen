# Load Larger LSTM network and generate text
import sys
import time

import numpy
import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import tweepy as tw

import tweepy
consumer_key = "tRv3Xvjq0iPhgAcTPxgV1k5Zb"
consumer_secret = "o3QQTLvEfxp2sRKdDSuLp55y7kp732qsEh0n386v7NgmzeSDnP"
access_token = "1181490025474736129-Ro305TR554rhxCuuV76PxWerNzogv9"
access_token_secret = "uIJtd0rixGkYVj6YIvXeZPXjhGy1cc6heBK71NZ6g2ht9"




def generate_tweet():
	# load ascii text and covert to lowercase
	filename = "formattedtrumptweets.txt"
	raw_text = open(filename, 'r', encoding='utf-8').read()
	raw_text = raw_text.lower()
	# create mapping of unique chars to integers, and a reverse mapping
	chars = sorted(list(set(raw_text)))
	char_to_int = dict((c, i) for i, c in enumerate(chars))
	int_to_char = dict((i, c) for i, c in enumerate(chars))
	# summarize the loaded data
	n_chars = len(raw_text)
	n_vocab = len(chars)
	dataX = []
	dataY = []
	print("Total Characters: ", n_chars)
	print("Total Vocab: ", n_vocab)
	# prepare the dataset of input to output pairs encoded as integers
	seq_length = 100
	for i in range(0, n_chars - seq_length, 1):
		seq_in = raw_text[i:i + seq_length]
		seq_out = raw_text[i + seq_length]
		dataX.append([char_to_int[char] for char in seq_in])
		dataY.append(char_to_int[seq_out])
		n_patterns = len(dataX)
	print("Total Patterns: ", n_patterns)
	# reshape X to be [samples, time steps, features]
	X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
	# normalize
	X = X / float(n_vocab)
	# one hot encode the output variable
	y = np_utils.to_categorical(dataY)
	# define the LSTM model
	model = Sequential()
	model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
	model.add(Dropout(0.2))
	model.add(LSTM(256))
	model.add(Dropout(0.2))
	model.add(Dense(y.shape[1], activation='softmax'))
	# load the network weights
	filename = "weights-improvement-57-1.5145-bigger.hdf5"
	model.load_weights(filename)
	model.compile(loss='categorical_crossentropy', optimizer='adam')
	tweet = ""
	# pick a random seed
	start = numpy.random.randint(0, len(dataX)-1)
	pattern = dataX[start]
	print("Seed:")
	print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
	# generate characters
	for i in range(241):
		x = numpy.reshape(pattern, (1, len(pattern), 1))
		x = x / float(n_vocab)
		prediction = model.predict(x, verbose=0)
		index = numpy.argmax(prediction)
		result = int_to_char[index]
		seq_in = [int_to_char[value] for value in pattern]
		tweet += result
		sys.stdout.write(result)
		pattern.append(index)
		pattern = pattern[1:len(pattern)]
	return tweet

def post_tweet():
	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tw.API(auth, wait_on_rate_limit=True)
	api.update_status(generate_tweet())


while True:
	post_tweet()
	time.sleep(3.75 * 60)
