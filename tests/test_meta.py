from unittest import TestCase
from critto.meta import MetaParser


class MetaParserTest(TestCase):
    def setUp(self):
        self.regex = 'th(is|at)'
        self.handler = lambda m: self.store.append(m.group(1))

        self.store = []
        self.parser = MetaParser()
        self.parser.register(self.regex, self.handler)

    def test_parse_valid(self):
        lines = ['this', 'that']
        assert list(self.parser.parse(lines)) == []
        assert self.store == ['is', 'at']

    def test_parse_invalid(self):
        lines = ['this', 'those']
        self.assertRaises(
            ValueError,
            lambda: list(self.parser.parse(lines)),
        )

    def test_expand(self):
        assert self.parser.expand('') == ''
        assert self.parser.expand('this\nthat') == ''
