"""Pytest configuration and fixtures."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.config import Base, DatabaseConfig
from src.models import User, Tamagotchi
from uuid import uuid4
from datetime import datetime


@pytest.fixture(scope="function")
def db_config():
    """Create a test database configuration."""
    config = DatabaseConfig(testing=True)
    config.create_tables()
    yield config
    config.drop_tables()
    config.close()


@pytest.fixture(scope="function")
def db_session(db_config):
    """Create a test database session."""
    session = db_config.get_session()
    yield session
    session.close()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        id=str(uuid4()),
        username="testuser",
        email="test@example.com",
        display_name="Test User",
        password_hash="hashed_password",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_tamagotchi(db_session, test_user):
    """Create a test tamagotchi."""
    tamagotchi = Tamagotchi(
        id=str(uuid4()),
        name="Testy",
        owner_id=test_user.id,
        species="digital_pet",
        personality_type="friendly",
        happiness=75.0,
        health=100.0,
        hunger=50.0,
        energy=80.0,
        cleanliness=90.0,
        birth_date=datetime.utcnow(),
        last_stat_update=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(tamagotchi)
    db_session.commit()
    return tamagotchi