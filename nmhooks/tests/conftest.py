import pytest
import notmuch
import shutil
import os


@pytest.fixture
def db(tmpdir):
    """
    Creates a notmuch database.
    """
    src = os.path.join(os.path.dirname(__file__), 'mails')
    for item in os.listdir(src):
        shutil.copytree(os.path.join(src, item),
                        os.path.join(str(tmpdir), item))
    db = notmuch.Database(str(tmpdir), create=True)
    for mail in os.listdir(str(tmpdir.join('cur'))):
        db.add_message(os.path.join(str(tmpdir.join('cur')), mail))
    return db
