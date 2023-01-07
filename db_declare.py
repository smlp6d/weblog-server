from sqlalchemy import create_engine, Column, Integer, Text, DateTime, BigInteger, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

from setup import sql_uri, debug


engine = create_engine(sql_uri, echo=debug)
base = declarative_base()


class tables:
    class turns(base):
        __tablename__ = 'turns'
        id = Column(Integer, primary_key=True)

        ip = Column(Text)
        user = Column(Text)
        debug = Column(Boolean)
        config = Column(JSON)

        datetime = Column(DateTime, default=datetime.now)

    class tokens(base):
        __tablename__ = 'tokens'
        id = Column(Integer, primary_key=True)

        name = Column(Text, nullable=False)
        token = Column(Text)

        alive = Column(Boolean, default=True)

        create_datetime = Column(DateTime, default=datetime.now)
        update_datetime = Column(DateTime, default=datetime.now)

    class logs(base):
        __tablename__ = 'logs'
        id = Column(Integer, primary_key=True)

        app_id = Column(Integer, nullable=False)

        lvl = Column(Integer, default=0)
        text = Column(Text, nullable=False)

        datetime = Column(DateTime, default=datetime.now)

    class logins(base):
        __tablename__ = 'logins'
        id = Column(Integer, primary_key=True)

        addr = Column(Text, nullable=False)

        datetime = Column(DateTime, default=datetime.now)



base.metadata.create_all(engine)
