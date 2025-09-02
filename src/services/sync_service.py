"""Data synchronization service for offline/online sync."""
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from uuid import uuid4
import hashlib
from sqlalchemy.orm import Session
from src.database.config import get_db
from src.models import Tamagotchi, User, Interaction, Activity


class SyncService:
    """Service for handling data synchronization."""
    
    def __init__(self, cache_dir: str = "./cache"):
        """Initialize sync service.
        
        Args:
            cache_dir: Directory for storing sync cache
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.sync_log_path = os.path.join(cache_dir, "sync_log.json")
        self.pending_sync_path = os.path.join(cache_dir, "pending_sync.json")
    
    def export_user_data(self, user_id: str, db: Session) -> Dict[str, Any]:
        """Export all user data for backup or transfer.
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Dictionary containing all user data
        """
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Get all tamagotchis
        tamagotchis = db.query(Tamagotchi).filter(
            Tamagotchi.owner_id == user_id
        ).all()
        
        # Get all interactions for user's tamagotchis
        tamagotchi_ids = [t.id for t in tamagotchis]
        interactions = db.query(Interaction).filter(
            Interaction.tamagotchi_id.in_(tamagotchi_ids)
        ).all()
        
        # Get all activities
        activities = db.query(Activity).filter(
            Activity.tamagotchi_id.in_(tamagotchi_ids)
        ).all()
        
        # Build export data
        export_data = {
            "version": "1.0",
            "export_date": datetime.utcnow().isoformat(),
            "user": user.to_dict(),
            "tamagotchis": [t.to_dict() for t in tamagotchis],
            "interactions": [i.to_dict() for i in interactions],
            "activities": [a.to_dict() for a in activities],
            "metadata": {
                "total_tamagotchis": len(tamagotchis),
                "total_interactions": len(interactions),
                "total_activities": len(activities)
            }
        }
        
        # Generate checksum
        data_str = json.dumps(export_data, sort_keys=True)
        export_data["checksum"] = hashlib.sha256(data_str.encode()).hexdigest()
        
        return export_data
    
    def import_user_data(self, import_data: Dict[str, Any], db: Session, merge: bool = False) -> Dict[str, Any]:
        """Import user data from backup.
        
        Args:
            import_data: Data to import
            db: Database session
            merge: Whether to merge with existing data or replace
            
        Returns:
            Import results
        """
        # Verify checksum
        checksum = import_data.pop("checksum", None)
        data_str = json.dumps(import_data, sort_keys=True)
        calculated_checksum = hashlib.sha256(data_str.encode()).hexdigest()
        
        if checksum and checksum != calculated_checksum:
            raise ValueError("Data integrity check failed")
        
        results = {
            "users_imported": 0,
            "tamagotchis_imported": 0,
            "interactions_imported": 0,
            "activities_imported": 0,
            "errors": []
        }
        
        try:
            # Import user
            user_data = import_data["user"]
            existing_user = db.query(User).filter(User.id == user_data["id"]).first()
            
            if existing_user and not merge:
                results["errors"].append(f"User {user_data['id']} already exists")
            else:
                if not existing_user:
                    user = User(**{k: v for k, v in user_data.items() 
                                  if k not in ["created_at", "updated_at"]})
                    db.add(user)
                    results["users_imported"] += 1
            
            # Import tamagotchis
            for tama_data in import_data.get("tamagotchis", []):
                existing = db.query(Tamagotchi).filter(
                    Tamagotchi.id == tama_data["id"]
                ).first()
                
                if not existing or merge:
                    if existing:
                        for key, value in tama_data.items():
                            if key not in ["id", "created_at"]:
                                setattr(existing, key, value)
                    else:
                        tama = Tamagotchi(**{k: v for k, v in tama_data.items()
                                            if k not in ["stats", "created_at", "updated_at"]})
                        if "stats" in tama_data:
                            for stat, value in tama_data["stats"].items():
                                setattr(tama, stat, value)
                        db.add(tama)
                    results["tamagotchis_imported"] += 1
            
            # Import interactions
            for interaction_data in import_data.get("interactions", []):
                existing = db.query(Interaction).filter(
                    Interaction.id == interaction_data["id"]
                ).first()
                
                if not existing:
                    interaction = Interaction(**{k: v for k, v in interaction_data.items()
                                               if k not in ["stat_changes", "created_at"]})
                    db.add(interaction)
                    results["interactions_imported"] += 1
            
            # Import activities
            for activity_data in import_data.get("activities", []):
                existing = db.query(Activity).filter(
                    Activity.id == activity_data["id"]
                ).first()
                
                if not existing:
                    activity = Activity(**{k: v for k, v in activity_data.items()
                                        if k not in ["created_at", "updated_at"]})
                    db.add(activity)
                    results["activities_imported"] += 1
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            results["errors"].append(str(e))
            raise
        
        return results
    
    def cache_pending_changes(self, changes: List[Dict[str, Any]]):
        """Cache changes that need to be synced.
        
        Args:
            changes: List of changes to cache
        """
        pending = []
        if os.path.exists(self.pending_sync_path):
            with open(self.pending_sync_path, 'r') as f:
                pending = json.load(f)
        
        for change in changes:
            change["id"] = str(uuid4())
            change["timestamp"] = datetime.utcnow().isoformat()
            pending.append(change)
        
        with open(self.pending_sync_path, 'w') as f:
            json.dump(pending, f, indent=2)
    
    def get_pending_changes(self) -> List[Dict[str, Any]]:
        """Get all pending changes to sync.
        
        Returns:
            List of pending changes
        """
        if not os.path.exists(self.pending_sync_path):
            return []
        
        with open(self.pending_sync_path, 'r') as f:
            return json.load(f)
    
    def clear_pending_changes(self, change_ids: Optional[List[str]] = None):
        """Clear pending changes after successful sync.
        
        Args:
            change_ids: Specific change IDs to clear, or None to clear all
        """
        if not os.path.exists(self.pending_sync_path):
            return
        
        if change_ids is None:
            # Clear all
            with open(self.pending_sync_path, 'w') as f:
                json.dump([], f)
        else:
            # Clear specific changes
            with open(self.pending_sync_path, 'r') as f:
                pending = json.load(f)
            
            pending = [c for c in pending if c.get("id") not in change_ids]
            
            with open(self.pending_sync_path, 'w') as f:
                json.dump(pending, f, indent=2)
    
    def log_sync(self, sync_type: str, status: str, details: Dict[str, Any]):
        """Log sync operation.
        
        Args:
            sync_type: Type of sync (export, import, auto)
            status: Status (success, failure, partial)
            details: Additional details
        """
        log_entry = {
            "id": str(uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "type": sync_type,
            "status": status,
            "details": details
        }
        
        logs = []
        if os.path.exists(self.sync_log_path):
            with open(self.sync_log_path, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        # Keep only last 100 entries
        logs = logs[-100:]
        
        with open(self.sync_log_path, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def get_sync_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get sync operation history.
        
        Args:
            limit: Number of entries to return
            
        Returns:
            List of sync log entries
        """
        if not os.path.exists(self.sync_log_path):
            return []
        
        with open(self.sync_log_path, 'r') as f:
            logs = json.load(f)
        
        return logs[-limit:]