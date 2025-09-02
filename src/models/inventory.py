"""Inventory and item models for Tamagotchi."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship
from src.database.config import Base


class Item(Base):
    """Master table of all possible items in the game."""
    
    __tablename__ = "items"
    
    # Primary key
    id = Column(String(36), primary_key=True)  # UUID
    
    # Item details
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False)  # food, toy, medicine, decoration, etc.
    subcategory = Column(String(50), nullable=True)
    description = Column(String(500), nullable=True)
    icon_url = Column(String(500), nullable=True)
    
    # Item properties
    rarity = Column(String(20), nullable=False, default="common")  # common, uncommon, rare, epic, legendary
    cost = Column(Integer, nullable=False, default=0)
    sell_value = Column(Integer, nullable=False, default=0)
    is_consumable = Column(Boolean, nullable=False, default=True)
    max_stack = Column(Integer, nullable=False, default=99)
    
    # Effects when used
    effects = Column(JSON, nullable=True)  # Dict of stat changes and special effects
    duration_minutes = Column(Integer, nullable=True)  # How long effects last
    cooldown_minutes = Column(Integer, nullable=True)  # How long before can use again
    
    # Requirements
    level_required = Column(Integer, nullable=False, default=1)
    evolution_stage_required = Column(String(50), nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="item")
    
    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name}, category={self.category})>"


class InventoryItem(Base):
    """Items owned by a specific Tamagotchi."""
    
    __tablename__ = "inventory_items"
    
    # Primary key
    id = Column(String(36), primary_key=True)  # UUID
    
    # Foreign keys
    tamagotchi_id = Column(String(36), ForeignKey("tamagotchis.id"), nullable=False)
    item_id = Column(String(36), ForeignKey("items.id"), nullable=False)
    
    # Inventory details
    quantity = Column(Integer, nullable=False, default=1)
    acquired_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    times_used = Column(Integer, nullable=False, default=0)
    
    # Item state
    is_equipped = Column(Boolean, nullable=False, default=False)
    is_favorite = Column(Boolean, nullable=False, default=False)
    custom_name = Column(String(100), nullable=True)  # If user renames the item
    
    # Metadata
    metadata = Column(JSON, nullable=True)  # Any item-specific data
    
    # Relationships
    tamagotchi = relationship("Tamagotchi", back_populates="items")
    item = relationship("Item", back_populates="inventory_items")
    
    def __repr__(self):
        return f"<InventoryItem(id={self.id}, item_id={self.item_id}, quantity={self.quantity})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "tamagotchi_id": self.tamagotchi_id,
            "item": {
                "id": self.item.id,
                "name": self.item.name,
                "category": self.item.category,
                "description": self.item.description,
                "icon_url": self.item.icon_url,
                "rarity": self.item.rarity,
                "effects": self.item.effects
            } if self.item else None,
            "quantity": self.quantity,
            "acquired_at": self.acquired_at.isoformat() if self.acquired_at else None,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "times_used": self.times_used,
            "is_equipped": self.is_equipped,
            "is_favorite": self.is_favorite,
            "custom_name": self.custom_name,
            "metadata": self.metadata
        }