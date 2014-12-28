from unittest import TestCase
from critto.meta import MetaParser
from critto.ropt import ROpt


class ThisThatROpt(ROpt):
    regex = r'th(is|at)'

    def __call__(self, m):
        return 'yes'


class MetaParserTest(TestCase):
    def setUp(self):
        self.parser = MetaParser()

    def test_parse(self):
        self.parser.register(ThisThatROpt)
        t = self.parser.parse(['this', 'that'])
        assert list(t) == ['yes', 'yes']

    def test_invalid(self):
        self.assertRaises(
            ValueError,
            lambda: list(self.parser.parse(['this'])),
        )
