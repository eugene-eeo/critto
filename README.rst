Critto
======

Critto is a file preprocessor that does line modifications.
It is made to be very lightweight and also extensible via
a callback based API. A simple example::

    import os
    from critto import process

    process("#[if os==posix]"
            "You're running *nix!"
            "#[endif]",
            variables={'os': lambda: os.name},)

The preprocessor syntax is inspired by Rust. Currently only
if-statements and "feature flags" are implemented.
