from collections import deque


class MetaParser(object):
    defaults = []

    def __init__(self):
        self.pats = deque([ropt() for ropt in self.defaults])

    def register(self, ropt):
        self.pats.appendleft(ropt())

    def handle(self, line):
        length = len(line)
        for ropt in self.pats:
            match = ropt.matches(line)
            if match:
                return ropt(match)
        raise ValueError

    def parse(self, lines):
        for item in lines:
            res = self.handle(item)
            if res is not None:
                yield res

    def expand(self, text):
        lines = text.splitlines()
        return '\n'.join(self.parse(lines))
