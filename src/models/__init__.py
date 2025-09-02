"""Data models for AI Tamagotchi v3."""
from src.models.user import User
from src.models.tamagotchi import Tamagotchi
from src.models.interaction import Interaction
from src.models.activity import Activity
from src.models.inventory import Item, InventoryItem
from src.models.achievement import Achievement, tamagotchi_achievements

__all__ = [
    "User",
    "Tamagotchi",
    "Interaction",
    "Activity",
    "Item",
    "InventoryItem",
    "Achievement",
    "tamagotchi_achievements"
]