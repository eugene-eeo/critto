from functools import partial
from re import compile as rcompile


class ROpt(object):
    def __init__(self, regex, callback):
        self.regex = regex
        self.compiled = self.compile()
        self.callback = callback

    def compile(self):
        return rcompile(self.regex)

    def matches(self, text):
        match = self.compiled.match(text)
        if match and match.end() == len(text):
            return match

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

    def bind(self, instance):
        return self.__class__(
                self.regex,
                partial(self.callback, instance),
            )
