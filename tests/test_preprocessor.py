from unittest import TestCase
from critto.preprocessor import Preprocessor


class PreprocessorTest(TestCase):
    def setUp(self):
        self.ctx = []
        self.preproc = Preprocessor()
        self.preproc.register_flag('flag', lambda: self.ctx.append(1))
        self.preproc.register_cond('cond', lambda: 1)

    def test_flag(self):
        self.preproc.expand('#[flag]')
        assert self.ctx == [1]

    def test_cond(self):
        t = self.preproc.expand('#[if cond=1]\nyes\n#[endif]')
        assert t == 'yes'

    def test_nested_cond(self):
        text = '#[if cond=2]\n#[if cond=1]\nyes\n#[endif]\n#[endif]'
        t = self.preproc.expand(text)
        assert t == ''

    def test_whitespace_ignored(self):
        self.preproc.register_cond('cond', lambda: self.ctx.append(2))
        self.preproc.expand('\t#[flag]  \n#[if cond=null]\n #[endif]')
        assert self.ctx == [1, 2]
