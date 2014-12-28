from critto.preprocessor import Preprocessor


def expand(text, conds=None, flags=None):
    return Preprocessor(
        conds=conds or {},
        flags=flags or {},
    )
