"""Base repository class for common database operations."""
from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.config import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db_session: Session):
        """Initialize repository.
        
        Args:
            model: SQLAlchemy model class
            db_session: Database session
        """
        self.model = model
        self.db = db_session
    
    def create(self, **kwargs) -> ModelType:
        """Create a new entity.
        
        Args:
            **kwargs: Entity attributes
            
        Returns:
            Created entity
        """
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid4())
        
        entity = self.model(**kwargs)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def get(self, entity_id: str) -> Optional[ModelType]:
        """Get entity by ID.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            Entity or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == entity_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all entities with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of entities
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, entity_id: str, **kwargs) -> Optional[ModelType]:
        """Update entity.
        
        Args:
            entity_id: Entity ID
            **kwargs: Attributes to update
            
        Returns:
            Updated entity or None if not found
        """
        entity = self.get(entity_id)
        if not entity:
            return None
        
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def delete(self, entity_id: str) -> bool:
        """Delete entity.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            True if deleted, False if not found
        """
        entity = self.get(entity_id)
        if not entity:
            return False
        
        self.db.delete(entity)
        self.db.commit()
        return True
    
    def exists(self, entity_id: str) -> bool:
        """Check if entity exists.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            True if exists, False otherwise
        """
        return self.db.query(self.model).filter(self.model.id == entity_id).count() > 0
    
    def count(self) -> int:
        """Get total count of entities.
        
        Returns:
            Total count
        """
        return self.db.query(self.model).count()
    
    def find_by(self, **kwargs) -> List[ModelType]:
        """Find entities by attributes.
        
        Args:
            **kwargs: Attributes to filter by
            
        Returns:
            List of matching entities
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.all()
    
    def find_one_by(self, **kwargs) -> Optional[ModelType]:
        """Find first entity by attributes.
        
        Args:
            **kwargs: Attributes to filter by
            
        Returns:
            First matching entity or None
        """
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first()
    
    def bulk_create(self, entities: List[Dict[str, Any]]) -> List[ModelType]:
        """Create multiple entities.
        
        Args:
            entities: List of entity data dictionaries
            
        Returns:
            List of created entities
        """
        created_entities = []
        for entity_data in entities:
            if 'id' not in entity_data:
                entity_data['id'] = str(uuid4())
            entity = self.model(**entity_data)
            self.db.add(entity)
            created_entities.append(entity)
        
        self.db.commit()
        for entity in created_entities:
            self.db.refresh(entity)
        
        return created_entities
    
    def commit(self):
        """Commit current transaction."""
        self.db.commit()
    
    def rollback(self):
        """Rollback current transaction."""
        self.db.rollback()