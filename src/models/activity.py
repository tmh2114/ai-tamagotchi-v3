"""Activity model for tracking Tamagotchi activities and routines."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.database.config import Base


class Activity(Base):
    """Model for tracking Tamagotchi activities and daily routines."""
    
    __tablename__ = "activities"
    
    # Primary key
    id = Column(String(36), primary_key=True)  # UUID
    
    # Foreign key
    tamagotchi_id = Column(String(36), ForeignKey("tamagotchis.id"), nullable=False)
    
    # Activity details
    activity_type = Column(String(50), nullable=False)  # sleeping, eating, playing, exploring, etc.
    activity_name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    
    # Scheduling
    is_scheduled = Column(Boolean, nullable=False, default=False)
    scheduled_time = Column(DateTime, nullable=True)  # When this should happen
    recurrence_pattern = Column(String(50), nullable=True)  # daily, weekly, etc.
    
    # Execution
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    was_successful = Column(Boolean, nullable=True)
    
    # Activity context
    location = Column(String(100), nullable=True)  # Where the activity takes place
    participants = Column(JSON, nullable=True)  # Other Tamagotchis or NPCs involved
    required_items = Column(JSON, nullable=True)  # Items needed for the activity
    rewards = Column(JSON, nullable=True)  # What the Tamagotchi gains from this
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tamagotchi = relationship("Tamagotchi", back_populates="activities")
    
    def __repr__(self):
        return f"<Activity(id={self.id}, name={self.activity_name}, type={self.activity_type})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "tamagotchi_id": self.tamagotchi_id,
            "activity_type": self.activity_type,
            "activity_name": self.activity_name,
            "description": self.description,
            "is_scheduled": self.is_scheduled,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "recurrence_pattern": self.recurrence_pattern,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_minutes": self.duration_minutes,
            "was_successful": self.was_successful,
            "location": self.location,
            "participants": self.participants,
            "required_items": self.required_items,
            "rewards": self.rewards,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }