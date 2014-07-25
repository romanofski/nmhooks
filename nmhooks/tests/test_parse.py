import pytest
import notmuch
import nmhooks.commandline
import io
import os


@pytest.fixture
def config():
    sample = """
[BugzillaTest]
query = to:receiver
header = X-Product
match = nmhooks
apply = +test -bug"""
    return io.BytesIO(sample)


def test_creates_queries_from_config(config, db):
    result = nmhooks.commandline.construct_query(db, 'tag: foo')
    assert isinstance(result, notmuch.Query)


def test_construct_tag_mapping_successfully():
    mapping = nmhooks.commandline.construct_tag_mapping('+foo bar -baz')
    assert mapping == [('foo', 'add_tag'), ('baz', 'remove_tag')]


def test_applies_rules_successfully(config, db):
    cparser = nmhooks.commandline.parse_rules(config)
    nmhooks.commandline.apply_rules(cparser, db)

    msgs = notmuch.Query(db, '').search_messages()
    assert 'test' == str(msgs.collect_tags())


def test_does_not_remove_existing_tags(config, db):
    cparser = nmhooks.commandline.parse_rules(config)

    query = notmuch.Query(db, '')
    msgs = query.search_messages()
    msg = list(msgs)[0]
    msg.freeze()
    msg.add_tag('hurz')
    msg.thaw()

    nmhooks.commandline.apply_rules(cparser, db)
    assert 'hurz test' == str(query.search_messages().collect_tags())
