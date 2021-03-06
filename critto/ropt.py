from functools import partial
from re import compile as rcompile


class ROpt(object):
    def __init__(self, regex, callback):
        self.regex = regex
        self.compiled = rcompile(self.regex)
        self.callback = callback

    def matches(self, text):
        match = self.compiled.match(text)
        if match and (match.end() - match.start()) == len(text):
            return match

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

    def bind(self, instance):
        return self.__class__(
            self.regex,
            partial(self.callback, instance),
            )


def ropt(regex):
    def wrapper(fn):
        return ROpt(regex, fn)
    return wrapper
