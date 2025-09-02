# AI Tamagotchi v3 - Core Data Models & Persistence Layer

An AI-powered virtual pet with advanced personality, learning capabilities, and comprehensive data persistence.

## Overview

This repository contains the core data models and persistence layer for AI Tamagotchi v3, featuring:

- **Comprehensive Data Models**: User, Tamagotchi, Interactions, Activities, Items, and Achievements
- **SQLAlchemy ORM**: Robust database abstraction with support for SQLite, PostgreSQL, and MySQL
- **Repository Pattern**: Clean separation of data access logic
- **Data Synchronization**: Offline/online sync capabilities with conflict resolution
- **Migration System**: Database versioning with Alembic
- **Comprehensive Testing**: Unit tests for all models and persistence operations

## Installation

```bash
# Clone the repository
git clone https://github.com/tmh2114/ai-tamagotchi-v3.git
cd ai-tamagotchi-v3

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Database Setup

### Initialize the database

```python
from src.database.config import db_config

# Create all tables
db_config.create_tables()
```

### Run migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

## Core Models

### User Model
- User account management
- Player statistics and progression
- Currency and resources
- Preferences and settings

### Tamagotchi Model
- Pet attributes and stats (happiness, health, hunger, energy, cleanliness)
- Personality traits and behaviors
- Evolution stages and leveling system
- Memory bank for learned behaviors
- Real-time stat decay system

### Interaction Model
- Tracks all user-pet interactions
- Records stat changes and effects
- Sentiment analysis and emotional context
- Experience gain tracking

### Activity Model
- Scheduled and recurring activities
- Activity completion tracking
- Location and participant management
- Reward system integration

### Item & Inventory Models
- Item catalog with effects and requirements
- Inventory management per Tamagotchi
- Equipment and favorite item system
- Consumable and permanent items

### Achievement Model
- Achievement categories and tiers
- Progress tracking
- Reward distribution
- Hidden achievements support

## Usage Examples

### Creating a new Tamagotchi

```python
from src.database.config import get_db
from src.repositories.tamagotchi_repository import TamagotchiRepository

# Get database session
db = next(get_db())
repo = TamagotchiRepository(db)

# Create a new Tamagotchi
tamagotchi = repo.create(
    name="Fluffy",
    owner_id=user_id,
    species="digital_pet",
    personality_type="playful"
)
```

### Interacting with a Tamagotchi

```python
# Feed the Tamagotchi
updated = repo.feed(tamagotchi_id, food_value=30.0)

# Play with the Tamagotchi
updated = repo.play(tamagotchi_id, happiness_value=20.0)

# Give medicine when sick
if tamagotchi.is_sick:
    updated = repo.give_medicine(tamagotchi_id)
```

### Data Synchronization

```python
from src.services.sync_service import SyncService

sync = SyncService()

# Export user data for backup
export_data = sync.export_user_data(user_id, db)

# Import data from backup
results = sync.import_user_data(import_data, db, merge=True)

# Cache pending changes for offline sync
sync.cache_pending_changes(changes)
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

## Project Structure

```
ai-tamagotchi-v3/
├── src/
│   ├── database/
│   │   └── config.py          # Database configuration
│   ├── models/
│   │   ├── user.py            # User model
│   │   ├── tamagotchi.py      # Tamagotchi model
│   │   ├── interaction.py     # Interaction model
│   │   ├── activity.py        # Activity model
│   │   ├── inventory.py       # Item and inventory models
│   │   └── achievement.py     # Achievement model
│   ├── repositories/
│   │   ├── base.py            # Base repository
│   │   └── tamagotchi_repository.py  # Tamagotchi-specific operations
│   └── services/
│       └── sync_service.py    # Data synchronization
├── migrations/
│   ├── env.py                 # Alembic environment
│   └── versions/              # Migration files
├── tests/
│   ├── conftest.py           # Test fixtures
│   ├── test_models.py        # Model tests
│   ├── test_repositories.py  # Repository tests
│   └── test_sync_service.py  # Sync service tests
├── requirements.txt           # Project dependencies
├── setup.py                   # Package setup
└── alembic.ini               # Alembic configuration
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database URL (defaults to SQLite)
DATABASE_URL=sqlite:///./tamagotchi.db

# For PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost/tamagotchi

# For MySQL
# DATABASE_URL=mysql+pymysql://user:password@localhost/tamagotchi
```

## Features

### Real-time Stat Management
- Automatic stat decay based on time elapsed
- Mood and state changes based on stat thresholds
- Health impacts from extreme conditions

### Evolution System
- Level-based evolution stages: baby → child → teen → adult → elder
- Experience-based progression
- Stage-specific abilities and requirements

### Memory and Learning
- Behavior learning system
- Preference tracking
- Memory bank for important events

### Comprehensive Tracking
- All interactions logged with effects
- Activity scheduling and completion
- Achievement progress monitoring

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
