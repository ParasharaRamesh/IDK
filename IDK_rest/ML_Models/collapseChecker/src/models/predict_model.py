import pickle
import numpy as np
import pandas as pd
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"\..")
from settings import *

def predictResult(input_text, obj):
	input_counts = obj[0].transform(input_text)
	input_tfidf = obj[1].transform(input_counts)
	predicted = obj[2].predict(input_tfidf)
	return predicted

def predictCollapse(input_text):
	with open(FINAL_VECT, 'rb') as final_count_vect:
		count_vect = pickle.load(final_count_vect)
	with open(FINAL_TFIDF, 'rb') as final_tf_transformer:
		tf_transformer = pickle.load(final_tf_transformer)
	with open(FINAL_MODEL, 'rb') as final_model:
		lr_clf = pickle.load(final_model)
	obj = [count_vect, tf_transformer, lr_clf]
	predicted_class = predictResult([input_text], obj)[0]
	if predicted_class == 0 or predicted_class == 1:
		print("hate speech")
		return True
	return False 

if __name__ == '__main__':
	with open(FINAL_VECT, 'rb') as final_count_vect:
		count_vect = pickle.load(final_count_vect)
	with open(FINAL_TFIDF, 'rb') as final_tf_transformer:
		tf_transformer = pickle.load(final_tf_transformer)
	with open(FINAL_MODEL, 'rb') as final_model:
		lr_clf = pickle.load(final_model)
	obj = [count_vect, tf_transformer, lr_clf]
	while True:
		input_text = input("Enter input text: ")
		predicted_class = predictResult([input_text], obj)
		print(['Hate speech', 'Offensive', 'Clean'][predicted_class[0]])
