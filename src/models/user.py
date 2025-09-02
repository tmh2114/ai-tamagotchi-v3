"""User model for Tamagotchi owners."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from src.database.config import Base


class User(Base):
    """Model for users who own Tamagotchis."""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(String(36), primary_key=True)  # UUID
    
    # User identification
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Authentication (password hash would be stored separately in production)
    password_hash = Column(String(255), nullable=False)
    
    # User stats
    total_playtime_minutes = Column(Integer, nullable=False, default=0)
    total_tamagotchis_raised = Column(Integer, nullable=False, default=0)
    current_streak_days = Column(Integer, nullable=False, default=0)
    longest_streak_days = Column(Integer, nullable=False, default=0)
    
    # Currency and resources
    coins = Column(Integer, nullable=False, default=100)  # Starting currency
    gems = Column(Integer, nullable=False, default=0)  # Premium currency
    experience_points = Column(Integer, nullable=False, default=0)
    player_level = Column(Integer, nullable=False, default=1)
    
    # Preferences
    preferences = Column(JSON, nullable=False, default=dict)  # User settings and preferences
    notification_settings = Column(JSON, nullable=False, default=dict)
    timezone = Column(String(50), nullable=False, default="UTC")
    language = Column(String(10), nullable=False, default="en")
    
    # Social features
    friend_code = Column(String(20), nullable=True, unique=True)
    is_public_profile = Column(Boolean, nullable=False, default=False)
    bio = Column(String(500), nullable=True)
    
    # Account status
    is_active = Column(Boolean, nullable=False, default=True)
    is_premium = Column(Boolean, nullable=False, default=False)
    premium_expires_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Note: Relationships would be added here for tamagotchis owned, friends, etc.
    # tamagotchis = relationship("Tamagotchi", back_populates="owner")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, level={self.player_level})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "display_name": self.display_name,
            "avatar_url": self.avatar_url,
            "stats": {
                "total_playtime_minutes": self.total_playtime_minutes,
                "total_tamagotchis_raised": self.total_tamagotchis_raised,
                "current_streak_days": self.current_streak_days,
                "longest_streak_days": self.longest_streak_days,
                "player_level": self.player_level,
                "experience_points": self.experience_points
            },
            "resources": {
                "coins": self.coins,
                "gems": self.gems
            },
            "preferences": self.preferences,
            "notification_settings": self.notification_settings,
            "timezone": self.timezone,
            "language": self.language,
            "friend_code": self.friend_code,
            "is_public_profile": self.is_public_profile,
            "bio": self.bio,
            "is_active": self.is_active,
            "is_premium": self.is_premium,
            "premium_expires_at": self.premium_expires_at.isoformat() if self.premium_expires_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }