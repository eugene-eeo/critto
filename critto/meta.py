from re import match
from collections import deque


class MetaParser(object):
    patterns = []

    def __init__(self):
        self.regexes = deque(self.patterns)

    def register(self, regex, callback):
        self.regexes.appendleft((regex, callback))

    def handle(self, line):
        for regex, callback in self.regexes:
            m = match(regex, line)
            if m and m.end() == len(line):
                return callback(m)
        raise ValueError

    def parse(self, lines):
        for item in lines:
            res = self.handle(item)
            if res is None:
                continue
            yield res
