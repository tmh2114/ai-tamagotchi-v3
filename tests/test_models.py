"""Unit tests for data models."""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from src.models import (
    User, Tamagotchi, Interaction, Activity,
    Item, InventoryItem, Achievement
)


class TestUserModel:
    """Test User model."""
    
    def test_user_creation(self, db_session):
        """Test creating a user."""
        user = User(
            id=str(uuid4()),
            username="newuser",
            email="new@example.com",
            password_hash="hash123",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.coins == 100  # Default starting coins
        assert user.player_level == 1
    
    def test_user_to_dict(self, test_user):
        """Test user to_dict method."""
        user_dict = test_user.to_dict()
        
        assert user_dict["id"] == test_user.id
        assert user_dict["username"] == test_user.username
        assert user_dict["email"] == test_user.email
        assert "stats" in user_dict
        assert "resources" in user_dict
        assert user_dict["resources"]["coins"] == 100


class TestTamagotchiModel:
    """Test Tamagotchi model."""
    
    def test_tamagotchi_creation(self, db_session, test_user):
        """Test creating a tamagotchi."""
        tama = Tamagotchi(
            id=str(uuid4()),
            name="Fluffy",
            owner_id=test_user.id,
            birth_date=datetime.utcnow(),
            last_stat_update=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(tama)
        db_session.commit()
        
        assert tama.id is not None
        assert tama.name == "Fluffy"
        assert tama.level == 1
        assert tama.evolution_stage == "baby"
        assert tama.happiness == 50.0
    
    def test_tamagotchi_update_stats(self, test_tamagotchi):
        """Test updating tamagotchi stats over time."""
        initial_hunger = test_tamagotchi.hunger
        initial_energy = test_tamagotchi.energy
        
        # Simulate 2 hours passing
        test_tamagotchi.update_stats(120)  # 120 minutes
        
        # Stats should decrease
        assert test_tamagotchi.hunger < initial_hunger
        assert test_tamagotchi.energy < initial_energy
        assert test_tamagotchi.hunger >= 0  # Should not go below 0
    
    def test_tamagotchi_to_dict(self, test_tamagotchi):
        """Test tamagotchi to_dict method."""
        tama_dict = test_tamagotchi.to_dict()
        
        assert tama_dict["id"] == test_tamagotchi.id
        assert tama_dict["name"] == test_tamagotchi.name
        assert "stats" in tama_dict
        assert tama_dict["stats"]["happiness"] == test_tamagotchi.happiness
        assert tama_dict["level"] == 1


class TestInteractionModel:
    """Test Interaction model."""
    
    def test_interaction_creation(self, db_session, test_tamagotchi):
        """Test creating an interaction."""
        interaction = Interaction(
            id=str(uuid4()),
            tamagotchi_id=test_tamagotchi.id,
            interaction_type="feed",
            interaction_subtype="apple",
            user_message="Here's an apple!",
            tamagotchi_response="Yummy! Thank you!",
            happiness_change=5.0,
            hunger_change=20.0,
            experience_gained=10,
            created_at=datetime.utcnow()
        )
        db_session.add(interaction)
        db_session.commit()
        
        assert interaction.id is not None
        assert interaction.interaction_type == "feed"
        assert interaction.happiness_change == 5.0
        assert interaction.experience_gained == 10
    
    def test_interaction_to_dict(self, db_session, test_tamagotchi):
        """Test interaction to_dict method."""
        interaction = Interaction(
            id=str(uuid4()),
            tamagotchi_id=test_tamagotchi.id,
            interaction_type="play",
            happiness_change=10.0,
            created_at=datetime.utcnow()
        )
        db_session.add(interaction)
        db_session.commit()
        
        interaction_dict = interaction.to_dict()
        
        assert interaction_dict["id"] == interaction.id
        assert interaction_dict["interaction_type"] == "play"
        assert interaction_dict["stat_changes"]["happiness"] == 10.0


class TestActivityModel:
    """Test Activity model."""
    
    def test_activity_creation(self, db_session, test_tamagotchi):
        """Test creating an activity."""
        activity = Activity(
            id=str(uuid4()),
            tamagotchi_id=test_tamagotchi.id,
            activity_type="sleeping",
            activity_name="Afternoon nap",
            description="Taking a peaceful nap",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(activity)
        db_session.commit()
        
        assert activity.id is not None
        assert activity.activity_type == "sleeping"
        assert activity.activity_name == "Afternoon nap"
    
    def test_scheduled_activity(self, db_session, test_tamagotchi):
        """Test creating a scheduled activity."""
        scheduled_time = datetime.utcnow() + timedelta(hours=2)
        activity = Activity(
            id=str(uuid4()),
            tamagotchi_id=test_tamagotchi.id,
            activity_type="eating",
            activity_name="Dinner time",
            is_scheduled=True,
            scheduled_time=scheduled_time,
            recurrence_pattern="daily",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(activity)
        db_session.commit()
        
        assert activity.is_scheduled is True
        assert activity.scheduled_time == scheduled_time
        assert activity.recurrence_pattern == "daily"


class TestItemModel:
    """Test Item and InventoryItem models."""
    
    def test_item_creation(self, db_session):
        """Test creating an item."""
        item = Item(
            id=str(uuid4()),
            name="Apple",
            category="food",
            description="A fresh, juicy apple",
            rarity="common",
            cost=10,
            effects={"hunger": 20, "happiness": 5},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(item)
        db_session.commit()
        
        assert item.id is not None
        assert item.name == "Apple"
        assert item.category == "food"
        assert item.effects["hunger"] == 20
    
    def test_inventory_item_creation(self, db_session, test_tamagotchi):
        """Test adding item to inventory."""
        # Create item first
        item = Item(
            id=str(uuid4()),
            name="Toy Ball",
            category="toy",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(item)
        db_session.commit()
        
        # Add to inventory
        inventory_item = InventoryItem(
            id=str(uuid4()),
            tamagotchi_id=test_tamagotchi.id,
            item_id=item.id,
            quantity=3,
            acquired_at=datetime.utcnow()
        )
        db_session.add(inventory_item)
        db_session.commit()
        
        assert inventory_item.id is not None
        assert inventory_item.quantity == 3
        assert inventory_item.is_equipped is False


class TestAchievementModel:
    """Test Achievement model."""
    
    def test_achievement_creation(self, db_session):
        """Test creating an achievement."""
        achievement = Achievement(
            id=str(uuid4()),
            name="First Steps",
            category="care",
            description="Feed your Tamagotchi for the first time",
            requirement_type="counter",
            requirement_value=1,
            reward_experience=50,
            tier="bronze",
            points=10,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(achievement)
        db_session.commit()
        
        assert achievement.id is not None
        assert achievement.name == "First Steps"
        assert achievement.reward_experience == 50
        assert achievement.tier == "bronze"
    
    def test_achievement_to_dict(self, db_session):
        """Test achievement to_dict method."""
        achievement = Achievement(
            id=str(uuid4()),
            name="Caretaker",
            category="care",
            description="Take care of your pet daily",
            requirement_type="milestone",
            requirement_value=7,
            reward_experience=100,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(achievement)
        db_session.commit()
        
        achievement_dict = achievement.to_dict()
        
        assert achievement_dict["id"] == achievement.id
        assert achievement_dict["name"] == "Caretaker"
        assert achievement_dict["rewards"]["experience"] == 100