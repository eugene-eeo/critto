from critto.constructs import endif, defined, cond, flag, text
from critto.meta import MetaParser
from critto.ropt import ROpt


NAME = r'([A-Za-z_$][\w_-]+)'


def tag(regex):
    return r'\s*#!\[%s\]\s*' % regex


class Preprocessor(MetaParser):
    defaults = [
        ROpt(tag('endif'), endif),
        ROpt(tag('if %s' % NAME), defined),
        ROpt(tag('if %s=(.+?)' % NAME), cond),
        ROpt(tag(NAME), flag),
        ROpt('(.+)', text),
    ]

    def __init__(self, flags, conds):
        self.defaults = [t.bind(self) for t in self.defaults]
        MetaParser.__init__(self)
        self.flags = flags
        self.conds = conds
        self.stack = [True]

    def add_flag(self, name, func):
        self.flags[name] = func

    def add_cond(self, name, func):
        self.conds[name] = func
