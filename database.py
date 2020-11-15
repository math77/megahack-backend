from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
"""
import psycopg2.extras

# call it in any place of your program
# before working with UUID objects in PostgreSQL
psycopg2.extras.register_uuid()
"""
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin_erp:%$#@!&*4dm1ndbbd@127.0.0.1/erp_version-dev"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20, max_overflow=0
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()
Base.query = SessionLocal.query_property()