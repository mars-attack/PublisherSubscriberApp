import json
import argparse
import paho.mqtt.client as mqtt
from util import Util
from tkinter import *
from tkinter.ttk import *
import threading
from subsrciber_gui import TkApp


class subscriber:
    counter = 0
    prevId = 0
    currentId = 0

    def __init__(self, topic='Toronto', port=1883):
        # Start subsribe using threading
        thread = threading.Thread(target=self.on_subscriber_init, args=[
                                  topic, port], daemon=True)
        thread.start()
        # Start tkinter App
        self.app = TkApp('Group 4 | Final', topic)

    def on_subscriber_init(self, topic, port):
        self.client = mqtt.Client()
        print(f'Subscriber listening to topic {topic} at port {port}\n...')
        self.client.on_message = self.message_handler  # Assign on_message delegate
        self.client.connect('localhost', port)
        self.client.subscribe(topic)
        self.client.loop_forever()

    def check_values(self, dict):
        if not dict['id']:
            return False
        elif not dict['location']:
            return False
        elif not dict['time']:
            return False
        elif not dict['humidity']:
            return False
        else:
            return True

    def check_wild_data(self, humidity):
        if humidity >= 80 or humidity < 30:
            return False
        else:
            self.counter += 1
            return True

    def message_handler(self, client, userdat, message):
        decoded_messgage = message.payload.decode("utf-8")
        myDict = json.loads(decoded_messgage)
        self.currentId = myDict['id']
        # Check for missed transmission
        if self.counter > 1 and self.currentId - self.prevId > 1:
            print("Skipped Transmission Found!")
            print('\n')
            self.app.initUI('error')

        if (self.check_values(myDict) == True):
            if self.check_wild_data(float(myDict['humidity'])):
                # Display data in console
                Util.print_data(myDict)
                # Display data using tkinter
                self.app.initUI(float(myDict['humidity']))
            else:
                print("Wild Data Found!")
                print('\n')
                # Send 'error' to alert UI of bad data
                self.app.initUI('error')
        else:
            print("Missing Data Found!")
            print('\n')
            self.app.initUI('error')
        self.prevId = self.currentId

    def block(self):
        self.app.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-topic',
        help='The topic that the subscriber will receive data from. Default="Toronto"',
        required=False)

    args = parser.parse_args()
    if args.topic is None:
        sub = subscriber()
    else:
        sub = subscriber(args.topic)
    sub.block()
