from functools import partial
from critto.meta import MetaParser
from critto.ropt import ROpt
from critto.constructs import endif, defined, cond, flag, text


NAME = '([$\w][\w0-9_-]+)'


def tag(regex):
    return '\W*#\[%s\]\W*' % regex


class Preprocessor(MetaParser):
    defaults = [
        ROpt(tag('endif'), endif),
        ROpt(tag('if %s' % NAME), defined),
        ROpt(tag('if %s=(.+?)' % NAME), cond),
        ROpt(tag(NAME), flag),
        ROpt('(.+)', text),
    ]

    def __init__(self, flags, conds):
        self.defaults = [self.wrap(t) for t in self.defaults]
        MetaParser.__init__(self)
        self.flags = flags
        self.conds = conds
        self.stack = [True]

    def add_flag(self, flag, cb):
        self.flags[flag] = cb

    def add_cond(self, cond, cb):
        self.conds[cond] = cb

    def wrap(self, ropt):
        return ROpt(ropt.regex, partial(ropt.cb, self))
