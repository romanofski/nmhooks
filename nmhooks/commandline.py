#!/usr/bin/env python
import notmuch
import logging


logging.basicConfig(level=logging.DEBUG)
db = notmuch.Database(mode=notmuch.Database.MODE.READ_WRITE)


def postnew():
    bugzilla_inbox_query = notmuch.Query(db, 'tag:inbox and tag:bug')
    processed = 0

    for msg in bugzilla_inbox_query.search_messages():
        if msg.get_header('X-Bugzilla-Product').startswith('Errata'):
            msg.freeze()
            msg.add_tag('et', False)
            msg.thaw()
            processed += 1

    return processed
