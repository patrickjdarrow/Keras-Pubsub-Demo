import numpy as np
import cv2
from keras.models import load_model

class Model():
	''' 
	Keras Model wrapper
	'''
	def __init__(self):
		self.model = load_model("model.h5")
		self.model._make_predict_function()

	def _predict(self, x):
		x = np.array(cv2.resize(np.array(x), (299,299)))/255.
		pred = self.model.predict(np.array([x]))[0]
		label = "dog" if pred[1] > pred[0] else "cat"
		confidence = str(int(100*np.max(pred))) + "%"
		return (label, confidence)