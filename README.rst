Critto
======

Critto is a preprocessor library that does line modifications.
Basically, it allows you to modify each line and then join
them together based on context. This model is very easy to
program against and can be very powerful but simple at the
same time. It is made to be very lightweight and also easily
extensible via a callback based API. That is, given a piece
of text:

.. code-block:: cfg

    #[enable]
    #[if os="posix"]
    code here...
    #[endif]

Critto can expand it to the following, if you are running
a -nix OS, or nothing at all if you are running something
else, like Windows::

    code here...

The code required to do it is very minimal:

.. code-block:: python

    import os
    from critto import expand

    expand(text,
           conds=dict(os=lambda: os.name),
           flags=dict(enable=do_something))

The preprocessor syntax is inspired by Rust. Currently only
if-statements and "feature flags" are implemented.
