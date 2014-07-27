notmuch hooks
=============

Allows you to configure hooks for tagging notmuch.

**Warning:** This utility can yield a very poor performance if
configured wrong. Keep in mind that it has a:

    O(n*m)
    
running time complexity with *n* the number of mails and *m* the number
of configurations.

Configuration
-------------

It is recommended to apply initial tags with `notmuch tag` (e.g. use an
offlineimap postsync script and call nmhooks from there for further
tagging).

The configuration file follows a typical .ini type syntax. Here's an
example:

    [GIMP Bugs]
    query = tag:inbox and from:bugzilla
    header = X-Bugzilla-Product
    match = ^.*Gimp\d+$
    apply = +prod +bug

    [CLOSED Bugs]
    # initial query to get all mails which we want to apply our rule on
    query = tag:inbox and from:bugzilla

    # header which should be matched against
    header = X-Bugzilla-Status

    # regular expression on the header value
    match = CLOSED

    # if the regular expression matches the header value, apply these
    # tags
    apply = +archive -inbox +bug


Development
-----------

All you (should) need is:

    python2.7 bootstrap.py
    bin/buildout
    bin/test
