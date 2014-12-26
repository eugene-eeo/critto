from critto.machinery import Parser


def expand(text, variables={}, flags={}):
    parser = Parser(variables, flags)
    it = parser.parse(text.split('\n'))
    return '\n'.join(it)
