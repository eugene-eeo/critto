Critto
======

Critto is a preprocessor library that does line modifications.
Basically, it allows you to modify each line and then join
them together based on context. It is made to be very lightweight
and also easily extensible via a callback based API. That is,
given a piece of text:

.. code-block:: cfg

    #![enable]
    #![if os="posix"]
    code here...
    #![endif]

Critto can expand it to the following, if you are running
a -nix OS, or nothing at all if you are running something
else, like Windows::

    code here...

The code required to do it is very minimal. Currently only
feature flags and simple equality conditionals are supported
by default. Expressions are parsed using JSON. I intend to
keep the API and core tiny.

.. code-block:: python

    import os
    from critto import expand

    expand(text,
           conds=dict(os=lambda: os.name),
           flags=dict(enable=do_something))

Preprocessor syntax is inspired by Rust. The aim of this
project is to help simplify the creation of preprocessors
where using template engines are overkill and not necessary.
