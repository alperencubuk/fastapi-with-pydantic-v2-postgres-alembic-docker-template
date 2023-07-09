from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from source.core.settings import settings

engine = create_engine(settings.POSTGRES_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def database_health(db: Session) -> bool:
    try:
        db.execute(select(1))
        return True
    except Exception:
        return False
