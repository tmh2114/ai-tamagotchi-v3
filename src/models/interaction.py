"""Interaction model for tracking user interactions with Tamagotchi."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.database.config import Base


class Interaction(Base):
    """Model for tracking interactions between users and their Tamagotchi."""
    
    __tablename__ = "interactions"
    
    # Primary key
    id = Column(String(36), primary_key=True)  # UUID
    
    # Foreign key
    tamagotchi_id = Column(String(36), ForeignKey("tamagotchis.id"), nullable=False)
    
    # Interaction details
    interaction_type = Column(String(50), nullable=False)  # feed, play, clean, talk, etc.
    interaction_subtype = Column(String(50), nullable=True)  # specific food, game, etc.
    
    # User input/output
    user_message = Column(Text, nullable=True)  # What the user said/did
    tamagotchi_response = Column(Text, nullable=True)  # How the Tamagotchi responded
    
    # Effects on stats
    happiness_change = Column(Float, nullable=False, default=0.0)
    health_change = Column(Float, nullable=False, default=0.0)
    hunger_change = Column(Float, nullable=False, default=0.0)
    energy_change = Column(Float, nullable=False, default=0.0)
    cleanliness_change = Column(Float, nullable=False, default=0.0)
    experience_gained = Column(Integer, nullable=False, default=0)
    
    # Emotional context
    emotion_before = Column(String(50), nullable=True)
    emotion_after = Column(String(50), nullable=True)
    sentiment_score = Column(Float, nullable=True)  # -1 to 1 sentiment analysis score
    
    # Additional data
    metadata = Column(JSON, nullable=True)  # Any additional interaction-specific data
    duration_seconds = Column(Integer, nullable=True)  # How long the interaction lasted
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    tamagotchi = relationship("Tamagotchi", back_populates="interactions")
    
    def __repr__(self):
        return f"<Interaction(id={self.id}, type={self.interaction_type}, tamagotchi_id={self.tamagotchi_id})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "tamagotchi_id": self.tamagotchi_id,
            "interaction_type": self.interaction_type,
            "interaction_subtype": self.interaction_subtype,
            "user_message": self.user_message,
            "tamagotchi_response": self.tamagotchi_response,
            "stat_changes": {
                "happiness": self.happiness_change,
                "health": self.health_change,
                "hunger": self.hunger_change,
                "energy": self.energy_change,
                "cleanliness": self.cleanliness_change,
                "experience": self.experience_gained
            },
            "emotion_before": self.emotion_before,
            "emotion_after": self.emotion_after,
            "sentiment_score": self.sentiment_score,
            "metadata": self.metadata,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }