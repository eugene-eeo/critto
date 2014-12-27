from unittest import TestCase
from critto.wrapper import expand


class ExpandTest(TestCase):
    def test_expand(self):
        def enable():
            conds['cond'] = lambda: 'this'
        conds = {}
        flags = {'enable-cond': enable}
        u = expand(open('tests/assets/test.txt').read(),
                   flags=flags,
                   conds=conds)
        assert u == 'Hello World!'
