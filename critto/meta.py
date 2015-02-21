class MetaParser(object):
    patterns = []

    def __init__(self):
        self.patterns = self.patterns[:]

    def register(self, ropt):
        self.patterns.insert(0, ropt)

    def handle(self, line):
        for ropt in self.patterns:
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
