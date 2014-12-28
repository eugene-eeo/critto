from functools import partial as bind
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
        self.defaults = [ROpt(r.regex, bind(r.cb, self)) for r in self.defaults]
        MetaParser.__init__(self)
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

    defaults = [
        ROpt(tag('endif'), handle_endif),
        ROpt(tag('if %s' % NAME), handle_defined),
        ROpt(tag('if %s=(.+?)' % NAME), handle_cond),
        ROpt(tag(NAME), handle_flag),
        ROpt('(.+)', handle_any),
    ]
