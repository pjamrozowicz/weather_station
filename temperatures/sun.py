import ephem


class Sun:
    def __init__(self, x, y):
        self.home = ephem.Observer()
        self.home.lat, self.home.lon = x, y
        self.sun = ephem.Sun()

    def last_rising(self):
        time = self.home.previous_rising(self.sun)
        return ephem.localtime(time)

    def next_rising(self):
        time = self.home.next_rising(self.sun)
        return ephem.localtime(time)

    def last_sunset(self):
        time = self.home.previous_setting(self.sun)
        return ephem.localtime(time)

    def next_sunset(self):
        time = self.home.next_setting(self.sun)
        return ephem.localtime(time)
