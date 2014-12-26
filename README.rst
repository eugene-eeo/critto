Critto
======

Critto is a preprocessor library that does line modifications.
Basically, it allows you to modify each line and then join
them together based on context. This model is very easy to
program against and can be very powerful but simple at the
same time. It is made to be very lightweight and also easily
extensible via a callback based API. A simple example::

    import os
    from critto import process

    process("#[if os==posix]"
            "You're running *nix!"
            "#[endif]",
            variables={'os': lambda: os.name},)

The preprocessor syntax is inspired by Rust. Currently only
if-statements and "feature flags" are implemented.
