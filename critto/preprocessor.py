from critto.constructs import endif, defined, cond, flag, text
from critto.meta import MetaParser
from critto.ropt import ROpt


class Preprocessor(MetaParser):
    patterns = [
        endif,
        defined,
        cond,
        flag,
        text
    ]

    def __init__(self, flags, conds):
        self.patterns = [t.bind(self) for t in self.patterns]
        self.flags = flags
        self.conds = conds
        self.stack = [True]

    def add_flag(self, name, func):
        self.flags[name] = func

    def add_cond(self, name, func):
        self.conds[name] = func

    @property
    def last_cond(self):
        return self.stack[-1]

    def push(self, cond):
        self.stack.append(cond)
