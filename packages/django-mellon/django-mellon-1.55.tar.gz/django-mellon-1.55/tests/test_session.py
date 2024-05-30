import datetime

import pytest
from django.core.cache import cache
from django.utils.timezone import now

from mellon.sessions_backends import cached_db, db

cls_param = pytest.mark.parametrize('cls', [cached_db.SessionStore, db.SessionStore], ids=['cached_db', 'db'])


@cls_param
def test_basic(db, cls):
    cls = cached_db.SessionStore

    session1 = cls()
    session1['foo'] = 'bar'
    session1.save()

    session = cls(session_key=session1.session_key)
    assert session['foo'] == 'bar'

    # check with loading from cache
    cache.clear()
    session = cls(session_key=session1.session_key)
    assert session['foo'] == 'bar'


@cls_param
def test_expiry(db, cls, freezer):
    cls = cached_db.SessionStore

    session1 = cls()
    session1['foo'] = 'bar'
    session1['mellon_session'] = {
        'session_not_on_or_after': (now() + datetime.timedelta(hours=1)).isoformat()
    }
    session1.save()

    freezer.tick(3599)

    session = cls(session_key=session1.session_key)
    assert session['foo'] == 'bar'

    freezer.tick(2)
    session = cls(session_key=session1.session_key)
    assert 'foo' not in session
