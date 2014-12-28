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


def endif(ctx, match):
    ctx.stack.pop()


@scoped
def defined(ctx, match):
    name = match.group(1)
    return name in ctx.conds


@scoped
def cond(ctx, match):
    name, val = match.groups()
    return ctx.conds[name]() == loads(val)


def flag(ctx, match):
    name = match.group(1)
    return ctx.flags[name]()


def text(ctx, match):
    if ctx.stack[-1]:
        return match.group()


class Preprocessor(MetaParser):
    defaults = [
        ROpt(tag('endif'), endif),
        ROpt(tag('if %s' % NAME), defined),
        ROpt(tag('if %s=(.+?)' % NAME), cond),
        ROpt(tag(NAME), flag),
        ROpt('(.+)', text),
    ]

    def __init__(self):
        self.defaults = [self.wrap(t) for t in self.defaults]
        MetaParser.__init__(self)
        self.flags = {}
        self.conds = {}
        self.stack = [True]

    def add_flag(self, flag, cb):
        self.flags[flag] = cb

    def add_cond(self, cond, cb):
        self.conds[cond] = cb

    def parse(self, *args, **kwargs):
        self.stack = [True]
        return MetaParser.parse(self, *args, **kwargs)

    def wrap(self, ropt):
        return ROpt(ropt.regex, partial(ropt.cb, self))
