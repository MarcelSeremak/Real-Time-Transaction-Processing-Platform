from db.database import get_session
from sqlalchemy import text

session = get_session()

session.execute(text("SELECT 1"))