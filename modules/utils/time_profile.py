import datetime as d
from config import BIO_PATTERN

class TimeKeeper:

    def __init__(self, first_part_nick_name=""):
        self.bio = first_part_nick_name

        self.timez = d.timezone(d.timedelta(hours=2))
        self.current_time = d.datetime.now(self.timez)
        self.last_time = d.datetime.now(self.timez)

        self.bio_pattern = BIO_PATTERN


    def _upd_time(self):
        self.current_time = d.datetime.now(self.timez)


    def update_time(self):
        self._upd_time()
        cur_m, cur_h = self.current_time.minute, self.current_time.hour
        last_m, last_h = self.last_time.minute, self.last_time.hour

        if cur_m != last_m or cur_h != last_h:
            self.last_time = self.current_time
            return True, self._time_stringified()
        else:
            return False, None

    def _time_stringified(self):
        result = self.bio_pattern.format(self.last_time.strftime('%a, %H:%M'))
        return result

    def update_name(self, name):
        self.bio = name


if __name__ == "__main__":
    x = TimeKeeper()