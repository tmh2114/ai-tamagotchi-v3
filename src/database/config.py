"""Database configuration and connection management."""
import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tamagotchi.db")
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create base class for models
Base = declarative_base()

class DatabaseConfig:
    """Database configuration and session management."""
    
    def __init__(self, database_url: Optional[str] = None, testing: bool = False):
        """Initialize database configuration.
        
        Args:
            database_url: Custom database URL
            testing: Whether this is for testing (uses in-memory database)
        """
        if testing:
            self.database_url = TEST_DATABASE_URL
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False
            )
        else:
            self.database_url = database_url or DATABASE_URL
            if self.database_url.startswith("sqlite"):
                self.engine = create_engine(
                    self.database_url,
                    connect_args={"check_same_thread": False},
                    echo=False
                )
            else:
                self.engine = create_engine(self.database_url, echo=False)
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all database tables."""
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()
    
    def close(self):
        """Close the database connection."""
        self.engine.dispose()

# Global database instance
db_config = DatabaseConfig()

def get_db():
    """Dependency to get database session."""
    db = db_config.get_session()
    try:
        yield db
    finally:
        db.close()