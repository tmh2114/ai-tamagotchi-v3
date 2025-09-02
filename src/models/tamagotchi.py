"""Tamagotchi entity model."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from src.database.config import Base


class Tamagotchi(Base):
    """Main Tamagotchi entity model."""
    
    __tablename__ = "tamagotchis"
    
    # Primary key
    id = Column(String(36), primary_key=True)  # UUID
    
    # Basic information
    name = Column(String(100), nullable=False)
    species = Column(String(50), nullable=False, default="digital_pet")
    avatar_url = Column(String(500), nullable=True)
    
    # Personality and traits
    personality_type = Column(String(50), nullable=False, default="friendly")
    personality_traits = Column(JSON, nullable=False, default=list)  # List of trait strings
    voice_style = Column(String(100), nullable=True)
    
    # Stats (0-100 scale)
    happiness = Column(Float, nullable=False, default=50.0)
    health = Column(Float, nullable=False, default=100.0)
    hunger = Column(Float, nullable=False, default=50.0)
    energy = Column(Float, nullable=False, default=100.0)
    cleanliness = Column(Float, nullable=False, default=100.0)
    
    # Experience and growth
    experience = Column(Integer, nullable=False, default=0)
    level = Column(Integer, nullable=False, default=1)
    evolution_stage = Column(String(50), nullable=False, default="baby")
    
    # Learning and memory
    learned_behaviors = Column(JSON, nullable=False, default=list)
    memory_bank = Column(JSON, nullable=False, default=dict)  # Stores important memories
    preferences = Column(JSON, nullable=False, default=dict)  # User preferences learned over time
    
    # State tracking
    current_mood = Column(String(50), nullable=False, default="neutral")
    current_activity = Column(String(100), nullable=True)
    is_sleeping = Column(Boolean, nullable=False, default=False)
    is_sick = Column(Boolean, nullable=False, default=False)
    
    # Timestamps
    birth_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_fed = Column(DateTime, nullable=True)
    last_played = Column(DateTime, nullable=True)
    last_cleaned = Column(DateTime, nullable=True)
    last_medicine = Column(DateTime, nullable=True)
    last_interaction = Column(DateTime, nullable=True)
    last_stat_update = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Metadata
    owner_id = Column(String(36), nullable=False)  # UUID of owner
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interactions = relationship("Interaction", back_populates="tamagotchi", cascade="all, delete-orphan")
    items = relationship("InventoryItem", back_populates="tamagotchi", cascade="all, delete-orphan")
    achievements = relationship("Achievement", secondary="tamagotchi_achievements", back_populates="tamagotchis")
    activities = relationship("Activity", back_populates="tamagotchi", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Tamagotchi(id={self.id}, name={self.name}, level={self.level})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "avatar_url": self.avatar_url,
            "personality_type": self.personality_type,
            "personality_traits": self.personality_traits,
            "voice_style": self.voice_style,
            "stats": {
                "happiness": self.happiness,
                "health": self.health,
                "hunger": self.hunger,
                "energy": self.energy,
                "cleanliness": self.cleanliness
            },
            "experience": self.experience,
            "level": self.level,
            "evolution_stage": self.evolution_stage,
            "current_mood": self.current_mood,
            "current_activity": self.current_activity,
            "is_sleeping": self.is_sleeping,
            "is_sick": self.is_sick,
            "owner_id": self.owner_id,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_stats(self, time_delta_minutes: float):
        """Update stats based on time passed.
        
        Args:
            time_delta_minutes: Minutes since last update
        """
        # Decrease stats over time
        decay_rate = time_delta_minutes / 60  # Convert to hours
        
        self.hunger = max(0, self.hunger - (5 * decay_rate))  # Loses 5 hunger per hour
        self.energy = max(0, self.energy - (3 * decay_rate))  # Loses 3 energy per hour
        self.cleanliness = max(0, self.cleanliness - (2 * decay_rate))  # Loses 2 cleanliness per hour
        
        # Happiness decays based on other stats
        if self.hunger < 30 or self.energy < 20 or self.cleanliness < 30:
            self.happiness = max(0, self.happiness - (4 * decay_rate))
        
        # Health affected by extreme conditions
        if self.hunger < 10 or self.is_sick:
            self.health = max(0, self.health - (2 * decay_rate))
        
        self.last_stat_update = datetime.utcnow()