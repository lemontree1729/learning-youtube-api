import time
import datetime


class ProgressBar:
    def __init__(self, length, division=50, fill=""):
        self.count = 0
        self.length = length
        self.division = division
        self.fill = str(fill)
        self.start = time.time()

    def next(self):
        self.count += 1
        bar = int(self.count / self.length * self.division)
        percent = int(self.count / self.length * 100)
        self.end = time.time()
        average_time = (self.end - self.start) / self.count
        eta = datetime.timedelta(seconds=int(average_time * (self.length - self.count)))
        loading = chr(60934 + (self.count - 1) % 5)
        end = ""
        if self.count == self.length:
            loading = "◯"
            end = ""
        print(
            f"process: {loading} {self.fill*bar}{''*(self.division-bar)}{end} | {percent:3d}% | {self.count}/{self.length} | eta: {eta}",
            end="\r",
        )
        if self.count == self.length:
            print(f"\ntook {datetime.timedelta(seconds=self.end - self.start)}")
