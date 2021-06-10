import paho.mqtt.client as mqtt
import time
import requests

class device_pubsub():
    '''
    Simulates a device-side pubsub setup 
    '''

    def __init__(self):
        self.update = False    
        self.animal = None
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_start()

        self._loop()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to broker: "+str(rc))
        self.client.subscribe("paho/animal")

    def on_message(self, client, userdata, msg):
        self.animal = str(msg.payload, "utf-8")
        self.update = True
        print("received: " + msg.topic + " " + self.animal)

    def _loop(self, ):
        while True:
            # If there's an update to paho/animal, publish a cat/dog image URL pulled from either API
            if self.update:
                self.client.unsubscribe("paho/animal")
                if self.animal:
                    if self.animal == 'dog':
                        url = requests.get("https://dog.ceo/api/breeds/image/random").json()["message"]
                    elif self.animal == 'cat':
                        url = requests.get("https://api.thecatapi.com/v1/images/search?api_key=3c805916-3786-4c04-96e1-676c8aac15bf&mime_types=jpg,png").json()[0]["url"]
                    self.client.publish('paho/classify', url)
                else:
                    self.client.publish('paho/classify', 0)                    

                time.sleep(1)
                self.update = False
                self.client.subscribe("paho/animal")


if __name__ == '__main__':
    dps = device_pubsub()