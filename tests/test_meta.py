from unittest import TestCase
from critto.meta import MetaParser
from critto.ropt import ROpt


class MetaParserTest(TestCase):
    def setUp(self):
        self.parser = MetaParser()

    def test_parse(self):
        self.parser.register(ROpt('th(is|at)', lambda m: 'yes'))
        t = self.parser.parse(['this', 'that'])
        assert list(t) == ['yes', 'yes']

    def test_invalid(self):
        self.assertRaises(
            ValueError,
            lambda: list(self.parser.parse(['this'])),
        )
