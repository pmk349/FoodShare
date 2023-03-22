from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MOVE META DATA TO YAML FILE

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:19065RA2y@localhost/foodshare_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()