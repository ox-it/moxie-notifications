from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from werkzeug.local import LocalProxy

from moxie.core.service import Service


class DatabaseService(Service):

    def __init__(self, backend_uri):
        self._backend = self._get_backend(backend_uri)

    def _get_backend(self, backend_uri):
        engine = create_engine(backend_uri, convert_unicode=True)
        db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=engine))
        Base = declarative_base()
        Base.query = db_session.query_property()
        return Base

    def __getattr__(self, name):
        return getattr(self._backend, name)

orm = LocalProxy(DatabaseService.from_context)

