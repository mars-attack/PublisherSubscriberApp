import argparse
from json import dumps
import paho.mqtt.client as mqtt
from time import sleep
from util import Util
from random import randint, uniform


class Publisher:
    def __init__(self, delay=0.75, topic='Toronto'):
        self.data_gen = Util(topic)
        self.client = mqtt.Client()
        self.topic = topic
        self.delay = delay

    def publish(self, times=1):
        # Generate values to skip for every 1/100
        skip_list = []
        for x in range(round(times/100)):
            skip_list.append(randint(0, times-1))

        print('======Begin Publishing Data======')
        for x in range(times):
            # Moved data generation here so it generates data to be skipped
            self.data = self.data_gen.create_data()

            # Skip transmiting data
            if (skip_list.count(x)):
                print('Transmission Skipped')
                continue

            # Publish wild data with probablity of 3/100
            num = randint(0, 100)
            if(num % 30 == 0):
                print('Wild Data')
                self.data['humidity'] = str(
                    round(uniform(80, 120), 2))  # Change humitidy data to random extreme outlier

            print(f'#{x}', end=' ')
            self.__publish()

        print('=======End Publishing Data=======')

    def __publish(self):
        print(self.data)
        self.client.connect('localhost', 1883)
        json_data = dumps(self.data, indent=2)
        self.client.publish(self.topic, payload=json_data)
        sleep(self.delay)
        self.client.disconnect()


if __name__ == '__main__':
    # Adding args
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-delay',
        help=f'The delay between transmitting data. Default = 0.75',
        required=False)

    parser.add_argument(
        '-topic',
        help=f'The desired topic. Default = COMP216',
        required=False)

    parser.add_argument(
        '-num_records',
        help=f'The number of records to public. Default = 1',
        required=False)

    args = parser.parse_args()

    # Initialize Publisher based on args
    if args.delay and args.topic:
        pub = Publisher(float(delay=args.delay), topic=args.topic)
    elif args.delay:
        pub = Publisher(float(delay=args.delay))
    elif args.topic:
        pub = Publisher(topic=args.topic)
    else:
        pub = Publisher(delay=1)

    # Publish data
    if args.num_records:
        pub.publish(int(args.num_records))
    else:
        pub.publish(1)
