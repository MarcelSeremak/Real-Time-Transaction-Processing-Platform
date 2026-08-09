from sqlalchemy.orm import declarative_base, sessionmaker

from db.connection import get_engine

Base = declarative_base()
engine = get_engine()
Session = sessionmaker(bind=engine)

def get_session():
    sess = Session()
    return sess

