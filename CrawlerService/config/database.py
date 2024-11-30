from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

CRAWLER_SERVICE_DB_CONFIG = {
    'CRAWLER_SERVICE_DB_USER': os.getenv('CRAWLER_SERVICE_DB_USER', 'root'),
    'CRAWLER_SERVICE_DB_PASSWORD': os.getenv('CRAWLER_SERVICE_DB_PASSWORD', 'truongquangchu'),
    'CRAWLER_SERVICE_DB_HOST': os.getenv('CRAWLER_SERVICE_DB_HOST', 'localhost'),
    'CRAWLER_SERVICE_DB_NAME': os.getenv('CRAWLER_SERVICE_DB_NAME', 'crawler_service'),
}

DATABASE_URI = (
    f"mysql+mysqlconnector://{CRAWLER_SERVICE_DB_CONFIG['CRAWLER_SERVICE_DB_USER']}:{CRAWLER_SERVICE_DB_CONFIG['CRAWLER_SERVICE_DB_PASSWORD']}"
    f"@{CRAWLER_SERVICE_DB_CONFIG['CRAWLER_SERVICE_DB_HOST']}/{CRAWLER_SERVICE_DB_CONFIG['CRAWLER_SERVICE_DB_NAME']}"
)

# Tạo engine kết nối
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized")