from operator import eq, ne
from critto.meta import MetaParser


class Parser(MetaParser):
    EXPR = '(.+?)\W*(==|!=)\W*(.+?)'
    COND = r'\W*#\[if %s\]' % EXPR
    FLAG = r'\W*#\[(.+)\]'

    def __init__(self, variables, flags):
        self.patterns = [
            (self.COND, self.parse_cond),
            (self.FLAG, self.parse_flag),
            (r'(.*)', self.parse_any),
        ]
        MetaParser.__init__(self)
        self.states = [True]
        self.variables = variables
        self.flags = dict(endif=lambda: self.states.pop())
        self.flags.update(flags)

    def parse_flag(self, match):
        self.flags[match.group(1)]()

    def execute_cond(self, match):
        name, op, text = match.groups()
        func = eq if op == '==' else ne
        return func(
            self.variables[name](),
            text,
            )

    def parse_cond(self, match):
        if not self.states[-1]:
            return
        self.states.append(self.execute_cond(match))

    def parse_any(self, match):
        if self.states[-1]:
            return match.group()
