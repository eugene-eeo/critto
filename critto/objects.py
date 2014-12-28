from json import loads
from critto.ropt import ROpt


def ignore_ws(regex):
    return '\W*%s\W*' % regex


class Name(ROpt):
    regex = r'(\w[$\w0-9_]*)'

    def __call__(self, ctx, match):
        name = match.group(1)
        return name in ctx.conds


class Cond(ROpt):
    regex = r'%s=(.+?)' % Name.regex

    def __call__(self, ctx, match):
        name, value = match.groups()
        return ctx.conds[name]() == loads(value)


class Any(ROpt):
    regex = r'(.+)'

    def __call__(self, ctx, match):
        if ctx.stack[-1]:
            return match.group()


class Flag(ROpt):
    regex = ignore_ws(r'#\[%s\]' % Name.regex)

    def __call__(self, ctx, match):
        name = match.group(1)
        return ctx.flags[name]()


class IfName(Name):
    regex = ignore_ws(r'#\[if %s\]' % Name.regex)

    def __call__(self, ctx, match):
        if ctx.stack[-1]:
            val = Name.__call__(self, ctx, match)
            ctx.stack.append(val)


class IfCond(Cond):
    regex = ignore_ws(r'#\[if %s\]' % Cond.regex)

    def __call__(self, ctx, match):
        if ctx.stack[-1]:
            val = Cond.__call__(self, ctx, match)
            ctx.stack.append(val)
        else:
            ctx.stack.append(False)


class EndBlock(Cond):
    regex = ignore_ws(r'#\[end(if|block)\]')

    def __call__(self, ctx, match):
        ctx.stack.pop()
