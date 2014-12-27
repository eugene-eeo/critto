from json import loads
from critto.meta import MetaParser


def ignore_ws(regex):
    return '\W*%s\W*' % regex


class Preprocessor(MetaParser):
    cond_re = ignore_ws(r'#\[if (.+?)=(.+?)\]')
    endc_re = ignore_ws(r'#\[endif\]')
    flag_re = ignore_ws(r'#\[(.+)\]')
    any_re  = r'(.+)'

    def __init__(self, *args, **kwargs):
        MetaParser.__init__(self, *args, **kwargs)
        self.stack = [True]
        self.flags = {}
        self.conds = {}
        self.setup()

    def setup(self):
        pairs = [
            (self.cond_re, self.handle_cond),
            (self.endc_re, self.handle_endc),
            (self.flag_re, self.handle_flag),
            (self.any_re, self.handle_any),
            ]
        for re, cb in pairs:
            self.register(re, cb)

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
