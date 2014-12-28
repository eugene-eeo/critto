from critto.meta import MetaParser
from critto.objects import IfName, IfCond, Flag, Any, EndBlock
from critto.ropt import ROpt


class Preprocessor(MetaParser):
    defaults = [
        EndBlock,
        IfCond,
        IfName,
        Flag,
        Any,
    ]

    def __init__(self):
        MetaParser.__init__(self)
        self.pats = [self.wrap(pat) for pat in self.pats]
        self.flags = {}
        self.conds = {}
        self.stack = [True]

    def add_flag(self, flag, cb):
        self.flags[flag] = cb

    def add_cond(self, cond, cb):
        self.conds[cond] = cb

    def wrap(self, ropt):
        class TmpROpt(ropt.__class__):
            regex = ropt.regex

            def __call__(ins, match):
                return ropt(self, match)
        return TmpROpt()
