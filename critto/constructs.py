from json import loads
from critto.ropt import ropt


NAME = r'([A-Za-z_$][\w_-]+)'


def tag(regex):
    return r'\s*#!\[%s\]\s*' % regex


def scoped(func):
    def function(ctx, match):
        if ctx.stack[-1]:
            return ctx.stack.append(func(ctx, match))
        ctx.stack.append(False)
    return function


@ropt(tag('endif'))
def endif(ctx, _):
    ctx.stack.pop()


@ropt(tag('if %s' % NAME))
@scoped
def defined(ctx, match):
    name = match.group(1)
    return name in ctx.conds


@ropt(tag('if %s=(.+)' % NAME))
@scoped
def cond(ctx, match):
    name, val = match.groups()
    return ctx.conds[name]() == loads(val)


@ropt(tag(NAME))
def flag(ctx, match):
    name = match.group(1)
    return ctx.flags[name]()


@ropt('.+')
def text(ctx, match):
    if ctx.stack[-1]:
        return match.group()
