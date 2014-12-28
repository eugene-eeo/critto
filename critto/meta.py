class MetaParser(object):
    defaults = []

    def __init__(self):
        self.pats = self.defaults[:]

    def register(self, ropt):
        self.pats.insert(0, ropt)

    def handle(self, line):
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
