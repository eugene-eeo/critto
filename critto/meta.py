from re import match


class MetaParser(object):
    def __init__(self):
        self.patterns = []

    def register(self, regex, callback):
        self.patterns.append((regex, callback))

    def parse_line(self, line):
        for regex, callback in self.patterns:
            m = match(regex, line)
            if m and m.end() == len(line):
                return callback(m)
        raise ValueError('No match for %s' % line)

    def parse(self, lines):
        for item in lines:
            res = self.parse_line(item)
            if res is not None:
                yield res

    def expand(self, text):
        lines = text.splitlines()
        return '\n'.join(self.parse(lines))
