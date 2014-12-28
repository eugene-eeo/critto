from functools import partial
from json import loads
from critto.meta import MetaParser
from critto.ropt import ROpt


NAME = '([$\w][\w0-9_-]+)'


def tag(regex):
    return '\W*#\[%s\]\W*' % regex


def scoped(func):
    def function(self, match):
        if self.stack[-1]:
            return self.stack.append(func(self, match))
        self.stack.append(False)
    return function


class Preprocessor(MetaParser):
    def __init__(self):
        self.pats = [
            ROpt(tag('endif'), self.handle_endif),
            ROpt(tag('if %s' % NAME), self.handle_defined),
            ROpt(tag('if %s=(.+?)' % NAME), self.handle_cond),
            ROpt(tag(NAME), self.handle_flag),
            ROpt('(.+)', self.handle_any),
        ]
        self.flags = {}
        self.conds = {}
        self.stack = [True]

    def add_flag(self, flag, cb):
        self.flags[flag] = cb

    def add_cond(self, cond, cb):
        self.conds[cond] = cb

    def handle_endif(self, match):
        self.stack.pop()

    @scoped
    def handle_defined(self, match):
        name = match.group(1)
        return name in self.conds

    @scoped
    def handle_cond(self, match):
        name, value = match.groups()
        return self.conds[name]() == loads(value)

    def handle_flag(self, match):
        name = match.group(1)
        self.flags[name]()

    def handle_any(self, match):
        if self.stack[-1]:
            return match.group()

    def parse(self, *args, **kwargs):
        self.stack = [True]
        return MetaParser.parse(self, *args, **kwargs)
