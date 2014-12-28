from json import loads
from critto.ropt import ROpt


NAME = r'(\w[$\w0-9_]*)'


def ignore_ws(regex):
    return '\W*%s\W*' % regex


class Any(ROpt):
    regex = r'(.+)'

    def __call__(self, ctx, match):
        if ctx.stack[-1]:
            return match.group()


class Flag(ROpt):
    regex = ignore_ws(r'#\[%s\]' % NAME)

    def __call__(self, ctx, match):
        name = match.group(1)
        return ctx.flags[name]()


class IfName(ROpt):
    regex = ignore_ws(r'#\[if %s\]' % NAME)

    def __call__(self, ctx, match):
        if ctx.stack[-1]:
            res = match.group(1) in ctx.conds
            ctx.stack.append(res)
        else:
            ctx.stack.append(False)


class IfCond(ROpt):
    regex = ignore_ws(r'#\[if %s=(.+?)\]' % NAME)

    def __call__(self, ctx, match):
        if ctx.stack[-1]:
            name, value = match.groups()
            res = ctx.conds[name]() == loads(value)
            ctx.stack.append(res)
        else:
            ctx.stack.append(False)


class EndBlock(ROpt):
    regex = ignore_ws(r'#\[end(if|block)\]')

    def __call__(self, ctx, match):
        ctx.stack.pop()
