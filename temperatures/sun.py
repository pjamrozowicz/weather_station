import ephem


class Sun:
    def __init__(self, x, y):
        self.home = ephem.Observer()
        self.home.lat, self.home.lon = x, y
        self.sun = ephem.Sun()

    def last_rising(self):
        return self.home.previous_rising(self.sun)

    def next_rising(self):
        return self.home.next_rising(self.sun)

    def last_sunset(self):
        return self.home.previous_setting(self.sun)

    def next_sunset(self):
        return self.home.next_setting(self.sun)
