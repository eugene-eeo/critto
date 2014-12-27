from functools import partial as bind
from json import loads
from critto.meta import MetaParser


def defined_or(value, cb):
    if value is None:
        return cb()
    return value


def ignore_ws(regex):
    return '\W*%s\W*' % regex


class Preprocessor(MetaParser):
    def __init__(self, conds=None, flags=None):
        MetaParser.__init__(self)
        self.stack = [True]
        self.conds = defined_or(conds, dict)
        self.flags = defined_or(flags, dict)
        self.setup()

    def register_flag(self, flag, callback):
        self.flags[flag] = callback

    def register_cond(self, cond, callback):
        self.conds[cond] = callback

    def handle_flag(self, match):
        flag = match.group(1)
        self.flags[flag]()

    def handle_cond(self, match):
        if self.last_cond:
            cond, value = match.groups()
            value = loads(value)
            self.stack.append(self.conds[cond]() == value)

    def handle_endc(self, match):
        self.stack.pop()

    def handle_any(self, match):
        if self.last_cond:
            return match.group()

    @property
    def last_cond(self):
        return self.stack[-1]

    def parse(self, *args, **kwargs):
        self.stack = [True]
        return MetaParser.parse(self, *args, **kwargs)

    pairs = [
        (ignore_ws(r'#\[if (.+?)=(.+?)\]'), handle_cond),
        (ignore_ws(r'#\[endif\]'), handle_endc),
        (ignore_ws(r'#\[(.+)\]'), handle_flag),
        (r'(.*)',  handle_any),
        ]

    def setup(self):
        for re, cb in self.pairs:
            self.register(re, bind(cb, self))
