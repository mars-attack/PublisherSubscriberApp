from random import randint, gauss
import matplotlib.pyplot as plt


class Generator:
    def __init__(self, low=0, high=1, start=0.5):
        self.value = start
        self.low = low
        self.high = high
        self.range = high - low
        self.isRise = True  # Defines whether the random delta is posititve of negative
        self.init()

    def init(self):
        # Update delta every sprint of about 1 week
        self.sprint = gauss(7, 1)
        self.delta = randint(-10, 10) * 0.005
        self.counter = 0

    # Returns a random value between 0 and 1
    def update_value(self):
        self.counter += 1
        if self.counter >= self.sprint:
            self.init()

        # Regenerate delta to stay within limits
        if self.value + self.delta < 0:
            self.delta = randint(0, 10) * 0.005
        elif self.value + self.delta > 1:
            self.delta = randint(-10, 0) * 0.005

        self.value += self.delta

        return self.value

    # Returns a scaled random value
    @property
    def data(self):
        variation = randint(-10, 10) * 0.005  # Adds 'sqiggles'
        if self.value + variation < 0 or self.value + variation > 1:
            variation *= -1  # Switch signs to stay within defined boundaries

        return (self.update_value() + variation) * self.range + self.low


if __name__ == '__main__':
    gen = Generator(low=30, high=80, start=0.4)
    y = [gen.data for _ in range(100)]

    plt.plot(y, 'b')
    plt.title('Humidity Per Day')
    plt.xlabel('Days')
    plt.ylabel('Humidity %')
    plt.show()
