import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt
from PIL import Image
import skimage.io as skio
import io
import requests

from model import Model

class server_pubsub():
    '''
    Simulates a server-side pubsub setup 
    '''

    def __init__(self):
        self.animal = None
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_start()
        self.model = Model()

        self._loop()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to server (i.e., broker) with result code "+str(rc))
        self.client.subscribe("paho/classify")

    def on_message(self, client, userdata, msg):
        msg = str(msg.payload, "utf-8")
        print("received: " + msg)

        # Load the image from URL and process it
        # If the image is valid, use the model and retrieve predictions
        if self.animal == "cat":
            params = dict(key='3c805916-3786-4c04-96e1-676c8aac15bf')
            img = Image.open(io.BytesIO(requests.get(msg, params).content))
        elif self.animal == "dog":
            img = Image.fromarray(skio.imread(msg))
        else:
            return

        # Get and plot predictions
        label, confidence = self.model._predict(img)
        plt.title(f'{label} (confidence: {confidence})')
        plt.imshow(img)
        plt.show()

    # Get user input (dog/cat)
    def _loop(self, ):
        while True:
            time.sleep(1)
            self.animal = input("Choose an animal (cat/dog): ") 
            self.client.publish("paho/animal", self.animal)


if __name__ == '__main__':
    sps = server_pubsub()