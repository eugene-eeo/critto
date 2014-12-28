from re import compile


class ROpt(object):
    def __init__(self, regex, cb):
        self.regex = regex
        self.compiled = compile(regex)
        self.cb = cb

    def matches(self, text):
        m = self.compiled.match(text)
        if m and m.end() == len(text):
            return m

    def __call__(self, *args, **kwargs):
        return self.cb(*args, **kwargs)
