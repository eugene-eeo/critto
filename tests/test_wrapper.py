from unittest import TestCase
from critto.wrapper import expand


class ExpandTest(TestCase):
    def test_expand(self):
        x = []
        u = expand('#[flag]\n#[if cond=1]\nthen\n#[endif]',
                   flags=dict(flag=lambda: x.append(1)),
                   conds=dict(cond=lambda: 1))
        assert u == 'then'
