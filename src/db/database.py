from db.connection import get_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = get_engine()
Session = sessionmaker(bind=engine)

def get_session():
    sess = Session()
    return sess

