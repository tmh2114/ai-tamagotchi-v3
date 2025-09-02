"""Achievement model for tracking Tamagotchi accomplishments."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, JSON, Table, Text
from sqlalchemy.orm import relationship
from src.database.config import Base

# Association table for many-to-many relationship between Tamagotchis and Achievements
tamagotchi_achievements = Table(
    'tamagotchi_achievements',
    Base.metadata,
    Column('tamagotchi_id', String(36), ForeignKey('tamagotchis.id'), primary_key=True),
    Column('achievement_id', String(36), ForeignKey('achievements.id'), primary_key=True),
    Column('unlocked_at', DateTime, nullable=False, default=datetime.utcnow),
    Column('progress', Integer, nullable=False, default=0),
    Column('is_completed', Boolean, nullable=False, default=False)
)


class Achievement(Base):
    """Model for achievements and milestones."""
    
    __tablename__ = "achievements"
    
    # Primary key
    id = Column(String(36), primary_key=True)  # UUID
    
    # Achievement details
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False)  # care, social, exploration, collection, special
    description = Column(Text, nullable=False)
    icon_url = Column(String(500), nullable=True)
    
    # Achievement requirements
    requirement_type = Column(String(50), nullable=False)  # counter, milestone, collection, special
    requirement_value = Column(Integer, nullable=False, default=1)  # Target value to achieve
    requirement_details = Column(JSON, nullable=True)  # Specific conditions
    
    # Rewards
    reward_experience = Column(Integer, nullable=False, default=0)
    reward_items = Column(JSON, nullable=True)  # List of item IDs and quantities
    reward_title = Column(String(100), nullable=True)  # Special title earned
    reward_badge_url = Column(String(500), nullable=True)
    
    # Achievement properties
    tier = Column(String(20), nullable=False, default="bronze")  # bronze, silver, gold, platinum
    points = Column(Integer, nullable=False, default=10)
    is_hidden = Column(Boolean, nullable=False, default=False)  # Secret achievements
    is_repeatable = Column(Boolean, nullable=False, default=False)
    
    # Display order
    display_order = Column(Integer, nullable=False, default=0)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tamagotchis = relationship("Tamagotchi", secondary=tamagotchi_achievements, back_populates="achievements")
    
    def __repr__(self):
        return f"<Achievement(id={self.id}, name={self.name}, tier={self.tier})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "icon_url": self.icon_url,
            "requirement_type": self.requirement_type,
            "requirement_value": self.requirement_value,
            "requirement_details": self.requirement_details,
            "rewards": {
                "experience": self.reward_experience,
                "items": self.reward_items,
                "title": self.reward_title,
                "badge_url": self.reward_badge_url
            },
            "tier": self.tier,
            "points": self.points,
            "is_hidden": self.is_hidden,
            "is_repeatable": self.is_repeatable,
            "display_order": self.display_order,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }