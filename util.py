from datetime import datetime, timedelta
from generator import Generator


class Util:

    def __init__(self, location='Toronto'):
        self.start_id = 111
        self.location = location
        self.gen = Generator(low=30, high=80)
        self.date_time = datetime.now()

    def create_data(self):
        data = {
            'id': self.start_id,
            'time': self.date_time.strftime('%d-%m-%Y %H:%M:%S'),
            'location': self.location,
            'humidity': str(round(self.gen.data, 2))
        }
        self.date_time += timedelta(days=1)
        self.start_id += 1
        return data

    def print_data(data):
        for i in data:
            print(f'{i}: {data[i]}')
        print('\n')
