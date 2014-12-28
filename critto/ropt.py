from re import compile


class ROpt(object):
    regex = None

    def __init__(self):
        self.compiled = compile(self.regex)

    def matches(self, text):
        m = self.compiled.match(text)
        if m and m.end() == len(text):
            return m

    def __call__(self, *args, **kwargs):
        return self.cb(*args, **kwargs)
