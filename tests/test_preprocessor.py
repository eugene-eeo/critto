from unittest import TestCase
from critto.preprocessor import Preprocessor


class PreprocessorTest(TestCase):
    def setUp(self):
        self.preproc = Preprocessor()

    def test_expand(self):
        def cb():
            self.preproc.add_cond('cond', lambda: True)
        self.preproc.add_flag('enable', cb)
        t = self.preproc.expand(open('tests/assets/basic.txt').read())
        assert t == 'yes'

    def test_nested(self):
        self.preproc.add_cond('cond1', lambda: None)
        self.preproc.add_cond('cond2', lambda: 'string')
        t = self.preproc.expand(open('tests/assets/nested.txt').read())
        assert t == 'yes'

    def test_defined(self):
        self.preproc.add_cond('cond1', lambda: 1)
        self.preproc.add_cond('cond2', lambda: 1)
        t = self.preproc.expand(open('tests/assets/defined.txt').read())
        assert t == 'yes'
