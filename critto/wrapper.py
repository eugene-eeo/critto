from critto.preprocessor import Preprocessor


def expand(text, conds={}, flags={}):
    preproc = Preprocessor(conds, flags)
    return preproc.expand(text)
