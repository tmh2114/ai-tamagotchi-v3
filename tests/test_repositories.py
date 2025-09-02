"""Unit tests for repository layer."""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from src.repositories.base import BaseRepository
from src.repositories.tamagotchi_repository import TamagotchiRepository
from src.models import User, Tamagotchi, Interaction


class TestBaseRepository:
    """Test base repository functionality."""
    
    def test_create(self, db_session):
        """Test creating an entity."""
        repo = BaseRepository(User, db_session)
        user = repo.create(
            username="repouser",
            email="repo@example.com",
            password_hash="hash123",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        assert user.id is not None
        assert user.username == "repouser"
    
    def test_get(self, db_session, test_user):
        """Test getting entity by ID."""
        repo = BaseRepository(User, db_session)
        user = repo.get(test_user.id)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.username == test_user.username
    
    def test_get_nonexistent(self, db_session):
        """Test getting non-existent entity."""
        repo = BaseRepository(User, db_session)
        user = repo.get(str(uuid4()))
        
        assert user is None
    
    def test_update(self, db_session, test_user):
        """Test updating an entity."""
        repo = BaseRepository(User, db_session)
        updated_user = repo.update(
            test_user.id,
            display_name="Updated Name",
            coins=500
        )
        
        assert updated_user is not None
        assert updated_user.display_name == "Updated Name"
        assert updated_user.coins == 500
    
    def test_delete(self, db_session, test_user):
        """Test deleting an entity."""
        repo = BaseRepository(User, db_session)
        
        # Verify user exists
        assert repo.exists(test_user.id) is True
        
        # Delete user
        result = repo.delete(test_user.id)
        assert result is True
        
        # Verify user no longer exists
        assert repo.exists(test_user.id) is False
    
    def test_find_by(self, db_session):
        """Test finding entities by attributes."""
        repo = BaseRepository(User, db_session)
        
        # Create multiple users
        user1 = repo.create(
            username="user1",
            email="user1@example.com",
            password_hash="hash1",
            language="en",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        user2 = repo.create(
            username="user2",
            email="user2@example.com",
            password_hash="hash2",
            language="es",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Find by language
        english_users = repo.find_by(language="en")
        assert len(english_users) >= 1
        assert user1.id in [u.id for u in english_users]
    
    def test_bulk_create(self, db_session):
        """Test creating multiple entities."""
        repo = BaseRepository(User, db_session)
        
        users_data = [
            {
                "username": f"bulkuser{i}",
                "email": f"bulk{i}@example.com",
                "password_hash": f"hash{i}",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            for i in range(3)
        ]
        
        created_users = repo.bulk_create(users_data)
        
        assert len(created_users) == 3
        assert all(u.id is not None for u in created_users)


class TestTamagotchiRepository:
    """Test Tamagotchi repository functionality."""
    
    def test_get_by_owner(self, db_session, test_user):
        """Test getting tamagotchis by owner."""
        repo = TamagotchiRepository(db_session)
        
        # Create multiple tamagotchis for the user
        tama1 = repo.create(
            name="Pet1",
            owner_id=test_user.id,
            birth_date=datetime.utcnow(),
            last_stat_update=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        tama2 = repo.create(
            name="Pet2",
            owner_id=test_user.id,
            birth_date=datetime.utcnow(),
            last_stat_update=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Get all tamagotchis for the owner
        tamagotchis = repo.get_by_owner(test_user.id)
        
        assert len(tamagotchis) >= 2
        names = [t.name for t in tamagotchis]
        assert "Pet1" in names
        assert "Pet2" in names
    
    def test_get_active_by_owner(self, db_session, test_user):
        """Test getting only active tamagotchis."""
        repo = TamagotchiRepository(db_session)
        
        # Create one healthy and one dead tamagotchi
        healthy = repo.create(
            name="Healthy",
            owner_id=test_user.id,
            health=80.0,
            birth_date=datetime.utcnow(),
            last_stat_update=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        dead = repo.create(
            name="Dead",
            owner_id=test_user.id,
            health=0.0,
            birth_date=datetime.utcnow(),
            last_stat_update=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Get only active tamagotchis
        active = repo.get_active_by_owner(test_user.id)
        
        assert len(active) >= 1
        assert healthy.id in [t.id for t in active]
        assert dead.id not in [t.id for t in active]
    
    def test_feed(self, db_session, test_tamagotchi):
        """Test feeding a tamagotchi."""
        repo = TamagotchiRepository(db_session)
        
        initial_hunger = test_tamagotchi.hunger
        
        # Feed the tamagotchi
        updated = repo.feed(test_tamagotchi.id, food_value=30.0)
        
        assert updated is not None
        assert updated.hunger == min(100, initial_hunger + 30.0)
        assert updated.last_fed is not None
    
    def test_play(self, db_session, test_tamagotchi):
        """Test playing with a tamagotchi."""
        repo = TamagotchiRepository(db_session)
        
        initial_happiness = test_tamagotchi.happiness
        initial_energy = test_tamagotchi.energy
        
        # Play with the tamagotchi
        updated = repo.play(test_tamagotchi.id, happiness_value=20.0)
        
        assert updated is not None
        assert updated.happiness == min(100, initial_happiness + 20.0)
        assert updated.energy < initial_energy  # Playing uses energy
        assert updated.last_played is not None
    
    def test_clean(self, db_session, test_tamagotchi):
        """Test cleaning a tamagotchi."""
        repo = TamagotchiRepository(db_session)
        
        # Make tamagotchi dirty
        test_tamagotchi.cleanliness = 30.0
        db_session.commit()
        
        # Clean the tamagotchi
        updated = repo.clean(test_tamagotchi.id)
        
        assert updated is not None
        assert updated.cleanliness == 100.0
        assert updated.last_cleaned is not None
    
    def test_give_medicine(self, db_session, test_tamagotchi):
        """Test giving medicine to a tamagotchi."""
        repo = TamagotchiRepository(db_session)
        
        # Make tamagotchi sick
        test_tamagotchi.is_sick = True
        test_tamagotchi.health = 40.0
        db_session.commit()
        
        # Give medicine
        updated = repo.give_medicine(test_tamagotchi.id)
        
        assert updated is not None
        assert updated.is_sick is False
        assert updated.health == 70.0  # 40 + 30
        assert updated.last_medicine is not None
    
    def test_add_experience(self, db_session, test_tamagotchi):
        """Test adding experience and leveling up."""
        repo = TamagotchiRepository(db_session)
        
        # Add experience
        updated = repo.add_experience(test_tamagotchi.id, 150)
        
        assert updated is not None
        assert updated.experience == 150
        assert updated.level == 2  # Should level up
    
    def test_evolution(self, db_session, test_tamagotchi):
        """Test tamagotchi evolution."""
        repo = TamagotchiRepository(db_session)
        
        # Add enough experience to trigger evolution
        test_tamagotchi.level = 4
        db_session.commit()
        
        updated = repo.add_experience(test_tamagotchi.id, 100)  # Level 5
        
        assert updated is not None
        assert updated.level == 5
        assert updated.evolution_stage == "child"  # Should evolve from baby
    
    def test_get_requiring_attention(self, db_session, test_user):
        """Test getting tamagotchis that need attention."""
        repo = TamagotchiRepository(db_session)
        
        # Create tamagotchis with different last interaction times
        old_interaction = datetime.utcnow() - timedelta(hours=48)
        recent_interaction = datetime.utcnow() - timedelta(hours=1)
        
        neglected = repo.create(
            name="Neglected",
            owner_id=test_user.id,
            last_interaction=old_interaction,
            birth_date=datetime.utcnow(),
            last_stat_update=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        cared_for = repo.create(
            name="CaredFor",
            owner_id=test_user.id,
            last_interaction=recent_interaction,
            birth_date=datetime.utcnow(),
            last_stat_update=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Get tamagotchis needing attention (24+ hours)
        needing_attention = repo.get_requiring_attention(threshold_hours=24)
        
        assert len(needing_attention) >= 1
        assert neglected.id in [t.id for t in needing_attention]
        assert cared_for.id not in [t.id for t in needing_attention]