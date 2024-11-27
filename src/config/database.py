from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_CONFIG = {
    'DB_USER': 'root',
    'DB_PASSWORD': 'truongquangchu',
    'DB_HOST': 'localhost',
    'DB_NAME': 'crawler_service'
}

DATABASE_URI = (
    f"mysql+mysqlconnector://{DB_CONFIG['DB_USER']}:{DB_CONFIG['DB_PASSWORD']}"
    f"@{DB_CONFIG['DB_HOST']}/{DB_CONFIG['DB_NAME']}"
)

# Tạo engine kết nối
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized")