"""Repository for Tamagotchi operations."""
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.repositories.base import BaseRepository
from src.models.tamagotchi import Tamagotchi


class TamagotchiRepository(BaseRepository[Tamagotchi]):
    """Repository for Tamagotchi-specific operations."""
    
    def __init__(self, db_session: Session):
        """Initialize Tamagotchi repository."""
        super().__init__(Tamagotchi, db_session)
    
    def get_by_owner(self, owner_id: str) -> List[Tamagotchi]:
        """Get all Tamagotchis owned by a user.
        
        Args:
            owner_id: User ID
            
        Returns:
            List of Tamagotchis
        """
        return self.db.query(Tamagotchi).filter(
            Tamagotchi.owner_id == owner_id
        ).all()
    
    def get_active_by_owner(self, owner_id: str) -> List[Tamagotchi]:
        """Get all active (alive) Tamagotchis owned by a user.
        
        Args:
            owner_id: User ID
            
        Returns:
            List of active Tamagotchis
        """
        return self.db.query(Tamagotchi).filter(
            Tamagotchi.owner_id == owner_id,
            Tamagotchi.health > 0
        ).all()
    
    def update_stats(self, tamagotchi_id: str) -> Optional[Tamagotchi]:
        """Update Tamagotchi stats based on time passed.
        
        Args:
            tamagotchi_id: Tamagotchi ID
            
        Returns:
            Updated Tamagotchi or None if not found
        """
        tamagotchi = self.get(tamagotchi_id)
        if not tamagotchi:
            return None
        
        # Calculate time since last update
        now = datetime.utcnow()
        time_delta = now - tamagotchi.last_stat_update
        minutes_passed = time_delta.total_seconds() / 60
        
        # Update stats
        tamagotchi.update_stats(minutes_passed)
        
        # Check for state changes
        if tamagotchi.energy < 20 and not tamagotchi.is_sleeping:
            tamagotchi.is_sleeping = True
            tamagotchi.current_activity = "sleeping"
        elif tamagotchi.energy > 80 and tamagotchi.is_sleeping:
            tamagotchi.is_sleeping = False
            tamagotchi.current_activity = None
        
        # Update mood based on stats
        if tamagotchi.happiness > 80:
            tamagotchi.current_mood = "happy"
        elif tamagotchi.happiness > 50:
            tamagotchi.current_mood = "content"
        elif tamagotchi.happiness > 30:
            tamagotchi.current_mood = "neutral"
        else:
            tamagotchi.current_mood = "sad"
        
        # Check if sick
        if tamagotchi.health < 30 and not tamagotchi.is_sick:
            tamagotchi.is_sick = True
        elif tamagotchi.health > 70 and tamagotchi.is_sick:
            tamagotchi.is_sick = False
        
        tamagotchi.updated_at = now
        self.db.commit()
        self.db.refresh(tamagotchi)
        
        return tamagotchi
    
    def feed(self, tamagotchi_id: str, food_value: float = 20.0) -> Optional[Tamagotchi]:
        """Feed the Tamagotchi.
        
        Args:
            tamagotchi_id: Tamagotchi ID
            food_value: Amount to increase hunger stat
            
        Returns:
            Updated Tamagotchi or None if not found
        """
        tamagotchi = self.get(tamagotchi_id)
        if not tamagotchi:
            return None
        
        tamagotchi.hunger = min(100, tamagotchi.hunger + food_value)
        tamagotchi.last_fed = datetime.utcnow()
        tamagotchi.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(tamagotchi)
        
        return tamagotchi
    
    def play(self, tamagotchi_id: str, happiness_value: float = 15.0) -> Optional[Tamagotchi]:
        """Play with the Tamagotchi.
        
        Args:
            tamagotchi_id: Tamagotchi ID
            happiness_value: Amount to increase happiness
            
        Returns:
            Updated Tamagotchi or None if not found
        """
        tamagotchi = self.get(tamagotchi_id)
        if not tamagotchi:
            return None
        
        tamagotchi.happiness = min(100, tamagotchi.happiness + happiness_value)
        tamagotchi.energy = max(0, tamagotchi.energy - 10)  # Playing uses energy
        tamagotchi.last_played = datetime.utcnow()
        tamagotchi.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(tamagotchi)
        
        return tamagotchi
    
    def clean(self, tamagotchi_id: str) -> Optional[Tamagotchi]:
        """Clean the Tamagotchi.
        
        Args:
            tamagotchi_id: Tamagotchi ID
            
        Returns:
            Updated Tamagotchi or None if not found
        """
        tamagotchi = self.get(tamagotchi_id)
        if not tamagotchi:
            return None
        
        tamagotchi.cleanliness = 100
        tamagotchi.happiness = min(100, tamagotchi.happiness + 5)
        tamagotchi.last_cleaned = datetime.utcnow()
        tamagotchi.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(tamagotchi)
        
        return tamagotchi
    
    def give_medicine(self, tamagotchi_id: str) -> Optional[Tamagotchi]:
        """Give medicine to the Tamagotchi.
        
        Args:
            tamagotchi_id: Tamagotchi ID
            
        Returns:
            Updated Tamagotchi or None if not found
        """
        tamagotchi = self.get(tamagotchi_id)
        if not tamagotchi:
            return None
        
        if tamagotchi.is_sick:
            tamagotchi.is_sick = False
            tamagotchi.health = min(100, tamagotchi.health + 30)
        else:
            tamagotchi.health = min(100, tamagotchi.health + 10)
        
        tamagotchi.last_medicine = datetime.utcnow()
        tamagotchi.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(tamagotchi)
        
        return tamagotchi
    
    def add_experience(self, tamagotchi_id: str, exp_points: int) -> Optional[Tamagotchi]:
        """Add experience points and handle leveling.
        
        Args:
            tamagotchi_id: Tamagotchi ID
            exp_points: Experience points to add
            
        Returns:
            Updated Tamagotchi or None if not found
        """
        tamagotchi = self.get(tamagotchi_id)
        if not tamagotchi:
            return None
        
        tamagotchi.experience += exp_points
        
        # Check for level up (100 exp per level)
        new_level = (tamagotchi.experience // 100) + 1
        if new_level > tamagotchi.level:
            tamagotchi.level = new_level
            
            # Check for evolution
            if tamagotchi.level >= 5 and tamagotchi.evolution_stage == "baby":
                tamagotchi.evolution_stage = "child"
            elif tamagotchi.level >= 10 and tamagotchi.evolution_stage == "child":
                tamagotchi.evolution_stage = "teen"
            elif tamagotchi.level >= 20 and tamagotchi.evolution_stage == "teen":
                tamagotchi.evolution_stage = "adult"
            elif tamagotchi.level >= 50 and tamagotchi.evolution_stage == "adult":
                tamagotchi.evolution_stage = "elder"
        
        tamagotchi.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(tamagotchi)
        
        return tamagotchi
    
    def get_requiring_attention(self, threshold_hours: int = 24) -> List[Tamagotchi]:
        """Get Tamagotchis that need attention.
        
        Args:
            threshold_hours: Hours since last interaction
            
        Returns:
            List of Tamagotchis needing attention
        """
        threshold_time = datetime.utcnow() - timedelta(hours=threshold_hours)
        
        return self.db.query(Tamagotchi).filter(
            (Tamagotchi.last_interaction < threshold_time) |
            (Tamagotchi.last_interaction == None),
            Tamagotchi.health > 0  # Only alive Tamagotchis
        ).all()