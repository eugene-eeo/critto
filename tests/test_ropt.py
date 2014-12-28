from unittest import TestCase
from critto.ropt import ROpt


class MetaRegex(ROpt):
    regex = r'(meta-)*regex'

    def __call__(self):
        return 0


class ROptTest(TestCase):
    def setUp(self):
        self.ropt = MetaRegex()

    def test_matches_positive(self):
        assert self.ropt.matches('meta-regex')
        assert self.ropt.matches('meta-meta-regex')

    def test_matches_negative(self):
        assert not self.ropt.matches(' regex')
        assert not self.ropt.matches('regex ')

    def test_callback(self):
        assert self.ropt() == 0
