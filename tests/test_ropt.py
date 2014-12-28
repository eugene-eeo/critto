from unittest import TestCase
from critto.ropt import ROpt


class ROptTest(TestCase):
    def setUp(self):
        self.ropt = ROpt('(meta-)*regex', lambda: 0)

    def test_matches_positive(self):
        assert self.ropt.matches('meta-regex')
        assert self.ropt.matches('meta-meta-regex')

    def test_matches_negative(self):
        assert not self.ropt.matches(' regex')
        assert not self.ropt.matches('regex ')

    def test_callback(self):
        assert self.ropt() == 0
