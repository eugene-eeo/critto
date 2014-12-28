from json import loads


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

